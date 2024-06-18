#  Copyright 2020-2023 Robert Bosch GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#################################################################################
#
# File: JsonPreprocessor.py
#
# This module uses to handle connfiguration file in json format (import another
# json file to the json file).
# Allows user adds comment into json config file
#
# History:
#
# 2021-01:
#    - Initially created by Mai Dinh Nam Son (RBVH/ECM11)
#
# 2021-02-08:
#   - Use object_pairs_hook of json.load() to process [import] node(s).
#     Allow to use multiple [import] node(s) at same level.
#   - Avoid cyclic import
#
# 2021-02-17:
#   - Replace method to load json data json.load() by json.loads()
#     to load string data after removing comment(s)
#
# 2021-02-18:
#   - Add parameter syntax to support Python types if required:
#     None  => null
#     True  => true
#     False => false
#
# 2021-03-29:
#   - Adds update configuration using json file
#   - Handles nested parameter in json config file
#################################################################################


import os
import json
import re
import sys
import copy
import shlex

from PythonExtensionsCollection.String.CString import CString
from enum import Enum
from JsonPreprocessor.version import VERSION, VERSION_DATE
from pydotdict import DotDict

class CSyntaxType():
    python = "python"
    json = "json"

class CNameMangling(Enum):
    AVOIDDATATYPE    = "JPavoidDataType_"
    COLONS           = "__handleColonsInLine__"
    DUPLICATEDKEY_00 = "__handleDuplicatedKey__00"
    DUPLICATEDKEY_01 = "__handleDuplicatedKey__"
    STRINGCONVERT    = "__ConvertParameterToString__"
    LISTINDEX        = "__IndexOfList__"
    SLICEINDEX       = "__SlicingIndex__"
    STRINGVALUE      = "__StringValueMake-up__"

