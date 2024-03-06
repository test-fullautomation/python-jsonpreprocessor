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

class CSyntaxType():
    python = "python"
    json = "json"

class CNameMangling(Enum):
    AVOIDDATATYPE    = "JPavoidDataType_"
    COLONS           = "__handleColonsInLine__"
    DUPLICATEDKEY_01 = "__handleDuplicatedKey__"
    STRINGCONVERT    = "__ConvertParameterToString__"
    LISTINDEX        = "__IndexOfList__"

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
        self.jsonPath = ''
        self.lImportedFiles = []
        self.recursive_level = 0
        self.syntax = syntax
        self.currentCfg = currentCfg
        self.dUpdatedParams = {}
        self.lNestedParams = []
        self.lDotInParamName = []
        self.bDuplicatedKeys = True
        self.jsonCheck = {}

    def __reset(self, bCleanGlobalVars : bool = False) -> None:
        """
Reset initial variables which are set in constructor method after master JSON file is loaded.
        """
        self.jsonPath = ''
        self.lImportedFiles = []
        self.recursive_level = 0
        self.dUpdatedParams = {}
        self.lNestedParams = []
        self.lDotInParamName = []
        self.bDuplicatedKeys = True
        self.jsonCheck = {}
        if bCleanGlobalVars:
            lGlobalVars = []
            for name, value in globals().items():
                if re.match("^__.+$", name):
                    continue
                else:
                    if isinstance(value, str) or isinstance(value, int) or \
                        isinstance(value, float) or isinstance(value, dict) or \
                        isinstance(value, list) or isinstance(value, type(None)):
                        lGlobalVars.append(name)
            for var in lGlobalVars:
                try:
                    del globals()[var]
                except:
                    pass

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
                self.lImportedFiles = self.lImportedFiles[:self.recursive_level]
                if abs_path_file in self.lImportedFiles:
                    self.__reset(bCleanGlobalVars=True)
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
                        pattern2 = rf'\${{\s*[^{re.escape(self.specialCharacters)}]*\.*' + k1 + r'\s*}$|\[\s*\'' + k1 + r'\'\s*\]$'
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

    def __load_and_removeComments(self, jsonFile : str) -> str:
        """
Loads a given json file and filters all C/C++ style comments.

**Arguments:**

* ``jsonFile``

  / *Condition*: required / *Type*: str /

  Path of file to be processed.

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

        file=open(jsonFile, mode='r', encoding='utf-8')
        sContent=file.read()
        file.close()

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
            if "." in param and CNameMangling.AVOIDDATATYPE.value + param.split('.')[0] in globals():
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
            sExec = "value = " + sParameter
            try:
                ldict = {}
                exec(sExec, globals(), ldict)
                tmpValue = ldict['value']
            except:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"The variable '{sNestedParam.replace('$$', '$')}' is not available!")
            if bKey and (isinstance(tmpValue, list) or isinstance(tmpValue, dict)):
                self.__reset(bCleanGlobalVars=True)
                errorMsg = f"Found expression '{sNestedParam.replace('$$', '$')}' with at least one parameter of composite data type \
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
                sVar = sVar + "[" + item + "]" if re.match(r'^\d+$', item) else sVar + "['" + item + "']"
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
        while re.search(tmpPattern, sInputStr, re.UNICODE) and sInputStr.count("$$")>1:
            referVars = re.findall(r'(' + tmpPattern + r')[^\[]', sInputStr, re.UNICODE)
            for var in referVars:
                sVar = __handleDotInNestedParam(var[0]) if "." in var[0] else var[0]
                tmpValue = __getNestedValue(sVar)
                while var[0] in sInputStr:
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
                            errorMsg = f"Invalid index or dictionary key in parameter '{sInputStr}'. The datatype of variable \
'{var}' have to 'int' or 'str'."
                            raise Exception(errorMsg)
                    else:
                        sInputStr = sInputStr.replace(var[0], str(tmpValue))
        if sInputStr.count("$$")==1:
             tmpPattern = pattern + rf'(\[\s*\d+\s*\]|\[\s*\'[^{re.escape(self.specialCharacters)}]+\'\s*\])*'
             if re.match("^" + tmpPattern + "$", sInputStr.strip(), re.UNICODE) and bKey and not bConvertToStr:
                rootVar = re.search(pattern, sInputStr, re.UNICODE)[0]
                sRootVar = __handleDotInNestedParam(rootVar) if "." in rootVar else rootVar
                sInputStr = sInputStr.replace(rootVar, sRootVar)
                dReplacements = {"$${" : "", "}" : ""}
                return self.__multipleReplace(sInputStr, dReplacements)
             var = re.search(tmpPattern, sInputStr, re.UNICODE)
             rootVar = re.search(pattern, var[0], re.UNICODE)[0]
             sRootVar = __handleDotInNestedParam(rootVar) if "." in rootVar else rootVar
             sVar = var[0].replace(rootVar, sRootVar)
             tmpValue = __getNestedValue(sVar)
             if re.match(r"^\s*" + tmpPattern + r"\s*$", sInputStr, re.UNICODE) and not bKey:
                return tmpValue
             else:
                sInputStr = sInputStr.replace(var[0], str(tmpValue))
        return sInputStr

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
        rootKey = re.sub(r'\[.*\]', "", sKey, re.UNICODE)
        subElements = re.findall(rf"\[\s*'([^{re.escape(self.specialCharacters)}]*)'\s*\]", sKey, re.UNICODE)
        if len(subElements) < 1:
            return True
        else:
            for index, element in enumerate(subElements):
                if index < len(subElements):
                    rootKey = rootKey + "['" + element + "']"
                    sExec = "dumpData = " + rootKey
                    try:
                        exec(sExec)
                    except Exception as error:
                        if "list indices must be integers" in str(error):
                            if keyNested != '':
                                errorMsg = f"Could not set variable '{keyNested}' with value '{value}'! Reason: {error}"
                            else:
                                errorMsg = f"Could not set variable '{sKey}' with value '{value}'! Reason: {error}"
                            self.__reset(bCleanGlobalVars=True)
                            raise Exception(errorMsg)
                        if bCheck==True:
                            return False   # Return 'False' when detected implicit creation of data structures based on nested parameters.
                        else:
                            sExec = rootKey + " = {}"
                            try:
                                exec(sExec, globals())
                            except Exception as error:
                                self.__reset(bCleanGlobalVars=True)
                                if keyNested != '':
                                    sKey = keyNested
                                errorMsg = f"Could not set variable '{sKey}' with value '{value}'! Reason: {error}"
                                raise Exception(errorMsg)
                else:
                    continue
            return True

    def __updateAndReplaceNestedParam(self, oJson : dict, bNested : bool = False, recursive : bool = False, parentParams : str = ''):
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

        def __jsonUpdated(k, v, oJson, bNested, keyNested = '', bDuplicatedHandle=False):
            if keyNested != '':
                if not bDuplicatedHandle:
                    del oJson[keyNested]
                rootKey = re.sub(r'\[.*\]', "", k, re.UNICODE)
                if re.search(r'^[0-9]+.*$', rootKey, re.UNICODE):
                    oJson[f"{rootKey}"] = {}
                elif rootKey not in globals():
                    oJson[rootKey] = {}
                    sExec = rootKey + " = {}"
                    try:
                        exec(sExec, globals())
                    except Exception as error:
                        raise Exception(f"Could not set root key element '{rootKey}'! Reason: {error}")
                if re.match(rf"^[^{re.escape(self.specialCharacters)}]+\[.+\]+$", k, re.UNICODE):
                    self.__checkAndCreateNewElement(k, v, keyNested=keyNested)
                    sExec = k + " = \"" + v + "\"" if isinstance(v, str) else k + " = " + str(v)
                    try:
                        exec(sExec, globals())
                    except Exception as error:
                        self.__reset(bCleanGlobalVars=True)
                        errorMsg = f"Could not set variable '{keyNested}' with value '{v}'! Reason: {error}"
                        raise Exception(errorMsg)

                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = re.sub(CNameMangling.AVOIDDATATYPE.value, "", k)
                    if isinstance(v, str):
                        sExec = "oJson['" + k.split('[', 1)[0] + "'][" + k.split('[', 1)[1] + " = \"" + v + "\""
                    else:
                        sExec = "oJson['" + k.split('[', 1)[0] + "'][" + k.split('[', 1)[1] + " = " + str(v)
                    try:
                        exec(sExec, globals())
                    except:
                        pass
                else:
                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = re.sub(CNameMangling.AVOIDDATATYPE.value, "", k)
                    oJson[k] = v
                    globals().update({k:v})

            else:
                if bNested:
                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = re.sub(CNameMangling.AVOIDDATATYPE.value, "", k) 
                oJson[k] = v
                globals().update({k:v})

        def __loadNestedValue(initValue: str, sInputStr: str, bKey=False, key=''):
            varPattern = rf"\${{\s*[^{re.escape(self.specialCharacters)}]*\s*}}"
            indexPattern = r"\[\s*-*\d*\s*:\s*-*\d*\s*\]"
            dictPattern = r"(\[+\s*'[^\$\[\]\(\)]+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*" + varPattern + r".*\]+)*|" + indexPattern
            pattern = varPattern + dictPattern
            bValueConvertString = False
            if CNameMangling.STRINGCONVERT.value in sInputStr:
                bValueConvertString = True
                sInputStr = sInputStr.replace(CNameMangling.STRINGCONVERT.value, '')
                sInputStr = re.sub("\$", "$$", sInputStr)
                initValue = initValue.replace(CNameMangling.STRINGCONVERT.value, '')
            elif re.match(r"^\s*" + pattern + r"\s*$", sInputStr, re.UNICODE):
                sInputStr = re.sub("\$", "$$", sInputStr)
            if sInputStr.count("${") > sInputStr.count("}"):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid syntax! One or more than one opened or closed curly bracket is missing in expression '{initValue}'.\n \
          Please check the configuration file of the executed test!")
            sInputStr = self.__checkParamName(sInputStr)
            handledValue = self.__nestedParamHandler(sInputStr) if not bValueConvertString else \
                                    self.__nestedParamHandler(sInputStr, bKey=bKey, bConvertToStr=bValueConvertString)
            if bValueConvertString and not isinstance(handledValue, str):
                handledValue = str(handledValue)
            return handledValue

        if bool(self.currentCfg) and not recursive:
            for k, v in self.currentCfg.items():
                if k in self.lDataTypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                globals().update({k:v})

        tmpJson = copy.deepcopy(oJson)
        sepecialCharacters = r'!@#%^&*()+=[\]|;:\'",<>?/`~'
        pattern = rf"\${{\s*[^{re.escape(sepecialCharacters)}]+\s*}}"
        pattern = pattern + r"(\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${.+\s*\]+)*"
        for k, v in tmpJson.items():
            if "${" not in k and CNameMangling.DUPLICATEDKEY_01.value not in k:
                parentParams = k if parentParams=='' else parentParams + "['" + k + "']"
            keyNested = ''
            bStrConvert = False
            bImplicitCreation = False
            bDuplicatedHandle = False
            if re.match(r"^.+" + CNameMangling.DUPLICATEDKEY_01.value + r"\d+$", k, re.UNICODE):
                del oJson[k]
                dupKey = k
                k = re.sub(CNameMangling.DUPLICATEDKEY_01.value + r"\d+$", "", k)
                value = tmpJson[k].pop(1)
                if "${" not in dupKey and "${" not in str(value):
                    if parentParams != "":
                        sExec = parentParams + "['" + k + "'] = \"" + value + "\"" if isinstance(value, str) else \
                                parentParams + "['" + k + "'] = " + str(value)
                    else:
                        sExec = k + " = \"" + value + "\"" if isinstance(value, str) else \
                                k + " = " + str(value)
                    try:
                        exec(sExec, globals())
                    except:
                        pass
                bDuplicatedHandle = True
            if CNameMangling.STRINGCONVERT.value in k:
                bStrConvert = True
                del oJson[k]
                keyNested = k.replace(CNameMangling.STRINGCONVERT.value, '')
                oJson[keyNested] = v
                bNested = True
                while "${" in k:
                    k = __loadNestedValue(keyNested, k, bKey=True, key=keyNested)
            elif re.match(r"^\s*" + pattern + r"\s*$", k, re.UNICODE):
                keyNested = k
                if re.search(r"\[\s*'*" + pattern + r"'*\s*\]", keyNested, re.UNICODE) or \
                    re.search(r"\." + pattern + r"[\.}]+", keyNested, re.UNICODE):
                    bImplicitCreation = True
                k = re.sub("\$", "$$", k)
                k = self.__checkParamName(k)
                k = self.__nestedParamHandler(k, bKey=True)
                if bImplicitCreation and not self.__checkAndCreateNewElement(k, v, bCheck=True, keyNested=keyNested):
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"The implicit creation of data structures based on nested parameter is not supported. \
New parameter '{k}' could not be created by the expression '{keyNested}'")
            elif k.count('{') != k.count('}'):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Could not overwrite parameter {k} due to wrong format.\n \
        Please check key '{k}' in config file!!!")
            
            if isinstance(v, dict):
                v, bNested = self.__updateAndReplaceNestedParam(v, bNested, recursive=True, parentParams=parentParams)
            elif isinstance(v, list):
                if v[0] != CNameMangling.DUPLICATEDKEY_01.value:
                    tmpValue = []
                    for item in v:
                        if isinstance(item, str) and re.search(pattern, item, re.UNICODE):
                            bNested = True
                            initItem = item
                            while isinstance(item, str) and "${" in item:
                                item = __loadNestedValue(initItem, item)

                        tmpValue.append(item)
                    v = tmpValue
                    del tmpValue
                else:
                    if len(v)==2:
                        v = v[1]
                        if "${" in str(v):
                            bNested = True
                        while isinstance(v, str) and "${" in v:
                            v = __loadNestedValue(initValue=v, sInputStr=v)
                    else:
                        i=1
                        while i<len(v):
                            while re.search(pattern, v[i], re.UNICODE):
                                bNested = True
                                initItem = v[i]
                                tmpValue = __loadNestedValue(initItem, v[i]) 
                                v[i] = tmpValue
                            tmpValue = v[i]
                            i+=1
                        v = tmpValue
                        del tmpValue

            elif isinstance(v, str) and self.__checkNestedParam(v):
                if re.search(pattern, v, re.UNICODE):
                    bNested = True
                    initValue = v
                    while isinstance(v, str) and "${" in v:
                        v = __loadNestedValue(initValue, v)
                    if bDuplicatedHandle:
                        if "${" not in dupKey and parentParams != "":
                            sExec = parentParams + "['" + k + "'] = \"" + v + "\"" if isinstance(v, str) else \
                                    parentParams + "['" + k + "'] = " + str(v)
                        else:
                            sExec = k + " = \"" + v + "\"" if isinstance(v, str) else \
                                    k + " = " + str(v)
                        try:
                            exec(sExec, globals())
                        except:
                            pass
                        continue
            __jsonUpdated(k, v, oJson, bNested, keyNested, bDuplicatedHandle)
            if keyNested != '' and not bStrConvert:
                transTable = str.maketrans({"[":"\[", "]":"\]"})
                tmpList = []
                for key in self.dUpdatedParams:
                    if re.match(r"^" + k.translate(transTable) + r"\['.+$", key, re.UNICODE):
                        tmpList.append(key)
                for item in tmpList:
                    self.dUpdatedParams.pop(item)
                if not bDuplicatedHandle and CNameMangling.DUPLICATEDKEY_01.value not in k:
                    self.dUpdatedParams.update({k:v})

            if re.match(r"^.+\['" + k + r"'\]$", parentParams, re.UNICODE):
                parentParams = re.sub("\['" + k + "'\]", "", parentParams)
        del tmpJson
        return oJson, bNested

    def __checkAndUpdateKeyValue(self, sInputStr: str, nestedKey = False) -> str:
        """
This function checks and makes up all nested parameters in JSON configuration files.

**Arguments:**

* ``sInputStr*``

  / *Condition*: required / *Type*: str /

  Key or value which is parsed from JSON configuration file.

**Returns:**
   The string after nested parameters are made up.

   Ex:

      Nested param ${abc}['xyz'] -> "${abc}['xyz']"

      Nested param "${abc}['xyz']" -> "${abc}['xyz']__ConvertParameterToString__"
        """
        def __recursiveNestedHandling(sInputStr: str, lNestedParam: list) -> str:
            """
This method handles nested parameters are called recursively in a string value.
            """
            tmpList = []
            for item in lNestedParam:
                item = re.sub(r'([$()\[\]])', r'\\\1', item)
                pattern = rf"(\${{\s*[^{re.escape(self.specialCharacters)}]*" + item + \
                            rf"[^{re.escape(self.specialCharacters)}]*\s*}}(\[\s*.+\s*\])*)"
                if re.search(pattern, sInputStr, re.UNICODE):
                    sInputStr = re.sub("(" + pattern + ")", "\\1" + CNameMangling.STRINGCONVERT.value, sInputStr, re.UNICODE)
                tmpResults = re.findall("(" + pattern + CNameMangling.STRINGCONVERT.value + ")", sInputStr, re.UNICODE)
                for result in tmpResults:
                    tmpList.append(result[0])
            if tmpList != []:
                sInputStr = __recursiveNestedHandling(sInputStr, tmpList)

            return sInputStr

        variablePattern = rf"[^{re.escape(self.specialCharacters)}]+"
        indexPattern = r"\[\s*-*\d*\s*:\s*-*\d*\s*\]"
        dictPattern = r"\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${\s*" + variablePattern + r"\s*}.*\]+|" + indexPattern
        nestedPattern = r"\${\s*" + variablePattern + r"(\${\s*" + variablePattern + r"\s*})*" + r"\s*}(" + dictPattern + r")*"
        valueStrPattern = r"[\"|\']\s*[0-9A-Za-z_\-\s*]+[\"|\']"
        valueNumberPattern = r"[0-9\.]+"

        if "${" in sInputStr:
            if re.search(r"\[[0-9\s]*[A-Za-z_]+[0-9\s]*\]", sInputStr, re.UNICODE):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid syntax! A sub-element in {sInputStr.strip()} has to enclosed in quotes.")
            if re.match(r"^\s*" + nestedPattern + r"[\s,\]}]*$", sInputStr, re.UNICODE):
                sInputStr = re.sub("(" + nestedPattern + ")", "\"\\1\"", sInputStr, re.UNICODE)
                nestedParam = re.sub(r"^\s*\"(.+)\".*$", "\\1", sInputStr)
                self.lNestedParams.append(nestedParam)
            elif re.match(r"^\s*\"\s*" + nestedPattern + r"\"[\s,\]}]*$", sInputStr, re.UNICODE):
                nestedParam = re.sub(r"^\s*\"(.+)\".*$", "\\1", sInputStr)
                self.lNestedParams.append(nestedParam)
                sInputStr = sInputStr.replace(nestedParam, nestedParam + CNameMangling.STRINGCONVERT.value)
            elif ((re.match(r"[\s{\[]*\".+\"\s*", sInputStr) and sInputStr.count("\"")==2) \
                or (re.match(r"^\s*\${.+}[,\s]*$", sInputStr) and sInputStr.count("{")==sInputStr.count("}") \
                    and not re.search(r"(?<!^)(?<!\.)[^\.]\${", sInputStr.strip()) and not nestedKey)) \
                and re.search("(" + nestedPattern + ")*", sInputStr, re.UNICODE):
                if sInputStr.strip()[-1] == ",":
                    sInputStr = sInputStr.strip()[:-2] + CNameMangling.STRINGCONVERT.value + "\","
                else:
                    sInputStr = sInputStr.strip()[:-1] + CNameMangling.STRINGCONVERT.value + "\""
            elif "," in sInputStr:
                if not re.match(r"^\s*\".+\"\s*$", sInputStr):
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"Invalid nested parameter format: {sInputStr} - The double quotes are missing!!!")
                listPattern = r"^\s*(\"*" + nestedPattern + r"\"*\s*,+\s*|" + valueStrPattern + r"\s*,+\s*|" + valueNumberPattern + r"\s*,+\s*)+" + \
                            r"(\"*" + nestedPattern + r"\"*\s*,*\s*|" + valueStrPattern + r"\s*,*\s*|" + valueNumberPattern + r"[\s,]*)*[\]}\s]*$"
                lNestedParam = re.findall("(" + nestedPattern + ")", sInputStr, re.UNICODE)
                for nestedParam in lNestedParam:
                    self.lNestedParams.append(nestedParam[0])
                if re.match(listPattern, sInputStr):
                    items = sInputStr.split(",")
                    newInputStr = ''
                    for item in items:
                        tmpItem = item
                        if "${" in item:
                            if not re.match(r"^[\s\"]*" + nestedPattern + r"[\"\]}\s]*$", item, re.UNICODE):
                                self.__reset(bCleanGlobalVars=True)
                                raise Exception(f"Invalid nested parameter format: {item}")
                            elif re.match(r"^\s*\".*" + nestedPattern + r".*\"\s*$", item, re.UNICODE):
                                item = re.sub("(" + nestedPattern + ")", "\\1" + CNameMangling.STRINGCONVERT.value, item)
                                tmpList = []
                                for subItem in re.findall("(" + nestedPattern + CNameMangling.STRINGCONVERT.value + ")", item, re.UNICODE):
                                    tmpList.append(subItem[0])
                                item = __recursiveNestedHandling(item, tmpList)
                            elif re.match(r"^\s*" + nestedPattern + r"[\s\]}]*$", item, re.UNICODE):
                                item = re.sub("(" + nestedPattern + ")", "\"\\1\"", item, re.UNICODE)
                                nestedParam = re.sub(r"^\s*\"(.+)\".*$", "\\1", item)
                                self.lNestedParams.append(nestedParam)
                        newInputStr = newInputStr + item if tmpItem==items[len(items)-1] else newInputStr + item + ","
                    sInputStr = newInputStr
            elif re.search(r"\${\s*}", sInputStr) \
                or (nestedKey and (sInputStr.count("{") != sInputStr.count("}") or sInputStr.count("[") != sInputStr.count("]"))):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid parameter format: {sInputStr}")
            elif nestedKey and re.match(r"^\s*\${[^\(\)\!@#%\^\&\-\+\/\\\=`~\?]+[}\[\]]+\s*$", sInputStr):
                sInputStr = re.sub(r"^\s*(\${[^\(\)\!@#%\^\&\-\+\/\\\=`~\?]+[}\[\]]+)\s*$", "\"\\1\"", sInputStr)
            else:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid nested parameter format: {sInputStr} - The double quotes are missing!!!")

        sOutput = sInputStr
        return sOutput

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

    def __checkNestedParam(self, sInput : str) -> bool:
        """