class CPythonJSONDecoder(json.JSONDecoder):
    """
Extends the JSON syntax by the Python keywords ``True``, ``False`` and ``None``.

**Arguments:**

* ``json.JSONDecoder``

  / *Type*: object /

  Decoder object provided by ``json.loads``
    """

    NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_once = self.custom_scan_once

    def _custom_scan_once(self, string :str, idx: int) -> any:
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx) from None

        if nextchar == '"':
            return self.parse_string(string, idx + 1, self.strict)
        elif nextchar == '{':
            return self.parse_object((string, idx + 1), self.strict,
                self._custom_scan_once, self.object_hook, self.object_pairs_hook, self.memo)
        elif nextchar == '[':
            return self.parse_array((string, idx + 1), self._custom_scan_once)
        elif nextchar == 'n' and string[idx:idx + 4] == 'null':
            return None, idx + 4
        elif nextchar == 't' and string[idx:idx + 4] == 'true':
            return True, idx + 4
        elif nextchar == 'f' and string[idx:idx + 5] == 'false':
            return False, idx + 5
        elif nextchar == 'N' and string[idx:idx + 4] == 'None':
            return None, idx + 4
        elif nextchar == 'T' and string[idx:idx + 4] == 'True':
            return True, idx + 4
        elif nextchar == 'F' and string[idx:idx + 5] == 'False':
            return False, idx + 5

        m = CPythonJSONDecoder.NUMBER_RE.match(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = self.parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = self.parse_int(integer)
            return res, m.end()
        elif nextchar == 'N' and string[idx:idx + 3] == 'NaN':
            return self.parse_constant('NaN'), idx + 3
        elif nextchar == 'I' and string[idx:idx + 8] == 'Infinity':
            return self.parse_constant('Infinity'), idx + 8
        elif nextchar == '-' and string[idx:idx + 9] == '-Infinity':
            return self.parse_constant('-Infinity'), idx + 9
        else:
            raise StopIteration(idx)

    def custom_scan_once(self, string : str, idx : int) -> any:
        try:
            return self._custom_scan_once(string, idx)
        finally:
            self.memo.clear()

class CJsonPreprocessor():
    """
CJsonPreprocessor extends the JSON syntax by the following features:

* Allow c/c++-style comments within JSON files
* Allow to import JSON files into JSON files
* Allow to define and use parameters within JSON files
* Allow Python keywords ``True``, ``False`` and ``None``
    """

    def getVersion(self):
        """
Returns the version of JsonPreprocessor as string.
        """
        return VERSION
    
    def getVersionDate(self):
        """
Returns the version date of JsonPreprocessor as string.
        """
        return VERSION_DATE

    def __init__(self, syntax: CSyntaxType = CSyntaxType.python , currentCfg : dict = {}) -> None:
        """
Constructor

**Arguments:**

* ``syntax`` (*CSyntaxType*) optional

  / *Condition*: optional / *Type*: CSyntaxType / *Default*: python /

  If set to ``python``, then Python data types are allowed as part of JSON file.

* ``currentCfg`` (*dict*) optional

  / *Condition*: optional / *Type*: dict / *Default*: {} /

  Internally used to aggregate imported json files.
        """
        import builtins
        import keyword
        self.lDataTypes = [name for name, value in vars(builtins).items() if isinstance(value, type)]
        self.specialCharacters = r'!@#$%^&*()+=[\]{}|;:\'",<>?/`~'
        self.lDataTypes.append(keyword.kwlist)
        self.jsonPath        = None
        self.masterFile      = None
        self.handlingFile    = []
        self.lImportedFiles  = []
        self.recursive_level = 0
        self.syntax          = syntax
        self.currentCfg      = currentCfg
        self.dUpdatedParams  = {}
        self.lNestedParams   = []
        self.lDotInParamName = []
        self.bDuplicatedKeys = True
        self.jsonCheck       = {}
        self.JPGlobals       = {}
        self.pythonTypeError = ["object is not subscriptable", \
                                "string indices must be integers", \
                                "list indices must be integers", \
                                "index out of range"]

    def __getFailedJsonDoc(self, jsonDecodeError=None, areaBeforePosition=50, areaAfterPosition=20, oneLine=True):
        failedJsonDoc = None
        if jsonDecodeError is None:
            return failedJsonDoc
        try:
            jsonDoc = jsonDecodeError.doc
        except:
            # 'jsonDecodeError' seems not to be a JSON exception object ('doc' not available)
            return failedJsonDoc
        jsonDocSize     = len(jsonDoc)
        positionOfError = jsonDecodeError.pos
        if areaBeforePosition > positionOfError:
            areaBeforePosition = positionOfError
        if areaAfterPosition > (jsonDocSize - positionOfError):
            areaAfterPosition = jsonDocSize - positionOfError
        failedJsonDoc = jsonDoc[positionOfError-areaBeforePosition:positionOfError+areaAfterPosition]
        failedJsonDoc = f"... {failedJsonDoc} ..."
        if oneLine is True:
            failedJsonDoc = failedJsonDoc.replace("\n", r"\n")
        return failedJsonDoc

    def __reset(self) -> None:
        """
Reset initial variables which are set in constructor method after master JSON file is loaded.
        """
        self.jsonPath        = None
        self.masterFile      = None
        self.handlingFile    = []
        self.lImportedFiles  = []
        self.recursive_level = 0
        self.dUpdatedParams  = {}
        self.lNestedParams   = []
        self.lDotInParamName = []
        self.bDuplicatedKeys = True
        self.jsonCheck       = {}
        self.JPGlobals       = {}

    def __processImportFiles(self, input_data : dict) -> dict:
        """
This is a custom decoder of ``json.loads object_pairs_hook`` function.

This method helps to import JSON files which are provided in ``"[import]"`` keyword into the current json file.

**Arguments:**

* ``input_data``

  / *Condition*: required / *Type*: (* /

  Dictionary from JSON file as input

**Returns:**

* ``out_dict``

  / *Type*: dict /

  Dictionary with resolved content from imported JSON file
        """
        out_dict = {}
        i=1
        for key, value in input_data:
            if re.match('^\s*\[\s*import\s*\]\s*', key.lower()):
                currJsonPath = self.jsonPath
                abs_path_file = CString.NormalizePath(value, sReferencePathAbs = currJsonPath)

                # Use recursive_level and lImportedFiles to avoid cyclic import
                self.recursive_level = self.recursive_level + 1     # increase recursive level

                # length of lImportedFiles should equal to recursive_level
                self.lImportedFiles = self.lImportedFiles[:self.recursive_level] if self.masterFile is not None else \
                                        self.lImportedFiles[:self.recursive_level-1]
                if abs_path_file in self.lImportedFiles:
                    # self.__reset()
                    raise Exception(f"Cyclic imported json file '{abs_path_file}'!")

                oJsonImport = self.jsonLoad(abs_path_file, masterFile=False)
                self.jsonPath = currJsonPath
                tmpOutdict = copy.deepcopy(out_dict)
                for k1, v1 in tmpOutdict.items():
                    for k2, v2 in oJsonImport.items():
                        if k2 == k1:
                            del out_dict[k1]
                del tmpOutdict
                out_dict.update(oJsonImport)

                self.recursive_level = self.recursive_level - 1     # descrease recursive level
            else:
                if self.bDuplicatedKeys:
                    tmpOutdict = copy.deepcopy(out_dict)
                    for k1, v1 in tmpOutdict.items():
                        dReplacements = {"[" : "\[", "]" : "\]", "(" : "\(", ")" : "\)",\
                                         "+" : "\+", "*" : "\*", "?" : "\?", "|" : "\|",\
                                         "\\" : "\\\\", "^" : "\^", "." : "\."}
                        keyPattern = self.__multipleReplace(k1, dReplacements)
                        pattern2 = rf'\${{\s*[^{re.escape(self.specialCharacters)}]*\.*' + keyPattern + r'\s*}$|\[\s*\'' + keyPattern + r'\'\s*\]$'
                        if re.search(pattern2, key, re.UNICODE):
                            bCheck = True
                            dReplacements = {"${" : "", "}" : ""}
                            tmpKey = self.__multipleReplace(key, dReplacements)
                            items = []
                            if "." in tmpKey:
                                items = tmpKey.split(".")
                            elif re.search(rf'\[\'[^{re.escape(self.specialCharacters)}]+\'\]', tmpKey, re.UNICODE):
                                try:
                                    rootKey = re.search(rf'^\s*([^{re.escape(self.specialCharacters)}]+)\[\'.+', tmpKey, re.UNICODE)[1]
                                    items = re.findall(rf'\[\'([^{re.escape(self.specialCharacters)}]+)\'\]', tmpKey, re.UNICODE)
                                    items.insert(0, rootKey)
                                except:
                                    pass
                            sExec = "self.jsonCheck"
                            for item in items:
                                sExec = sExec + f"['{item}']"
                            try:
                                exec(f"dumpData = {sExec}")
                            except:
                                bCheck = False
                                pass
                            if bCheck:
                                key = k1
                        if k1 == key:
                            listKeys = list(out_dict.keys())
                            index = listKeys.index(key)
                            newKey = key + CNameMangling.DUPLICATEDKEY_01.value + str(i)
                            listKeys.insert(index, newKey)
                            tmpDict = {}
                            for k in listKeys:
                                tmpDict[k] = index if k==newKey else out_dict[k]
                            out_dict = tmpDict
                            if isinstance(out_dict[key], list):
                                if out_dict[key][0] != CNameMangling.DUPLICATEDKEY_01.value:
                                    tmpValue = [CNameMangling.DUPLICATEDKEY_01.value, out_dict[key], value]
                                    del out_dict[key]
                                else:
                                    tmpValue = out_dict[key]
                                    tmpValue.append(value)
                                    del out_dict[key]
                            else:
                                tmpValue = [CNameMangling.DUPLICATEDKEY_01.value, out_dict[key], value]
                                del out_dict[key]
                            value = tmpValue
                            out_dict[key] = value
                    del tmpOutdict
                out_dict[key] = value
            i+=1
        return out_dict

    def __loadAndRemoveComments(self, jsonP : str, isFile = True) -> str:
        """
Loads a given json file or json content and filters all C/C++ style comments.

**Arguments:**

* ``jsonP``

  / *Condition*: required / *Type*: str /

  Path of file to be processed or a JSONP content.

* ``isFile``

  / *Condition*: required / *Type*: bool /

  Indicates the jsonP is a path of file or a JSONP content, default value is True.

**Returns:**

* ``sContentCleaned``

  / *Type*: str /

  String version of JSON file after removing all comments.
        """
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return ""
            else:
                return s

        if isFile:
            file=open(jsonP, mode='r', encoding='utf-8')
            sContent=file.read()
            file.close()
        else:
            sContent = jsonP

        pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
        sContentCleaned=re.sub(pattern, replacer, sContent)
        return sContentCleaned

    def __checkParamName(self, sInput: str) -> str:
        """
Checks a parameter name, in case the name is conflict with Python keywords, the temporary prefix
will be added to avoid any potential issues. This temporary prefix is removed when updating returned
Json object.

**Arguments:**

* ``sInput``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``sInput``

  / *Type*: str /
        """
        pattern = rf'\${{\s*([^{re.escape(self.specialCharacters)}]+)\s*}}'
        lParams = re.findall(pattern, sInput, re.UNICODE)
        for param in lParams:
            if "." not in param and param in self.lDataTypes:
                sInput = re.sub(param, CNameMangling.AVOIDDATATYPE.value + param, sInput, count=1)
            if "." in param and CNameMangling.AVOIDDATATYPE.value + param.split('.')[0] in self.JPGlobals.keys():
                sInput = re.sub(param, CNameMangling.AVOIDDATATYPE.value + param, sInput, count=1)
        return sInput
    
    def __multipleReplace(self, sInput : str, dReplacements : str) -> str:
        """
    Replaces multiple parts in a string.

**Arguments:**

* ``sInput``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``sOutput``

  / *Type*: str /

        """
        pattern = re.compile('|'.join(re.escape(key) for key in dReplacements.keys()))
        sOutput = pattern.sub(lambda x: dReplacements[x.group()], sInput)
        return sOutput
    
    def __parseDictPath(self, sInput : str) -> list:
        """
Parse a dictionary path string into a list of its components.

**Arguments:**

* ``sInput``

  / *Condition*: required / *Type*: str /

  The dictionary path string in the format "dictobj['element1']['element2']['element3']".

**Returns:**

* ``lOutput``

  / *Type*: list /

  A list containing the dictionary object and its successive elements.
        """
        lOutput = []
        if not re.search(r"\[.+\]", sInput):
            lOutput.append(sInput)
        else:
            index = sInput.index("[")
            lOutput.append(sInput[:index])
            elements = re.findall(rf"\[\s*('*[^{re.escape(self.specialCharacters)}]+'*)\s*\]", sInput)
            for element in elements:
                lOutput.append(element)
        return lOutput

    def __nestedParamHandler(self, sInputStr : str, bKey = False, bConvertToStr = False):
        """
This method handles nested variables in parameter names or values. Variable syntax is ${Variable_Name}.

**Arguments:**

* ``sInputStr``

  / *Condition*: required / *Type*: str /

  Parameter name or value which contains a nested variable.

**Returns:**

* ``lNestedParam``

  / *Type*: list /

  List of resolved variables which contains in the ``sInputStr``.
        """
        def __getNestedValue(sNestedParam : str):
            dReplacements = {"$${" : "", "}" : ""}
            sParameter = self.__multipleReplace(sNestedParam, dReplacements)
            lElements = self.__parseDictPath(sParameter)
            sExec = "value = self.JPGlobals"
            oTmpObj = self.JPGlobals
            for element in lElements:
                bList = False
                if re.match(r"^[\s\-]*\d+$", element):
                    bList = True
                    sExec = sExec + f"[{element}]"
                elif re.match(rf"^'\s*[^{re.escape(self.specialCharacters)}]+\s*'$", element.strip()):
                    element = element.strip("'")
                if not bList:
                    if isinstance(oTmpObj, dict) and element not in oTmpObj.keys():
                        sDuplicatedCheck = element + CNameMangling.DUPLICATEDKEY_01.value
                        for key in oTmpObj.keys():
                            if sDuplicatedCheck in key and CNameMangling.DUPLICATEDKEY_00.value not in key:
                                element = key                            
                    sExec = sExec + f"['{element}']"
                if not bList and isinstance(oTmpObj, dict):
                    if element in oTmpObj and (isinstance(oTmpObj[element], dict) or \
                                               isinstance(oTmpObj[element], list)):
                        oTmpObj = oTmpObj[element]
                elif bList and isinstance(oTmpObj, list):
                    if int(element)<len(oTmpObj) and (isinstance(oTmpObj[int(element)], dict) or \
                                                      isinstance(oTmpObj[int(element)], list)):
                        oTmpObj = oTmpObj[int(element)]
            try:
                ldict = {}
                exec(sExec, locals(), ldict)
                tmpValue = ldict['value']
            except Exception as error:
                self.__reset()
                errorMsg = ''
                for errorType in self.pythonTypeError:
                    if errorType in str(error):
                        errorMsg = f"Could not resolve expression '{sNestedParam.replace('$$', '$')}'."
                if errorMsg != '':
                    errorMsg = errorMsg + f" Reason: {error}" if ' or slices' not in str(error) else \
                                errorMsg + f" Reason: {str(error).replace(' or slices', '')}"
                else:
                    if isinstance(error, KeyError) and re.search(r"\[\s*" + str(error) + "\s*\]", sNestedParam):
                        errorMsg = f"Could not resolve expression '{sNestedParam.replace('$$', '$')}'. \
Reason: Key error {error}"
                    else:
                        errorMsg = f"The parameter '{sNestedParam.replace('$$', '$')}' is not available!"
                raise Exception(errorMsg)
            if bKey and (isinstance(tmpValue, list) or isinstance(tmpValue, dict)):
                self.__reset()
                errorMsg = f"Found parameter '{sNestedParam.replace('$$', '$')}' of composite data type \
('{sNestedParam.replace('$$', '$')}' is of type {type(tmpValue)}). Because of this expression is the name of a parameter, \
only simple data types are allowed to be substituted inside."
                raise Exception(errorMsg)
            return tmpValue
        
        def __handleDotInNestedParam(sNestedParam : str) -> str:
            ddVar = re.sub(r'\$\${\s*(.*?)\s*}', '\\1', sNestedParam, re.UNICODE)
            lddVar = ddVar.split(".")
            lElements = self.__handleDotdictFormat(lddVar, [])
            sVar = '$${' + lElements[0] + '}'
            lElements.pop(0)
            for item in lElements:
                if re.match(r'^\d+$', item):
                    sVar = sVar + "[" + item + "]"
                elif re.search(r'[{}\[\]\(\)]+', item) and "${" not in item:
                    sVar = sVar + "[" + item + "]"
                else:
                    sVar = sVar + "['" + item + "']"
            return sVar

        pattern = rf'\$\${{\s*[^{re.escape(self.specialCharacters)}]+\s*}}'
        referVars = re.findall("(" + pattern + ")", sInputStr, re.UNICODE)
        # Resolve dotdict in sInputStr
        for var in referVars:
            if var not in sInputStr:
                continue
            if "." in var:
                sVar = __handleDotInNestedParam(var)
                sInputStr = sInputStr.replace(var, sVar)
        tmpPattern = pattern + rf'(\[\s*\d+\s*\]|\[\s*\'[^{re.escape(self.specialCharacters)}]+\'\s*\])*'
        sNestedParam = sInputStr.replace("$$", "$")
        while re.search(tmpPattern, sInputStr, re.UNICODE) and sInputStr.count("$$")>1:
            sLoopCheck = sInputStr
            referVars = re.findall(r'(' + tmpPattern + r')[^\[]', sInputStr, re.UNICODE)
            if len(referVars)==0:
                referVars = re.findall(r'(' + tmpPattern + r')$', sInputStr, re.UNICODE)
            for var in referVars:
                sVar = __handleDotInNestedParam(var[0]) if "." in var[0] else var[0]
                tmpValue = __getNestedValue(sVar)
                if (isinstance(tmpValue, list) or isinstance(tmpValue, dict)) and bConvertToStr:
                    self.__reset()
                    raise Exception(f"The substitution of parameter '{sVar.replace('$$', '$')}' inside the string \
value '{sInputStr.replace('$$', '$')}' is not supported! Composite data types like lists and dictionaries cannot \
be substituted inside strings.")
                while var[0] in sInputStr:
                    sLoopCheck1 = sInputStr
                    dReplacements = {"$" : "\$", "[" : "\[", "]" : "\]"}
                    varPattern = self.__multipleReplace(var[0], dReplacements)
                    if re.search(r"\[['\s]*" + varPattern + r"['\s]*\]", sInputStr):
                        if re.search(r"\[\s*'\s*" + varPattern + r"\s*'\s*\]", sInputStr):
                            sInputStr = re.sub(r"\[\s*'\s*" + varPattern + r"\s*'\s*\]", "['" + str(tmpValue) + "']", sInputStr)
                        elif isinstance(tmpValue, str):
                            sInputStr = re.sub(r"\[['\s]*" + varPattern + r"['\s]*\]", "['" + tmpValue + "']", sInputStr)
                        elif isinstance(tmpValue, int):
                            sInputStr = re.sub(r"\[['\s]*" + varPattern + r"['\s]*\]", "[" + str(tmpValue) + "]", sInputStr)
                        else:
                            sInputStr = sInputStr.replace("$$", "$")
                            var = var[0].replace("$$", "$")
                            errorMsg = f"Invalid index or dictionary key in parameter '{sInputStr}'. The datatype of parameter \
'{var}' has to be 'int' or 'str'."
                            self.__reset()
                            raise Exception(errorMsg)
                    else:
                        if bConvertToStr or sInputStr.count("$${")>1:
                            sInputStr = sInputStr.replace(var[0], str(tmpValue))
                        else:
                            return tmpValue
                    if sInputStr==sLoopCheck1:
                        self.__reset()
                        raise Exception(f"Invalid expression found: '{sNestedParam}'.")
                    elif re.search(r"\[\s*\+*\-+\+*\d+\s*\]", sInputStr):
                        errorMsg = f"Slicing is not supported! Please update the expression '{sNestedParam}'."
                        self.__reset()
                        raise Exception(errorMsg)
            if sInputStr==sLoopCheck:
                self.__checkNestedParam(sInputStr)
                self.__reset()
                raise Exception(f"Invalid expression found: '{sNestedParam}'.")
        if sInputStr.count("$${")==1:
            tmpPattern = pattern + rf'(\[\s*\-*\d+\s*\]|\[[\s\']*[^{re.escape(self.specialCharacters)}]+[\'\s]*\])*'
            if re.match("^" + tmpPattern + "$", sInputStr.strip(), re.UNICODE) and bKey and not bConvertToStr:
                rootVar = re.search(pattern, sInputStr, re.UNICODE)[0]
                sRootVar = __handleDotInNestedParam(rootVar) if "." in rootVar else rootVar
                sInputStr = sInputStr.replace(rootVar, sRootVar)
                dReplacements = {"$${" : "", "}" : ""}
                return self.__multipleReplace(sInputStr, dReplacements)
            var = re.search(tmpPattern, sInputStr, re.UNICODE)
            if var==None:
                sVar = __handleDotInNestedParam(sInputStr) if "." in sInputStr else sInputStr
                sVar = re.sub(r'^\s*\$\${\s*([^}]+)}', "['\\1']", sVar)
                sExec = "value = self.JPGlobals" + sVar
                try:
                    ldict = {}
                    exec(sExec, locals(), ldict)
                    tmpValue = ldict['value']
                except Exception as error:
                    self.__reset()
                    errorMsg = ''
                    for errorType in self.pythonTypeError:
                        if errorType in str(error):
                            errorMsg = f"Could not resolve expression '{sNestedParam.replace('$$', '$')}'."
                    if errorMsg != '':
                        errorMsg = errorMsg + f" Reason: {error}"
                    else:
                        errorMsg = f"The parameter '{sNestedParam.replace('$$', '$')}' is not available!"
                    raise Exception(errorMsg)
                return tmpValue
            else:
                rootVar = re.search(pattern, var[0], re.UNICODE)[0]
                sRootVar = __handleDotInNestedParam(rootVar) if "." in rootVar else rootVar
                sVar = var[0].replace(rootVar, sRootVar)
            tmpValue = __getNestedValue(sVar)
            if bConvertToStr and (isinstance(tmpValue, list) or isinstance(tmpValue, dict)):
                dataType = re.sub(r"^.+'([a-zA-Z]+)'.*$", "\\1", str(type(tmpValue)))
                self.__reset()
                raise Exception(f"The substitution of parameter '{sVar.replace('$$', '$')}' inside the string \
value '{sInputStr.replace('$$', '$')}' is not supported! Composite data types like lists and dictionaries cannot \
be substituted inside strings.")
            if re.match(r"^\s*" + tmpPattern + r"\s*$", sInputStr, re.UNICODE) and not bKey:
                return tmpValue
            else:
                sInputStr = sInputStr.replace(var[0], str(tmpValue))
        return sInputStr.replace("$$", "$") if "$$" in sInputStr else sInputStr

    def __handleDotdictFormat(self, lInputListParams : list, lParams: list = []) -> list:
        """
This method checks the availability of param names contained "." in dotdict format element in JSON config file.

**Arguments:**

* ``lInputListParams``

  / *Condition*: required / *Type*: list /

  List of items separated by "." of dotdict format.

* ``lParams``

  / *Type*: list /

  List of parameter names in dotdict format.

**Returns:**

* ``lParams``

  / *Type*: list /
        """
        checkParam = lInputListParams[0]
        i = 0
        bDotdictParam = False
        for item in lInputListParams:
            if i > 0:
                checkParam = checkParam + '.' + item
                if checkParam in self.lDotInParamName:
                    lParams.append(checkParam)
                    bDotdictParam = True
                    lInputListParams = lInputListParams[i+1:]
                    break
            i+=1
        if not bDotdictParam:
            lParams.append(lInputListParams[0])
            lInputListParams.pop(0)
        if lInputListParams == []:
            return lParams
        else:
            return self.__handleDotdictFormat(lInputListParams, lParams)

    def __checkAndCreateNewElement(self, sKey: str, value, bCheck=False, keyNested=''):
        """
This method checks and creates new elements if they are not already existing.
        """
        lElements = self.__parseDictPath(sKey)
        if len(lElements) == 1:
            return True
        else:
            sExec = "dummyData = self.JPGlobals"
            for element in lElements:
                if re.match(r"^[\s\-]*\d+$", element) or \
                    re.match(rf"^'\s*[^{re.escape(self.specialCharacters)}]+\s*'$", element.strip()):
                    sExec = sExec + f"[{element}]"
                else:
                    sExec = sExec + f"['{element}']"
                try:
                    exec(sExec)
                except Exception as error:
                    if isinstance(error, TypeError): # If Python's type errors occur when executing an expression
                        for eType in self.pythonTypeError:
                            if eType in str(error):
                                if keyNested != '':
                                    errorMsg = f"Could not set parameter '{keyNested}' with value '{value}'! \
Reason: {str(error).replace(' or slices', '')}"
                                else:
                                    errorMsg = f"Could not set parameter '{sKey}' with value '{value}'! \
Reason: {str(error).replace(' or slices', '')}"
                                self.__reset()
                                raise Exception(errorMsg)
                    if bCheck:
                        return False
                    else: # if bCheck flag is False, this function will create a new data structure with default value is empty dict.
                        index = sExec.index("=")
                        sExec1 = sExec[index+1:].strip() + " = {}"
                        try:
                            exec(sExec1)
                        except Exception as error:
                            self.__reset()
                            if keyNested != '':
                                sKey = keyNested
                            errorMsg = f"Could not set parameter '{sKey}' with value '{value}'! Reason: {error}"
                            raise Exception(errorMsg)
            return True

    def __updateAndReplaceNestedParam(self, oJson : dict, bNested : bool = False, recursive : bool = False, \
                                      parentParams : str = '', bDictInList : bool = False):
        """
This method replaces all nested parameters in key and value of a JSON object .

**Arguments:**

* ``oJson``

  / *Condition*: required / *Type*: dict /

  Input JSON object as dictionary. This dictionary will be searched for all ``${variable}`` occurences.
  If found it will be replaced with it's current value.

**Returns:**

* ``oJsonOut``

  / *Type*: dict /

  Output JSON object as dictionary with all variables resolved.
        """
        def __jsonUpdated(k, v, oJson, bNested, keyNested = '', bDuplicatedHandle=False, recursive = False):
            if keyNested != '':
                if not bDuplicatedHandle and keyNested in oJson.keys():
                    del oJson[keyNested]
                rootKey = re.sub(r'\[.*\]', "", k, re.UNICODE)
                if re.search(r'^[0-9]+.*$', rootKey, re.UNICODE):
                    oJson[f"{rootKey}"] = {}
                elif rootKey not in self.JPGlobals.keys():
                    oJson[rootKey] = {}
                    sExec = f"self.JPGlobals['{rootKey}'] = {{}}"
                    try:
                        exec(sExec)
                    except Exception as error:
                        raise Exception(f"Could not set root key element '{rootKey}'! Reason: {error}")
                if re.match(rf"^[^{re.escape(self.specialCharacters)}]+\[.+\]+$", k, re.UNICODE):
                    self.__checkAndCreateNewElement(k, v, keyNested=keyNested)
                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = re.sub(CNameMangling.AVOIDDATATYPE.value, "", k)
                    lElements = self.__parseDictPath(k)
                    sExec = "self.JPGlobals"
                    for element in lElements:
                        if re.match(r"^[\s\-]*\d+$", element) or \
                            re.match(rf"^'\s*[^{re.escape(self.specialCharacters)}]+\s*'$", element.strip()):
                            sExec = sExec + f"[{element}]"
                        else:
                            sExec = sExec + f"['{element}']"
                    sExec = sExec + f" = \"{v}\"" if isinstance(v, str) else sExec + f" = {str(v)}"
                    try:
                        exec(sExec)
                    except Exception as error:
                        self.__reset()
                        errorMsg = f"Could not set parameter '{keyNested}' with value '{v}'! Reason: {error}"
                        raise Exception(errorMsg)
                    if not recursive:
                        oJson[rootKey] = self.JPGlobals[rootKey]
                else:
                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = re.sub(CNameMangling.AVOIDDATATYPE.value, "", k)
                    oJson[k] = v
                    if not recursive:
                        self.JPGlobals.update({k:v})

            else:
                if bNested:
                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = re.sub(CNameMangling.AVOIDDATATYPE.value, "", k) 
                oJson[k] = v
                if not recursive:
                    self.JPGlobals.update({k:v})

        def __loadNestedValue(initValue: str, sInputStr: str, bKey=False, key=''):
            varPattern = rf"[^{re.escape(self.specialCharacters)}]*"
            indexPattern = r"\[[\s\-\+\d]*\]"
            dictPattern = r"(\[+\s*'[^\$\[\]\(\)]+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${\s*" + varPattern + r"\s*}.*\]+)*|" + indexPattern
            pattern = r"\${\s*" + varPattern + r"(\.*\${\s*" + varPattern + r"\s*})*" + dictPattern
            bValueConvertString = False
            if CNameMangling.STRINGCONVERT.value in sInputStr:
                bValueConvertString = True
                sInputStr = sInputStr.replace(CNameMangling.STRINGCONVERT.value, '')
                sInputStr = re.sub("\$", "$$", sInputStr)
                initValue = initValue.replace(CNameMangling.STRINGCONVERT.value, '')
            elif re.match(r"^\s*" + pattern + r"\s*$", sInputStr, re.UNICODE):
                sInputStr = re.sub("\$", "$$", sInputStr)
            sInputStr = self.__checkParamName(sInputStr)
            handledValue = self.__nestedParamHandler(sInputStr) if not bValueConvertString else \
                                    self.__nestedParamHandler(sInputStr, bKey=bKey, bConvertToStr=bValueConvertString)
            if bValueConvertString and not isinstance(handledValue, str):
                handledValue = str(handledValue)
            return handledValue

        def __handleList(lInput : list, bNested : bool) -> list:
            tmpValue = []
            for item in lInput:
                if isinstance(item, str) and re.search(pattern, item, re.UNICODE):
                    bNested = True
                    initItem = item
                    while isinstance(item, str) and "${" in item:
                        sLoopCheck = item
                        item = __loadNestedValue(initItem, item)
                        if item==sLoopCheck:
                            self.__reset()
                            raise Exception(f"Invalid expression found: '{initItem}'.")
                elif isinstance(item, list) and "${" in str(item):
                    item = __handleList(item, bNested)
                elif isinstance(item, dict):
                    tmpItem = copy.deepcopy(item)
                    for key, value in tmpItem.items():
                        if isinstance(value, list) and value[0]==CNameMangling.DUPLICATEDKEY_01.value:
                            item[key] = value[-1]
                        if CNameMangling.DUPLICATEDKEY_01.value in key:
                            item.pop(key)
                    del tmpItem
                    if "${" in str(item):
                        item, bNested = self.__updateAndReplaceNestedParam(item, bNested, recursive=True, bDictInList=True)
                tmpValue.append(item)
            return tmpValue

        if bool(self.currentCfg) and not recursive:
            for k, v in self.currentCfg.items():
                if k in self.lDataTypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                self.JPGlobals.update({k:v})

        tmpJson = copy.deepcopy(oJson)
        sepecialCharacters = r'!@#%^&*()+=[\]|;:\'",<>?/`~'
        pattern = rf"\${{\s*[^{re.escape(sepecialCharacters)}]+\s*}}"
        pattern = pattern + r"(\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${.+\s*\]+)*"
        for k, v in tmpJson.items():
            if "${" not in k and CNameMangling.DUPLICATEDKEY_01.value not in k:
                parentParams = k if parentParams=='' else parentParams + "['" + k + "']"
            keyNested = ''
            origKey = ''
            bStrConvert = False
            bImplicitCreation = False
            bDuplicatedHandle = False
            if re.match(r"^.+" + CNameMangling.DUPLICATEDKEY_01.value + r"\d+$", k, re.UNICODE):
                bDuplicatedHandle = True
                dupKey = k
                if CNameMangling.DUPLICATEDKEY_00.value in k:
                    origKey = re.sub(CNameMangling.DUPLICATEDKEY_01.value + r"\d+$", "", k)
                    if not re.match(r'^\s*' + pattern + r'\s*$', origKey):
                        oJson = self.__changeDictKey(oJson, k, origKey)
                    else:
                        del oJson[k]
                    k = origKey
                else:
                    del oJson[k]
                    k = re.sub(CNameMangling.DUPLICATEDKEY_01.value + r"\d+$", "", k)
            if CNameMangling.STRINGCONVERT.value in k:
                bStrConvert = True
                del oJson[k]
                keyNested = k.replace(CNameMangling.STRINGCONVERT.value, '')
                oJson[keyNested] = v
                bNested = True
                while "${" in k:
                    sLoopCheck = k
                    k = __loadNestedValue(keyNested, k, bKey=True, key=keyNested)
                    if k == sLoopCheck:
                        self.__reset()
                        raise Exception(f"Invalid expression found: '{keyNested}'.")
            elif re.match(r"^\s*" + pattern + r"\s*$", k, re.UNICODE):
                bCheckDynamicKey = False
                keyNested = k
                if k.count("${")>1 and re.match(r'^\s*"*\s*' + pattern + r'\s*"*\s*$', k, re.UNICODE):
                    bCheckDynamicKey = True
                if re.search(r"\[\s*'*" + pattern + r"'*\s*\]", keyNested, re.UNICODE) or \
                    re.search(r"\." + pattern + r"[\.}]+", keyNested, re.UNICODE):
                    bImplicitCreation = True
                k = re.sub("\$", "$$", k)
                k = self.__checkParamName(k)
                k = self.__nestedParamHandler(k, bKey=True)
                sExec = 'dummyData = self.JPGlobals' if not bDictInList else 'dummyData = oJson'
                # Check digits inside a square brackets indicating a key name of a dict or index of a list
                while re.search(r'\[\d+\]', k):
                    tmpK = re.sub(r'\[\d+\].*$', '', k)
                    tmpK = re.sub(r'_listIndex_', '', tmpK)
                    sTmpExec = sExec + re.sub(r'^\s*([^\[]+)', "['\\1']", parentParams) + \
                                    re.sub(r'^\s*([^\[]+)', "['\\1']", tmpK)
                    try:
                        ldict = {}
                        exec(sTmpExec, locals(), ldict)
                    except:
                        pass
                    if len(ldict)>0 and isinstance(ldict['dummyData'], dict):
                        k = re.sub(r'\[(\d+)\]', "['\\1']", k, count=1) # if it a key name, put inside single quotes
                    else:
                        k = re.sub(r'\[(\d+)\]', "[\\1_listIndex_]", k, count=1) # add temporary suffix to the index due to while condition
                if '_listIndex_' in k:
                    k = re.sub(r'_listIndex_', '', k)
                dReplacements = {"[":"\[", "]":"\]", ".":"\.", "-":"\-"}
                tmpPattern = self.__multipleReplace(parentParams, dReplacements)
                if (parentParams != '' and not re.match(r'^'+tmpPattern+r'.+$', k)) or bDictInList:
                    tmpParam = re.sub(r'^\s*([^\[]+)', "${\\1}", parentParams) + re.sub(r'^\s*([^\[]+)', "['\\1']", k)
                    sExec = sExec + re.sub(r'^\s*([^\[]+)', "['\\1']", parentParams) + \
                                    re.sub(r'^\s*([^\[]+)\[*.*$', "['\\1']", k)
                    k = parentParams + re.sub(r'^\s*([^\[]+)', "['\\1']", k) # Update absolute path of nested key
                    try:
                        exec(sExec)
                    except:
                        self.__reset()
                        raise Exception(f"A key with name '{keyNested}' does not exist at this position. \
Use the '<name> : <value>' syntax to create a new key.")
                elif bCheckDynamicKey:
                    sExec = sExec + re.sub(r'^\s*([^\[]+)', "['\\1']", parentParams) + \
                                    re.sub(r'^\s*([^\[]+)', "['\\1']", k)
                    try:
                        exec(sExec)
                    except Exception as error:
                        if isinstance(error, KeyError):
                            self.__reset()
                            raise Exception(f"Identified dynamic name of key '{keyNested}' that does not exist. But new keys can \
only be created based on hard code names.")
                        else:
                            pass
                if bImplicitCreation and not self.__checkAndCreateNewElement(k, v, bCheck=True, keyNested=keyNested):
                    self.__reset()
                    raise Exception(f"The implicit creation of data structures based on parameters is not supported \
(affected expression: '{keyNested}').")
            if isinstance(v, dict):
                v, bNested = self.__updateAndReplaceNestedParam(v, bNested, recursive=True, parentParams=parentParams)
            elif isinstance(v, list):
                v = __handleList(v, bNested)
            elif isinstance(v, str) and self.__checkNestedParam(v):
                if re.search(pattern, v, re.UNICODE):
                    bNested = True
                    initValue = v
                    while isinstance(v, str) and "${" in v:
                        sLoopCheck = v
                        v = __loadNestedValue(initValue, v)
                        if v == sLoopCheck:
                            self.__reset()
                            raise Exception(f"Invalid expression found: '{initValue}'.")
                    if isinstance(v, str) and re.search(r'\[[^\]]+\]', v):
                        sExec = 'value = ' + v
                        try:
                            ldict = {}
                            exec(sExec, locals(), ldict)
                            v = ldict['value']
                        except:
                            pass
            if bDuplicatedHandle:
                if "${" not in dupKey and parentParams != "":
                    sParams = parentParams + "['" + k + "']"
                    lElements = self.__parseDictPath(sParams)
                    sExec = "self.JPGlobals"
                    for element in lElements:
                        if re.match(r"^[\s\-]*\d+$", element) or \
                            re.match(rf"^'\s*[^{re.escape(self.specialCharacters)}]+\s*'$", element.strip()):
                            sExec = sExec + f"[{element}]"
                        else:
                            sExec = sExec + f"['{element}']"
                    sExec = sExec + f" = \"{v}\"" if isinstance(v, str) else sExec + f" = {str(v)}"
                else:
                    lElements = self.__parseDictPath(k)
                    sExec = "self.JPGlobals"
                    dCheck = self.JPGlobals
                    for element in lElements:
                        if (isinstance(dCheck, dict) or isinstance(dCheck, list)) and element not in dCheck:
                            dCheck[element.strip("'")] = {}
                        if re.match(r"^[\s\-]*\d+$", element) or \
                            re.match(rf"^'\s*[^{re.escape(self.specialCharacters)}]+\s*'$", element.strip()):
                            sExec = sExec + f"[{element}]"
                        else:
                            sExec = sExec + f"['{element}']"
                        dCheck = dCheck[element.strip("'")]
                    sExec = sExec + f" = \"{v}\"" if isinstance(v, str) else sExec + f" = {str(v)}"
                try:
                    exec(sExec)
                except:
                    pass
                if origKey == '':
                    continue
                
            __jsonUpdated(k, v, oJson, bNested, keyNested, bDuplicatedHandle, recursive)
            if keyNested != '' and not bStrConvert:
                transTable = str.maketrans({"[":"\[", "]":"\]"})
                tmpList = []
                for key in self.dUpdatedParams:
                    if re.match(r"^" + k.translate(transTable) + r"\['.+$", key, re.UNICODE):
                        tmpList.append(key)
                for item in tmpList:
                    self.dUpdatedParams.pop(item)
                if CNameMangling.DUPLICATEDKEY_01.value not in k:
                    self.dUpdatedParams.update({k:v})
            dReplacements = {"[" : "\[", "]" : "\]", "(" : "\(", ")" : "\)",\
                                "+" : "\+", "*" : "\*", "?" : "\?", "|" : "\|",\
                                "\\" : "\\\\", "^" : "\^", "." : "\."}
            keyPattern = self.__multipleReplace(k, dReplacements)
            if re.match(r"^.+\['" + keyPattern + r"'\]$", parentParams, re.UNICODE):
                parentParams = re.sub("\['" + k + "'\]", "", parentParams)
            if not recursive:
                parentParams = ''
        del tmpJson
        return oJson, bNested

    def __checkDotInParamName(self, oJson : dict):
        """
This is recrusive funtion collects all parameters which contain "." in the name.

**Arguments:**

* ``oJson``

  / *Condition*: required / *Type*: dict /

  Json object which want to collect all parameter's name contained "."

**Returns:**

  *no return values*
        """
        for k, v in oJson.items():
            if "." in k and k not in self.lDotInParamName:
                self.lDotInParamName.append(k)
            if isinstance(v, dict):
                self.__checkDotInParamName(v)

    def __checkNestedParam(self, sInput : str, bKey=False) -> bool:
        """
Checks nested parameter format.

**Arguments:**

* ``sInput``

  / *Condition*: required / *Type*: str /

**Returns:**

  *raise exception if nested parameter format invalid*
        """
        pattern = rf"^\${{\s*[^{re.escape(self.specialCharacters)}]+\s*}}(\[.*\])+$"
        pattern1 = rf"\${{.+}}(\[.+\])*[^\[]*\${{"
        pattern2 = r"\[[a-zA-Z0-9\.\-\+\${}'\s]*:[a-zA-Z0-9\.\-\+\${}'\s]*\]" # Slicing pattern
        # Checks special character in parameters
        sTmpInput = sInput
        bSpecialCharInParam = False
        while sTmpInput.count("${") > 1:
            lParams = re.findall(r'\${([^\$}]*)}', sTmpInput)
            for param in lParams:
                if param.strip()=='' or re.search(r'[!@#\$%\^&\*\(\)=\[\]{}|;:\s\+\'",<>?/`~]', param) or \
                                        re.match(r'^\s*\-+.*\s*$', param) or re.match(r'^\s*[^\-]*\-+\s*$', param):
                    bSpecialCharInParam = True
                    break
                sTmpInput = sTmpInput.replace('${' + param + '}', '')
            if bSpecialCharInParam:
                break
        if "${" not in sInput:
            return True
        if re.search(rf"\${{\s*[^{re.escape(self.specialCharacters)}]+\['*.+'*\].*}}", sInput, re.UNICODE):
            if CNameMangling.STRINGCONVERT.value in sInput:
                sInput = sInput.replace(CNameMangling.STRINGCONVERT.value, "")
            errorMsg = f"Invalid syntax: Found index or sub-element inside curly brackets in the parameter '{sInput}'"
            self.__reset()
            raise Exception(errorMsg)
        elif re.search(r"\[[0-9\s]*[A-Za-z_]+[0-9\s]*\]", sInput, re.UNICODE):
            invalidElem = re.search(r"\[[0-9\s]*[A-Za-z_]+[0-9\s]*\]", sInput, re.UNICODE)[0]
            errorMsg = f"Invalid syntax! Sub-element '{invalidElem}' in {sInput.replace(CNameMangling.STRINGCONVERT.value, '').strip()} \
has to enclosed in quotes."
            self.__reset()
            raise Exception(errorMsg)
        elif re.search(r'\[[!@#\$%\^&\*\(\)=\[\]|;\s\-\+\'",<>?/`~]*\]', sInput):
            if CNameMangling.STRINGCONVERT.value not in sInput or \
                re.match(pattern, sInput.replace(CNameMangling.STRINGCONVERT.value, "")):
                errorMsg = f"Expression '{sInput.replace(CNameMangling.STRINGCONVERT.value, '')}' cannot be evaluated. \
Reason: A pair of square brackets is empty or contains not allowed characters."
                self.__reset()
                raise Exception(errorMsg)
            else:
                return True
        elif bSpecialCharInParam:
            if CNameMangling.STRINGCONVERT.value not in sInput:
                errorMsg = f"Expression '{sInput.replace(CNameMangling.STRINGCONVERT.value, '')}' cannot be evaluated. \
Reason: A pair of curly brackets is empty or contains not allowed characters."
                self.__reset()
                raise Exception(errorMsg)
            else:
                return True
        elif re.search(pattern2, sInput) or re.search(r"\[\s*\-\s*\d+\s*\]", sInput):
            if CNameMangling.STRINGCONVERT.value in sInput:
                sInput = sInput.replace(CNameMangling.STRINGCONVERT.value, '')
            errorMsg = f"Slicing is not supported! Please update the expression '{sInput}'."
            self.__reset()
            raise Exception(errorMsg)
        elif CNameMangling.STRINGCONVERT.value in sInput:
            if sInput.count("${") > sInput.count("}"):
                sInput = re.sub(CNameMangling.STRINGCONVERT.value, "", sInput)
                errorMsg = f"Invalid syntax! One or more than one opened or closed curly bracket is missing in expression '{sInput.strip()}'."
                self.__reset()
                raise Exception(errorMsg)
            else:
                return True
        elif re.match(r"^[\s\"]*\${[^!@#%\^&\*\(\)=|;,<>?/`~]+[\s\"]*$", sInput) and \
            sInput.count("${") > sInput.count("}"):
            errorMsg = f"Invalid parameter format: {sInput.strip()} - Closed curly bracket is missing."
            self.__reset()
            raise Exception(errorMsg)
        elif CNameMangling.STRINGCONVERT.value not in sInput and \
            CNameMangling.DUPLICATEDKEY_01.value not in sInput:
            if not re.match(r"^\${.+[}\]]+$", sInput) or (re.search(pattern1, sInput) and not bKey):
                sTmpInput = re.sub(r"(\.\${[a-zA-Z0-9\.\_]+}(\[[^\[]+\])*)", "", sInput)
                if not re.match(r"^\s*\${[a-zA-Z0-9\.\_]+}(\[[^\[]+\])*\s*$", sTmpInput):
                    errorMsg = f"Invalid parameter format: {sInput} - The double quotes are missing!!!"
                else:
                    return True
            else:
                if sInput.count("${") != sInput.count("}") or sInput.count("[") != sInput.count("]"):
                    errorMsg = f"Invalid parameter format: {sInput.strip()} - The brackets mismatch!!!"
                else:
                    return True
            self.__reset()
            raise Exception(errorMsg)
        else:
            return True
        
    def __changeDictKey(self, dInput : dict, sOldKey : str, sNewKey : str) -> dict:
        """
Replace an existing key in a dictionary with a new key name. The replacement is done by preserving the original order of the keys.

**Arguments:**

* ``dInput``

  / *Condition*: required / *Type*: dict /

* ``sOldKey``

  / *Condition*: required / *Type*: str /

* ``sNewKey``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``dOutput``

  / *Type*: dict /
        """
        listKeys = list(dInput.keys())
        index = listKeys.index(sOldKey)
        listKeys.insert(index, sNewKey)
        listKeys.pop(index + 1)
        dOutput = {}
        for key in listKeys:
            dOutput[key] = dInput[sOldKey] if key==sNewKey else dInput[key]
        return dOutput
    
    def __keyNameValidation(self, sInput):
        """
Validates the key names of a JSON object to ensure they adhere to certain rules and conventions.

**Arguments:**

* ``sInput``

  / *Condition*: required / *Type*: str /

**Returns:**

  *No return value*
        """
        if CNameMangling.STRINGCONVERT.value in sInput:
            sInput = sInput.replace(CNameMangling.STRINGCONVERT.value, '')
            errorMsg = f"A substitution in key names is not allowed! Please update the key name {sInput}"
            self.__reset()
            raise Exception(errorMsg)

    def jsonLoad(self, jFile : str, masterFile : bool = True):
        """
This method is the entry point of JsonPreprocessor.

``jsonLoad`` loads the JSON file, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``jFile``

  / *Condition*: required / *Type*: str /

  Path and name of main JSON file. The path can be absolute or relative and is also allowed to contain environment variables.

* ``masterFile``

  / *Condition*: required / *Type*: bool /

  Identifies the entry level when loading JSONP file in comparison with imported files levels. Default value is True

**Returns:**

* ``oJson``

  / *Type*: dict /

  Preprocessed JSON file(s) as Python dictionary
        """
        jFile = CString.NormalizePath(jFile, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        self.handlingFile.append(jFile)
        if masterFile:
            self.masterFile = jFile
        if  not(os.path.isfile(jFile)):
            self.__reset()
            raise Exception(f"File '{jFile}' is not existing!")

        self.lImportedFiles.append(jFile)
        self.jsonPath = os.path.dirname(jFile)
        try:
            sJsonData= self.__loadAndRemoveComments(jFile)
        except Exception as reason:
            self.__reset()
            raise Exception(f"Could not read json file '{jFile}' due to: '{reason}'!")
        return self.jsonLoads(sJsonData, firstLevel=masterFile)

    def jsonLoads(self, sJsonpContent : str, referenceDir : str = '', firstLevel : bool = True):
        """
``jsonLoads`` loads the JSONP content, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``sJsonpContent``

  / *Condition*: required / *Type*: str /

  The JSONP content.

* ``referenceDir``

  / *Condition*: required / *Type*: str /

  A reference path for loading imported files.

* ``firstLevel``

  / *Condition*: required / *Type*: bool /

  Identifies the entry level when loading JSONP content in comparison with imported files levels.

**Returns:**

* ``oJson``

  / *Type*: dict /

  Preprocessed JSON content as Python dictionary
        """
        def __handleDuplicatedKey(dInput : dict) -> dict:
            listKeys = list(dInput.keys())
            dictValues = {}
            for key in listKeys:
                if CNameMangling.DUPLICATEDKEY_01.value in key:
                    origKey = re.sub(CNameMangling.DUPLICATEDKEY_01.value + "\d+\s*$", "", key)
                    dictValues[origKey] = copy.deepcopy(dInput[origKey])
            for key in dictValues.keys():
                dInput = self.__changeDictKey(dInput, key, key + CNameMangling.DUPLICATEDKEY_01.value + "00")
            tmpDict = copy.deepcopy(dInput)
            for k, v in tmpDict.items():
                if CNameMangling.DUPLICATEDKEY_01.value in k:
                    origK = re.sub(CNameMangling.DUPLICATEDKEY_01.value + "\d+\s*$", "", k)
                    dInput[k] = dictValues[origK].pop(1)
                if isinstance(v, list) and v[0]==CNameMangling.DUPLICATEDKEY_01.value:
                    v = v[-1]
                    dInput[k] = v
                if isinstance(v, dict):
                    dInput[k] = __handleDuplicatedKey(v)
            del tmpDict
            del dictValues
            return dInput
        
        def __removeDuplicatedKey(dInput : dict) -> dict:
            if isinstance(dInput, dict):
                for k, v in list(dInput.items()):
                    __removeDuplicatedKey(v)
            elif isinstance(dInput, list):
                for item in dInput:
                    __removeDuplicatedKey(item)

        def __checkKeynameFormat(oJson : dict):
            """
This function checks key names in JSON configuration files.
            """
            for k, v in oJson.items():
                if "${" in k:
                    self.__checkNestedParam(k, bKey=True)
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, str) and "${" in item:
                            self.__checkNestedParam(item)
                elif isinstance(v, dict):
                    __checkKeynameFormat(v)
        
        def __handleLastElement(sInput : str) -> str:
            '''
This function handle a last element of a list or dictionary
            '''
            param = re.search(r'(' + nestedPattern + r')', sInput)
            if param is not None and re.match(r'^[\s\[\]{}]*$', sInput.replace(param[0], '')):
                sParam = param[0]
                if sParam.count('[')<sParam.count(']'):
                    while re.search(r'\[[^\]]+\]', sParam):
                        sParam = re.sub(r'\[[^\]]+\]', '', sParam)
                    while re.search(r'\${[^}]+}', sParam):
                        sParam = re.sub(r'\${[^}]+}', '', sParam)
                    index = len(sParam)
                    sParam = param[0]
                    sParam = sParam[:-index]
                dReplacements = {"$":"\$", "[":"\[", "]":"\]", ".":"\.", "-":"\-", "+":"\+"}
                tmpPattern = self.__multipleReplace(sParam, dReplacements)
                sInput = re.sub(r'(' + tmpPattern + r')', '"\\1"', sInput)
            else:
                sParam = re.findall(r'^[{\[\s*]*(.+)$', sInput.strip())[0]
                sInput = sInput.replace(sParam, '"' + sParam + '"')
            return sInput

        if referenceDir != '':
            self.jsonPath = CString.NormalizePath(referenceDir, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
            if not os.path.exists(self.jsonPath):
                self.__reset()
                raise Exception(f"Reference directory '{referenceDir}' is not existing!")
        if self.masterFile is None or not firstLevel:
            try:
                sJsonData= self.__loadAndRemoveComments(sJsonpContent, isFile=False)
            except Exception as reason:
                self.__reset()
                raise Exception(f"Could not read JSONP content due to: '{reason}'!")
        else:
            sJsonData = sJsonpContent
        sJsonDataUpdated = ""
        for line in sJsonData.splitlines():
            if line == '' or line.isspace():
                continue
            try:
                listDummy = shlex.split(line)
            except Exception as error:
                self.__reset()
                raise Exception(f"\n{str(error)} in line: '{line}'")

            if "${" in line:
                curLine = line
                lNestedVar = re.findall(rf"\${{\s*([^{re.escape(self.specialCharacters)}]+)\s*}}", line, re.UNICODE)
                for nestedVar in lNestedVar:
                    if nestedVar[0].isdigit():
                        self.__reset()
                        raise Exception(f"Invalid parameter format in line: {line.strip()}")
                tmpList01 = re.findall(r"(\"[^\"]+\")", line)
                line = re.sub(r"(\"[^\"]+\")", CNameMangling.COLONS.value, line)
                slicingPattern = r"\[[a-zA-Z0-9\.\-\+\${}'\s]*:[a-zA-Z0-9\.\-\+\${}'\s]*\]"
                tmpList02 = re.findall(slicingPattern, line)
                line = re.sub(slicingPattern, CNameMangling.SLICEINDEX.value, line)
                indexPattern = r"\[[\s\-\+\d]*\]"
                if re.search(indexPattern, line):
                    indexList = re.findall(indexPattern, line)
                    line = re.sub("(" + indexPattern + ")", CNameMangling.LISTINDEX.value, line)
                items = re.split("\s*:\s*", line)
                iItems = len(items)-1 if items[-1]=='' else len(items) 
                newLine = ''
                preItem = ''
                i=1
                for item in items:
                    if CNameMangling.COLONS.value in item:
                        while CNameMangling.COLONS.value in item:
                            item = item.replace(CNameMangling.COLONS.value, tmpList01.pop(0), 1)
                    elif CNameMangling.LISTINDEX.value in item:
                        while CNameMangling.LISTINDEX.value in item:
                            item = item.replace(CNameMangling.LISTINDEX.value, indexList.pop(0), 1)
                    elif CNameMangling.SLICEINDEX.value in item:
                        while CNameMangling.SLICEINDEX.value in item:
                            item = item.replace(CNameMangling.SLICEINDEX.value, tmpList02.pop(0), 1)
                    curItem = item
                    if "${" in item:
                        variablePattern = rf"[^{re.escape(self.specialCharacters)}]+"
                        indexPattern = r"\[[\s\-\+\d]*\]|\[.*:.*\]"
                        dictPattern = r"\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${\s*" + variablePattern + r"\s*}.*\]+|" + indexPattern
                        nestedPattern = r"\${\s*" + variablePattern + r"(\.*\${\s*" + variablePattern + r"\s*})*" + r"\s*}(" + dictPattern + r")*"
                        bHandle = False
                        if '"' in item and item.count('"')%2==0:
                            tmpList = re.findall(r'"[^"]+"', item)
                            item = re.sub(r'"[^"]+"', CNameMangling.STRINGVALUE.value, item)
                        if re.search(r'[\(\)\!@#%\^\&\/\\\=`~\?]+', item):
                            item = re.sub(r'^\s*(.+)\s*,*', '"\\1"', item)
                            bHandle = True
                        if "," in item and not bHandle:
                            if item.count(',')>1 and not re.match(r'^\[|{.+$', item.strip()):
                                dReplacements = {"$":"\$", "[":"\[", "]":"\]", ".":"\.", "-":"\-", "+":"\+"}
                                tmpPattern1 = self.__multipleReplace(preItem, dReplacements)
                                tmpPattern2 = self.__multipleReplace(curItem, dReplacements)
                                if re.search(tmpPattern1 + '\s*:\s*' + tmpPattern2, curLine):
                                    item = re.sub(r'^\s*(.+)\s*', '"\\1"', item)
                                    bHandle = True
                            if not bHandle:
                                subItems = item.split(',')
                                iSubItems = len(subItems) -1 if subItems[-1]=='' else len(subItems)
                                newSubItem = ""
                                j=1
                                for subItem in subItems:
                                    if "${" in subItem:
                                        if iSubItems>1 and j<iSubItems:
                                            if subItem.count("${") < subItem.count("}") or subItem.count("[") < subItem.count("]"):
                                                subItem = __handleLastElement(subItem)
                                            elif re.match(r'^\${.+$', subItem.strip()):
                                                subItem = '"' + subItem.strip() + '"'
                                            else:
                                                subItem = re.sub(r'(\${.+$)', '"\\1"', subItem.strip())
                                        else:
                                            subItem = __handleLastElement(subItem)   
                                    if j < iSubItems:
                                        newSubItem = newSubItem + subItem + ', '
                                    else:
                                        newSubItem = newSubItem + subItem + ',' if subItem=='' else newSubItem + subItem
                                    j+=1
                                item = newSubItem
                        else:
                            if "${" in item and not bHandle:
                                item = __handleLastElement(item)
                        while CNameMangling.STRINGVALUE.value in item:
                            if "${" in tmpList[0]:
                                sValue = tmpList.pop(0)
                                sValue = re.sub(r'(' + nestedPattern + r')', '\\1' + CNameMangling.STRINGCONVERT.value, sValue)
                                item = item.replace(CNameMangling.STRINGVALUE.value, sValue, 1)
                            else:
                                item = item.replace(CNameMangling.STRINGVALUE.value, tmpList.pop(0), 1)
                    if i<iItems:
                        newLine = newLine + item + " : "
                    else:
                        newLine = newLine + item + " :" if item=='' else newLine + item
                    preItem = curItem
                    i+=1
                for nestedParam in self.lNestedParams:
                    dReplacements = {"$" : "\$", "[" : "\[", "]" : "\]"}
                    tmpNestedParam = self.__multipleReplace(nestedParam, dReplacements)
                    if re.search(r"(\s*\"str\(" + tmpNestedParam + "\)\"\s*:)", newLine.replace(CNameMangling.STRINGCONVERT.value, '')) \
                        or re.search(r"(\s*\"" + tmpNestedParam + r"\"\s*:)", newLine.replace(CNameMangling.STRINGCONVERT.value, '')):
                        self.lNestedParams.remove(nestedParam)
                if re.search(r"\[\s*\+\s*\d+\s*\]", newLine):
                    newLine = re.sub(r"\[\s*\+\s*(\d+)\s*\]", "[\\1]", newLine)
                sJsonDataUpdated = sJsonDataUpdated + newLine + "\n"
            else:
                sJsonDataUpdated = sJsonDataUpdated + line + "\n"
        lKeyName = re.findall(r'("[^:"]+")\s*:\s*', sJsonDataUpdated)
        for key in lKeyName:
            keyDecode = bytes(key, 'utf-8').decode('unicode_escape')
            self.__keyNameValidation(keyDecode)
        CJSONDecoder = None
        if self.syntax != CSyntaxType.json:
            if self.syntax == CSyntaxType.python:
                CJSONDecoder = CPythonJSONDecoder
            else:
                self.__reset()
                raise Exception(f"Provided syntax '{self.syntax}' is not supported.")
        # Load the temporary Json object without checking duplicated keys for 
        # verifying duplicated keys later.
        if firstLevel:
            self.bDuplicatedKeys = False
            try:
                self.jsonCheck = json.loads(sJsonDataUpdated,
                                cls=CJSONDecoder,
                                object_pairs_hook=self.__processImportFiles)
            except Exception as error:
                failedJsonDoc = self.__getFailedJsonDoc(error)
                jsonException = "not defined"
                if failedJsonDoc is None:
                    jsonException = f"{error}\nIn file: '{self.handlingFile.pop(-1)}'" if len(self.handlingFile)>0 else f"{error}"
                else:
                    jsonException = f"{error}\nNearby: '{failedJsonDoc}'\nIn file: '{self.handlingFile.pop(-1)}'" if len(self.handlingFile)>0 else \
                                    f"{error}\nNearby: '{failedJsonDoc}'"
                self.__reset()
                raise Exception(jsonException)
            self.bDuplicatedKeys = True

        # Load Json object with checking duplicated keys feature is enabled.
        # The duplicated keys feature uses the self.jsonCheck object to check duplicated keys. 
        try:
            oJson = json.loads(sJsonDataUpdated,
                               cls=CJSONDecoder,
                               object_pairs_hook=self.__processImportFiles)
        except Exception as error:
            failedJsonDoc = self.__getFailedJsonDoc(error)
            jsonException = "not defined"
            if failedJsonDoc is None:
                jsonException = f"{error}\nIn file: '{self.handlingFile.pop(-1)}'" if len(self.handlingFile)>0 else f"{error}"
            else:
                jsonException = f"{error}\nNearby: '{failedJsonDoc}'\nIn file: '{self.handlingFile.pop(-1)}'" if len(self.handlingFile)>0 else \
                                f"{error}\nNearby: '{failedJsonDoc}'"
            if firstLevel:
                self.__reset()
            raise Exception(jsonException)

        self.__checkDotInParamName(oJson)
        __checkKeynameFormat(oJson)

        if firstLevel:
            oJson = __handleDuplicatedKey(oJson)
            for k, v in oJson.items():
                if re.match(r"^[0-9]+.*$", k) or re.match(r"^[\s\"]*\${.+}[\s\"]*$", k) \
                    or CNameMangling.DUPLICATEDKEY_01.value in k:
                    continue
                if k in self.lDataTypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                self.JPGlobals.update({k:v})
            oJson, bNested = self.__updateAndReplaceNestedParam(oJson)
            self.jsonCheck = {}
            for k, v in self.dUpdatedParams.items():
                if '[' in k:
                    rootElement = k.split('[', 1)[0]
                    if rootElement in oJson:
                        self.__checkAndCreateNewElement(k, v)
                        sExec = "oJson['" + rootElement + "'] = " + rootElement
                        try:
                            exec(sExec)
                        except:
                            pass
                    if isinstance(v, str):
                        sExec = "oJson['" + k.split('[', 1)[0] + "'][" + k.split('[', 1)[1] + " = \"" + v + "\""
                    else:
                        sExec = "oJson['" + k.split('[', 1)[0] + "'][" + k.split('[', 1)[1] + " = " + str(v)
                else:
                    if isinstance(v, str):
                        sExec = "oJson['" + k + "'] = \"" + v + "\""
                    else:
                        sExec = "oJson['" + k + "'] = " + str(v)
                try:
                    exec(sExec)
                except:
                    pass
                
            self.__reset()
            __removeDuplicatedKey(oJson)
            oJson = DotDict(oJson)
        return oJson

    def jsonDump(self, oJson : dict, outFile : str) -> str:
        """
This method writes the content of a Python dictionary to a file in JSON format and returns a normalized path to this JSON file.

**Arguments:**

* ``oJson``

  / *Condition*: required / *Type*: dict /

* ``outFile`` (*string*)

  / *Condition*: required / *Type*: str /

  Path and name of the JSON output file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

* ``outFile`` (*string*)

  / *Type*: str /

  Normalized path and name of the JSON output file.
        """
        outFile = CString.NormalizePath(outFile, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        jsonObject = json.dumps(oJson, ensure_ascii=False, indent=4)
        try:
            with open(outFile, "w", encoding='utf-8') as f:
                f.write(jsonObject)
        except Exception as error:
            errorMsg = f"Could not write a JSON file '{outFile}'! Reason: {error}"
            raise Exception(errorMsg)

        return outFile