Checks nested parameter format.

**Arguments:**

* ``sInput``

  / *Condition*: required / *Type*: str /

**Returns:**

  *raise exception if nested parameter format invalid*
        """
        pattern1 = rf"\${{[^{re.escape(self.specialCharacters)}]+\['*.+'*\].*}}"
        if re.search(pattern1, sInput, re.UNICODE):
            if CNameMangling.STRINGCONVERT.value in sInput:
                sInput = sInput.replace(CNameMangling.STRINGCONVERT.value, "")
            raise Exception(f"Invalid nested parameter format: '{sInput}'." + "The '[<index>]' or '[<key>]' have to \
be outside of '${<variable name>}'.")
        else:
            return True

    def jsonLoad(self, jFile : str, masterFile : bool = True):
        """
This method is the entry point of JsonPreprocessor.

``jsonLoad`` loads the JSON file, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``jFile``

  / *Condition*: required / *Type*: str /

  Path and name of main JSON file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

* ``oJson``

  / *Type*: dict /

  Preprocessed JSON file(s) as Python dictionary
        """
        
        def __handleListElements(sInput : str) -> str:
            items = re.split("\s*,\s*", sInput)
            j=0
            newItem = ""
            for item in items:
                j+=1
                if j<len(items):
                    newItem = newItem + self.__checkAndUpdateKeyValue(item) + ","
                else:
                    newItem = newItem + self.__checkAndUpdateKeyValue(item)
            return newItem
        
        def __handleDuplicatedKey(dInput : dict) -> dict:
            tmpDict = copy.deepcopy(dInput)
            listKeys = list(tmpDict.keys())
            dictValues = {}
            for key in listKeys:
                if CNameMangling.DUPLICATEDKEY_01.value in key:
                    origKey = re.sub(CNameMangling.DUPLICATEDKEY_01.value + "\d+\s*$", "", key)
                    dictValues[origKey] = copy.deepcopy(tmpDict[origKey])
            for k, v in tmpDict.items():
                if CNameMangling.DUPLICATEDKEY_01.value in k:
                    origK = re.sub(CNameMangling.DUPLICATEDKEY_01.value + "\d+\s*$", "", k)
                    dInput[k] = dictValues[origK].pop(1)
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
            pattern1 = rf"\${{\s*[^{re.escape(self.specialCharacters)}]*\['*.+'*\]\s*}}"
            for k, v in oJson.items():
                if re.search(pattern1, k, re.UNICODE):
                    errorMsg = f"Invalid syntax: Found index or sub-element inside curly brackets in the parameter '{k}'"
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(errorMsg)
                if isinstance(v, dict):
                    __checkKeynameFormat(v)

        jFile = CString.NormalizePath(jFile, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        if  not(os.path.isfile(jFile)):
            self.__reset(bCleanGlobalVars=True)
            raise Exception(f"File '{jFile}' is not existing!")

        self.lImportedFiles.append(jFile)
        self.jsonPath = os.path.dirname(jFile)
        try:
            sJsonData= self.__load_and_removeComments(jFile)
        except Exception as reason:
            self.__reset(bCleanGlobalVars=True)
            raise Exception(f"Could not read json file '{jFile}' due to: '{reason}'!")

        pattern = rf"\${{\s*[^{re.escape(self.specialCharacters)}]*\s*}}(\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+)*"
        sJsonDataUpdated = ""
        for line in sJsonData.splitlines():
            if line == '' or line.isspace():
                continue
            try:
                listDummy = shlex.split(line)
            except Exception as error:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"\n{str(error)} in line: '{line}'")

            if re.search(pattern, line, re.UNICODE):
                lNestedVar = re.findall(rf"\${{\s*([^{re.escape(self.specialCharacters)}]+)\s*}}", line, re.UNICODE)
                for nestedVar in lNestedVar:
                    if nestedVar[0].isdigit():
                        self.__reset(bCleanGlobalVars=True)
                        raise Exception(f"Invalid parameter format in line: {line.strip()}")
                tmpList = re.findall(r"(\"[^\"]+\")", line)
                line = re.sub(r"(\"[^\"]+\")", CNameMangling.COLONS.value, line)
                indexPattern = r"\[\s*-*\d*\s*:\s*-*\d*\s*\]"
                if re.search(indexPattern, line):
                    indexList = re.findall(indexPattern, line)
                    line = re.sub("(" + indexPattern + ")", CNameMangling.LISTINDEX.value, line)
                items = re.split("\s*:\s*", line)
                newLine = ""
                i=0
                for item in items:
                    nestedKey = False
                    nestedKeyPattern = r"^\s*,\s*\${.+[\]}]\s*$"
                    if i==0 or re.match(nestedKeyPattern, item):
                        nestedKey = True
                    if CNameMangling.COLONS.value in item:
                        while CNameMangling.COLONS.value in item:
                            item = re.sub(CNameMangling.COLONS.value, tmpList[0], item, count=1)
                            tmpList.pop(0)
                    elif CNameMangling.LISTINDEX.value in item:
                        while CNameMangling.LISTINDEX.value in item:
                            item  = re.sub(CNameMangling.LISTINDEX.value, indexList[0], item, count=1)
                            indexList.pop(0)
                    i+=1
                    newSubItem = ""
                    if re.search(r"^\s*\[.+\][\s,]*$", item) and item.count('[')==item.count(']'):
                        item = item.strip()
                        bLastElement = True
                        if item.endswith(","):
                            bLastElement = False
                        item = re.sub(r"^\[", "", item)
                        item = re.sub(r"\s*\][\s,]*$", "", item)
                        newSubItem = __handleListElements(item)
                        newSubItem = "[" + newSubItem + "]" if bLastElement else "[" + newSubItem + "],"
                    elif re.search(r"^\s*\[.*\${.+", item):
                        item = item.strip()
                        item = re.sub(r"^\[", "", item)
                        newSubItem = __handleListElements(item)
                        newSubItem = "[" + newSubItem
                    elif re.search(r"]\s*,*\s*", item) and item.count('[') < item.count(']'):
                        item = item.rstrip()
                        bLastElement = True
                        if item.endswith(","):
                            bLastElement = False
                        item = re.sub(r"\s*\][\s,]*$", "", item)
                        newSubItem = __handleListElements(item)
                        newSubItem = newSubItem + "]" if bLastElement else newSubItem + "],"
                    elif re.match(r"^[\s\"]*\${.+[}\]]+[\"\s]*,[\s\"]*\${.+[}\]]+[\"\s]*$", item):
                        subItems = re.split("\s*,\s*", item)
                        subItem1 = self.__checkAndUpdateKeyValue(subItems[0], nestedKey)
                        subItem2 = self.__checkAndUpdateKeyValue(subItems[1], nestedKey=True)
                        newSubItem = subItem1 + ", " + subItem2
                    else:
                        newSubItem = self.__checkAndUpdateKeyValue(item, nestedKey)
                    if i<len(items):
                        newLine = newLine + newSubItem + " : "
                    else:
                        newLine = newLine + newSubItem
                for nestedParam in self.lNestedParams:
                    dReplacements = {"$" : "\$", "[" : "\[", "]" : "\]"}
                    tmpNestedParam = self.__multipleReplace(nestedParam, dReplacements)
                    if re.search(r"(\s*\"str\(" + tmpNestedParam + "\)\"\s*:)", newLine.replace(CNameMangling.STRINGCONVERT.value, '')) \
                        or re.search(r"(\s*\"" + tmpNestedParam + r"\"\s*:)", newLine.replace(CNameMangling.STRINGCONVERT.value, '')):
                        self.lNestedParams.remove(nestedParam)
                sJsonDataUpdated = sJsonDataUpdated + newLine + "\n"
            else:
                if "${" in line:
                    self.__reset(bCleanGlobalVars=True)
                    invalidPattern1 = r"\${\s*[0-9A-Za-z\._]*\[.+\][0-9A-Za-z\._]*\s*}"
                    if re.search(invalidPattern1, line):
                        raise Exception(f"Invalid syntax: Found index inside curly brackets in line '{line.strip()}'. \
Indices in square brackets have to be placed outside the curly brackets.")
                    else:
                        raise Exception(f"Invalid parameter format in line: {line.strip()}")
                sJsonDataUpdated = sJsonDataUpdated + line + "\n"

        CJSONDecoder = None
        if self.syntax != CSyntaxType.json:
            if self.syntax == CSyntaxType.python:
                CJSONDecoder = CPythonJSONDecoder
            else:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Provided syntax '{self.syntax}' is not supported.")
        # Load the temporary Json object without checking duplicated keys for 
        # verifying duplicated keys later.
        if masterFile:
            self.bDuplicatedKeys = False
            try:
                self.jsonCheck = json.loads(sJsonDataUpdated,
                                cls=CJSONDecoder,
                                object_pairs_hook=self.__processImportFiles)
            except Exception as error:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"JSON file: {jFile}\n{error}")
            self.bDuplicatedKeys = True

        # Load Json object with checking duplicated keys feature is enabled.
        # The duplicated keys feature uses the self.jsonCheck object to check duplicated keys. 
        try:
            oJson = json.loads(sJsonDataUpdated,
                               cls=CJSONDecoder,
                               object_pairs_hook=self.__processImportFiles)
        except Exception as error:
            self.__reset(bCleanGlobalVars=True)
            raise Exception(f"JSON file: {jFile}\n{error}")
        self.__checkDotInParamName(oJson)
        __checkKeynameFormat(oJson)

        if masterFile:
            oJson = __handleDuplicatedKey(oJson)
            for k, v in oJson.items():
                if re.match(r"^[0-9]+.*$", k) or re.match(r"^[\s\"]*\${.+}[\s\"]*$", k) \
                    or CNameMangling.DUPLICATEDKEY_01.value in k:
                    continue
                if k in self.lDataTypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                globals().update({k:v})
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