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
import platform
import copy
import shlex

from PythonExtensionsCollection.String.CString import CString
from enum import Enum

class CSyntaxType():
    python = "python"
    json = "json"

class CNameMangling(Enum):
    AVOIDDATATYPE    = "JPavoidDataType_"
    COLONS           = "__handleColonsInLine__"
    DUPLICATEDKEY_00 = "__rootDuplicatedKey__"
    DUPLICATEDKEY_01 = "__handleDuplicatedKey__"
    DUPLICATEDKEY_02 = "__RecursiveInitialValue__"
    STRINGCONVERT    = "__ConvertParameterToString__"
    LISTINDEX        = "__IndexOfList__"

class CPythonJSONDecoder(json.JSONDecoder):
    """
   Add python data types and syntax to json. ``True``, ``False`` and ``None`` will be a accepted as json syntax elements.

**Args:**

   **json.JSONDecoder** (*object*)

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
   CJsonPreprocessor extends the syntax of json.

   Features are

   -  Allow c/c++-style comments within json files.

      // single line or part of single line and /\* \*/ multline comments are possible

   -  Allow to import json files into json files

      ``"[import]" : "relative/absolute path"``, imports another json file to exactly this location.

   -  Allow use of the defined paramaters within json files

      In any place the syntax ``${basenode.subnode. ... nodename}`` allows to reference an already existing parameter.

      * Example:

   .. code::

      {
          "basenode" : {
                           subnode : {
                                          "myparam" : 5
                                     },

                       },

          "myVar" : ${basenode.subnode.myparam}
      }

   - Allow Python data types ``True``, ``False`` and ``None``
    """

    def __init__(self, syntax: CSyntaxType = CSyntaxType.python , currentCfg : dict = {}) -> None:
        """
   Constructor

**Args:**

   **syntax** (*CSyntaxType*) optional

      default: `json` , `python`

      If set to `python`, then python data types are allowed as part of json file.

   **currentCfg** (*dict*) optional

      Internally used to aggregate imported json files.
        """
        import builtins
        import keyword
        self.lDataTypes = [name for name, value in vars(builtins).items() if isinstance(value, type)]
        self.lDataTypes.append(keyword.kwlist)
        self.jsonPath = ''
        self.lImportedFiles = []
        self.recursive_level = 0
        self.syntax = syntax
        self.currentCfg = currentCfg
        self.dUpdatedParams = {}
        self.lNestedParams = []
        self.lDotInParamName = []

    def __reset(self, bCleanGlobalVars : bool = False) -> None:
        '''
   Reset initial variables which are set in constructor method after master Json file is loaded.
        '''
        self.jsonPath = ''
        self.lImportedFiles = []
        self.recursive_level = 0
        self.dUpdatedParams = {}
        self.lNestedParams = []
        self.lDotInParamName = []
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
        '''
   This is a custom decorder of ``json.loads object_pairs_hook`` function.

   This method helps to import json files which are provided in ``"[import]"`` keyword into the current json file.

**Args:**

   **input_data** (*dict*)

      Dictionary from json file as input

**Returns:**

   **out_dict** (*dict*)

      Dictionary as output, dictionary is extended if ``"[import]"`` found and properly imported.
        '''
        out_dict = {}

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
                tmpOutdict = copy.deepcopy(out_dict)
                for k1, v1 in tmpOutdict.items():
                    pattern2 = "\${\s*[0-9A-Za-z\.\-_]*\.*" + k1 + "\s*}$|\[\s*'" + k1 + "'\s*\]$"
                    if re.search(pattern2, key):
                        key = k1
                    if k1 == key:
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
        return out_dict

    def __load_and_removeComments(self, jsonFile : str) -> str:
        """
      Loads a given json file and filters all C/C++ style comments.

**Args:**

   **jsonFile** (*string*)

      Path (absolute/relative/) file to be processed.
      The path can contain windows/linux style environment variables.

         !ATTENTION! This is dangerous

**Returns:**

   **sContentCleaned** (*string*)

      String version of json file after removing all comments.
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

**Args:**

   **sInput** (*string*)

**Returns:**

   **sInput** (*string*)
        """

        pattern = "\${\s*([0-9A-Za-z_]+[0-9A-Za-z\.\-_]*)\s*}"
        lParams = re.findall(pattern, sInput)
        for param in lParams:
            if "." not in param and param in self.lDataTypes:
                sInput = re.sub(param, CNameMangling.AVOIDDATATYPE.value + param, sInput, count=1)
            if "." in param and CNameMangling.AVOIDDATATYPE.value + param.split('.')[0] in globals():
                sInput = re.sub(param, CNameMangling.AVOIDDATATYPE.value + param, sInput, count=1)
        return sInput

    def __nestedParamHandler(self, sInputStr : str, bKey = False) -> list:
        '''
   This method handles nested variables in parameter names or values. Variable syntax is ${Variable_Name}.

**Args:**

   **sInputStr** (*string*)

      Parameter name or value which contains a nested variable.

**Returns:**

   **lNestedParam** (*list*)

      List of resolved variables which contains in the sInputStr.
        '''
        def __referVarHandle(referVar : str, sInputStr : str) -> str:
            if "." in referVar:
                dotdictVariable = re.sub('\$\${\s*(.*?)\s*}', '\\1', referVar)
                lDotdictVariable = dotdictVariable.split(".")
                lParams = self.__handleDotdictFormat(lDotdictVariable, [])
                rootElement = lParams[0]
                sParam = '$${' + rootElement + '}'
                lParams.pop(0)
                for item in lParams:
                    sParam = sParam + "[" + item + "]" if re.match("^\d+$", item) else sParam + "['" + item + "']"
                sInputStr = re.sub(referVar.replace("$", "\$"), sParam, sInputStr)
                referVar = '$${' + rootElement + '}'
            tmpReferVar = re.sub("\$", "\\$", referVar)
            pattern = '(' + tmpReferVar + '\s*(\[+\s*.*?\s*\]+)*)'
            variable = re.search(pattern, sInputStr)
            return variable[0]

        pattern = "\$\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}"
        referVars = re.findall("(" + pattern + ")", sInputStr)
        while sInputStr.count("$$") > len(referVars):
            for var in referVars:
                if var not in sInputStr:
                    continue
                if "." in var:
                    ddVar = re.sub('\$\${\s*(.*?)\s*}', '\\1', var)
                    lddVar = ddVar.split(".")
                    lElements = self.__handleDotdictFormat(lddVar, [])
                    sVar = '$${' + lElements[0] + '}'
                    lElements.pop(0)
                    for item in lElements:
                        sVar = sVar + "[" + item + "]" if re.match("^\d+$", item) else sVar + "['" + item + "']"
                    sInputStr = sInputStr.replace(var, sVar)
                else:
                    sVar = var
                rootVar = re.search('^\s*\$\${(\s*.*?)}', sVar).group(1)
                tmpVar = re.sub("\$", "\\$", sVar)
                tmpVar = re.sub("((\[\s*'[^\$\[\]\(\)]+'\s*\]|\[\s*\d+\s*\])*)", "", tmpVar)
                subPattern = tmpVar + "((\[\s*'[^\$\[\]\(\)]+'\s*\]|\[\s*\d+\s*\])*)"
                subVar = re.search(subPattern, sInputStr).group(1)
                sExec = "value = " + rootVar + subVar
                try:
                    ldict = {}
                    exec(sExec, globals(), ldict)
                    tmpValue = ldict['value']
                except:
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"The variable '{var.replace('$$', '$')}' is not available!")
                if bKey and (isinstance(tmpValue, list) or isinstance(tmpValue, dict)):
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"Overwrite the element '{sInputStr.replace('$$', '$')}' failed! \
Due to the datatype of '{sVar.replace('$$', '$')}' is '{type(tmpValue)}'. Only simple data types are allowed to be substituted inside.")
                subPattern = "(" + tmpVar + "(\[\s*'[^\$\[\]\(\)]+'\s*\]|\[\s*\d+\s*\])*)"
                var = re.sub("\$", "\\$", re.search(subPattern, sInputStr).group(1))
                if re.search("\[.+\]", var):
                    var = var.replace("[", "\[")
                    var = var.replace("]", "\]")
                sInputStr = re.sub(var, tmpValue, sInputStr) if isinstance(tmpValue, str) else \
                            re.sub(var, str(tmpValue), sInputStr)
            referVars = re.findall("(" + pattern + ")", sInputStr)
        lNestedParam = []
        if len(referVars) > 1:
            if not bKey:
                for referVar in referVars:
                    lNestedParam.append(re.sub("\$\$", "$", __referVarHandle(referVar, sInputStr))) 
                return lNestedParam
            else:
                sUpdateVar =  referVars[0]
                referVars = referVars[1:]
                tmpPattern = re.sub("\$", "\\$", sUpdateVar)
                sInputStr = re.sub(tmpPattern, '', sInputStr, count=1)
                for var in referVars[::-1]:
                    pattern = '(' + var.replace('$', '\$') + '\s*\[\s*.*?\s*\])'
                    variable = re.findall(pattern, sInputStr)
                    if variable == []:
                        sExec = "value = " + re.search('^\s*\$\${(\s*.*?)}', var).group(1)
                        try:
                            ldict = {}
                            exec(sExec, globals(), ldict)
                            tmpValue = ldict['value']
                        except:
                            self.__reset(bCleanGlobalVars=True)
                            raise Exception(f"The variable '{var}' is not available!")
                        if re.search("\[\s*"+ var.replace('$', '\$') +"\s*\]", sInputStr) and isinstance(tmpValue, str):
                            sInputStr = sInputStr.replace(var, "'" + var + "'")
                        sInputStr = re.sub(var.replace('$', '\$'), tmpValue, sInputStr) if isinstance(tmpValue, str) else \
                                    re.sub(var.replace('$', '\$'), str(tmpValue), sInputStr)
                        continue
                    while variable != []:
                        fullVariable = variable[0]
                        pattern = pattern[:-1] + '\[\s*.*?\s*\])'
                        variable = re.findall(pattern, sInputStr)
                        if variable != []:
                            fullVariable = variable[0]
                    sExec = "value = " + re.sub('\$\${\s*(.*?)\s*}', '\\1', fullVariable)
                    try:
                        ldict = {}
                        exec(sExec, globals(), ldict)
                        tmpValue = ldict['value']
                    except:
                        self.__reset(bCleanGlobalVars=True)
                        raise Exception(f"The variable '{fullVariable}' is not available!")
                    pattern = re.sub('\[', '\\[', fullVariable)
                    pattern = re.sub('\]', '\\]', pattern)
                    pattern = re.sub("\$", "\\$", pattern)
                    sInputStr = re.sub(pattern, '\'' + tmpValue + '\'', sInputStr) if isinstance(tmpValue, str) else \
                                re.sub(pattern, '\'' + str(tmpValue) + '\'', sInputStr)
                sKeyHandled = sUpdateVar + sInputStr
                lNestedParam.append(re.sub("\$\$", "$", __referVarHandle(sUpdateVar, sKeyHandled)))
                return lNestedParam
        else:
            lNestedParam.append(re.sub("\$\$", "$", __referVarHandle(referVars[0], sInputStr)))
            return lNestedParam

    def __handleDotdictFormat(self, lInputListParams : list, lParams: list = []) -> list:
        '''
   This method checks the availability of param names contained "." in dotdict format element in JSON config file.

**Args:**

   **lInputListParams** (*list*)

      List of items which separated by "." of dotdict format element.

   **lParams** (*list*)

      List of param names in dotdict format element.

**Returns:**

   **lParams** (*list*)

        '''
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

    def __checkAndCreateNewElement(self, sKey: str, value, bCheck=False):
        '''
    This method check and create new elements if they are not exist.
        '''
        rootKey = re.sub("\[.*\]", "", sKey)
        subElements = re.findall("\[\s*'([0-9A-Za-z_]+[0-9A-Za-z\.\-_]*)'\s*\]", sKey)
        if len(subElements) < 1:
            return True
        else:
            for index, element in enumerate(subElements):
                if index < len(subElements):
                    rootKey = rootKey + "['" + element + "']"
                    sExec = "dumpData = " + rootKey
                    try:
                        exec(sExec)
                    except:
                        if bCheck==True:
                            return False   # Return 'False' when detected implicit creation of data structures based on nested parameters.
                        else:
                            sExec = rootKey + " = {}"
                            try:
                                exec(sExec, globals())
                            except Exception as error:
                                self.__reset(bCleanGlobalVars=True)
                                errorMsg = f"Could not set variable '{sKey}' with value '{value}'! Reason: {error}"
                                raise Exception(errorMsg)
                else:
                    continue
            return True

    def __updateAndReplaceNestedParam(self, oJson : dict, bNested : bool = False, recursive : bool = False):
        '''
   This method replaces all nested parameters in key and value of a json object .

**Args:**

   **oJson** (*dict*)

      Input Json object as dictionary. This dictionary will be searched for all ``${variable}`` occurences.
      If found it will be replaced with it's current value.

**Returns:**

   **oJsonOut** (*dict*)

      Output Json object as dictionary with all variables resolved.
        '''

        def __jsonUpdated(k, v, oJson, bNested, keyNested = ''):
            if keyNested != '':
                del oJson[keyNested]
                if re.match("^[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\[.+\]+$", k):
                    self.__checkAndCreateNewElement(k, v)
                    sExec = k + " = \"" + v + "\"" if isinstance(v, str) else k + " = " + str(v)
                    try:
                        exec(sExec, globals())
                    except Exception as error:
                        self.__reset(bCleanGlobalVars=True)
                        errorMsg = f"Could not set variable '{k}' with value '{v}'! Reason: {error}"
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
            varPattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}"
            indexPattern = "\[\s*-*\d*\s*:\s*-*\d*\s*\]"
            dictPattern = "(\[+\s*'[^\$\[\]\(\)]+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*" + varPattern + ".*\]+)*|" + indexPattern
            pattern = varPattern + dictPattern
            bStringValue = False
            bValueConvertString = False
            if CNameMangling.STRINGCONVERT.value in sInputStr:
                bValueConvertString = True
                sInputStr = sInputStr.replace(CNameMangling.STRINGCONVERT.value, '')
                initValue = initValue.replace(CNameMangling.STRINGCONVERT.value, '')
            if re.search("(str\(\s*" + pattern + "\))", sInputStr.lower()):
                sInputStr = re.sub("str\(\s*(" + pattern + ")\s*\)", "$\\1", sInputStr)
                bStringValue = True
            elif re.match("^\s*" + pattern + "\s*$", sInputStr):
                sInputStr = re.sub("\$", "$$", sInputStr)
            else:
                self.__reset(bCleanGlobalVars=True)
                while "str(" in initValue:
                    initValue = re.sub("str\(([\${}0-9A-Za-z\.\-_\[\]]+)\)", "\\1", initValue, count=1)
                raise Exception(f"Invalid syntax! One or more than one opened or closed curly bracket is missing in expression '{initValue}'.\n \
          Please check the configuration file of the executed test!")
            sInputStr = self.__checkParamName(sInputStr)
            valueAfterProcessed = self.__nestedParamHandler(sInputStr) if not bValueConvertString else \
                                    self.__nestedParamHandler(sInputStr, bKey=bKey)
            for valueProcessed in valueAfterProcessed:
                tmpValueAfterProcessed = re.sub("'*\${\s*(.*?)\s*}'*", '\\1', valueProcessed)
                sExec = "value = " + tmpValueAfterProcessed if isinstance(tmpValueAfterProcessed, str) else \
                        "value = " + str(tmpValueAfterProcessed)
                try:
                    ldict = {}
                    exec(sExec, globals(), ldict)
                    if bStringValue:
                        pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[+\s*'[^\$]+'\s*\]+|\[+\s*\d+\s*\]+)*"
                        sInputStr = re.sub("(\$" + pattern + ")", str(ldict['value']), sInputStr, count=1)
                    else:
                        sInputStr = re.sub("\$\$", "$", sInputStr)
                        sInputStr = str(ldict['value']) if bValueConvertString else ldict['value']
                except:
                    self.__reset(bCleanGlobalVars=True)
                    if CNameMangling.DUPLICATEDKEY_00.value in valueProcessed:
                        valueProcessed = valueProcessed.replace(CNameMangling.DUPLICATEDKEY_00.value, '')
                    elif CNameMangling.DUPLICATEDKEY_02.value in valueProcessed:
                        valueProcessed = valueProcessed.replace(CNameMangling.DUPLICATEDKEY_02.value, '')
                    raise Exception(f"The variable '{valueProcessed}' is not available!")
                if bKey and type(ldict['value']) in [list, dict]:
                    self.__reset(bCleanGlobalVars=True)
                    while 'str(' in key:
                        key = re.sub("str\(([0-9A-Za-z\._\${}'\[\]]+)\)", "\\1", key)
                    errorMsg = f"Found expression '{key}' with at least one parameter of composite data type \
('{valueProcessed}' is of type {type(ldict['value'])}). Because of this expression is the name of a parameter, \
only simple data types are allowed to be substituted inside."
                    raise Exception(errorMsg)
                if "${" not in str(sInputStr):
                    break
            return sInputStr

        if bool(self.currentCfg) and not recursive:
            for k, v in self.currentCfg.items():
                if k in self.lDataTypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                globals().update({k:v})

        tmpJson = copy.deepcopy(oJson)
        pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\$\{\}\-_]*\s*}(\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${.+\s*\]+)*"
        for k, v in tmpJson.items():
            keyNested = ''
            bStrConvert = False
            bImplicitCreation = False
            if CNameMangling.DUPLICATEDKEY_00.value in k:
                del oJson[k]
                k = k.replace(CNameMangling.DUPLICATEDKEY_00.value, '')
                oJson[k] = v
            if re.search("(str\(" + pattern + "\))", k.lower()):
                bStrConvert = True
                keyNested = k
                bNested = True
                while "${" in k:
                    k = __loadNestedValue(keyNested, k, bKey=True, key=keyNested)
            elif CNameMangling.STRINGCONVERT.value in k:
                bStrConvert = True
                del oJson[k]
                keyNested = k.replace(CNameMangling.STRINGCONVERT.value, '')
                oJson[keyNested] = v
                bNested = True
                while "${" in k:
                    k = __loadNestedValue(keyNested, k, bKey=True, key=keyNested)
            elif re.match("^\s*" + pattern + "\s*$", k.lower()):
                keyNested = k
                if re.search("\[\s*'*" + pattern + "'*\s*\]", keyNested) or \
                    re.search("\." + pattern + "[\.}]+", keyNested):
                    bImplicitCreation = True
                k = re.sub("\$", "$$", k)
                k = self.__checkParamName(k)
                keyAfterProcessed = self.__nestedParamHandler(k, bKey=True)
                k = re.sub("\$\$", "$", k)
                k = re.sub('^\s*\${\s*(.*?)\s*}', '\\1', keyAfterProcessed[0])
                # Temporary disable implicit creation of data structures based on nested parameters.
                # In case check sub-element returns False -> reset() and raise an exception.
                if bImplicitCreation and not self.__checkAndCreateNewElement(k, v, bCheck=True):
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"The implicit creation of data structures based on nested parameter is not supported. \
New parameter '{k}' could not be created by the expression '{keyNested}'")
            elif k.count('{') != k.count('}'):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Could not overwrite parameter {k} due to wrong format.\n \
        Please check key '{k}' in config file!!!")

            if isinstance(v, dict):
                v, bNested = self.__updateAndReplaceNestedParam(v, bNested, recursive=True)

            elif isinstance(v, list):
                if v[0] != CNameMangling.DUPLICATEDKEY_01.value:
                    tmpValue = []
                    for item in v:
                        if isinstance(item, str) and re.search(pattern, item.lower()):
                            bNested = True
                            initItem = item
                            while isinstance(item, str) and "${" in item:
                                item = __loadNestedValue(initItem, item)

                        tmpValue.append(item)
                    v = tmpValue
                    del tmpValue
                else:
                    i=1
                    while i<len(v):
                        while re.search(pattern, v[i]):
                            bNested = True
                            initItem = v[i]
                            tmpValue = __loadNestedValue(initItem, v[i]) 
                            v[i] = tmpValue
                        tmpValue = v[i]
                        i+=1
                    v = tmpValue
                    del tmpValue

            elif isinstance(v, str):
                if re.search(pattern, v.lower()):
                    bNested = True
                    initValue = v
                    while isinstance(v, str) and "${" in v:
                        v = __loadNestedValue(initValue, v)

            __jsonUpdated(k, v, oJson, bNested, keyNested)
            if keyNested != '' and not bStrConvert:
                self.dUpdatedParams.update({k:v})
        del tmpJson
        return oJson, bNested

    def __checkAndUpdateKeyValue(self, sInputStr: str, nestedKey = False) -> str:
        '''
   This function checks and makes up all nested parameters in json configuration files.

**Args:**
   **sInputStr** (*string*)
   Key or value which is parsed from json configuration file.

**Returns:**
   The string after nested parameters are made up.

   Ex:

      Nested param ${abc}['xyz'] -> "${abc}['xyz']"

      Nested param "${abc}['xyz']" -> "str(${abc}['xyz'])"
        '''
        def __recursiveNestedHandling(sInputStr: str, lNestedParam: list) -> str:
            '''
        This method handles nested parameters are called recursively in a string value.
            '''
            tmpList = []
            for item in lNestedParam:
                item = re.sub(r'([$()\[\]])', r'\\\1', item)
                pattern = "(\${\s*[0-9A-Za-z\.\-_]*" + item + "[0-9A-Za-z\.\-_]*\s*}(\[\s*.+\s*\])*)"
                if re.search(pattern, sInputStr):
                    sInputStr = re.sub("(" + pattern + ")", "str(\\1)", sInputStr)
                tmpResults = re.findall("(str\(" + pattern + "\))", sInputStr)
                for result in tmpResults:
                    tmpList.append(result[0])
            if tmpList != []:
                sInputStr = __recursiveNestedHandling(sInputStr, tmpList)

            return sInputStr

        variablePattern = "[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*"
        indexPattern = "\[\s*-*\d*\s*:\s*-*\d*\s*\]"
        dictPattern = "\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${\s*" + variablePattern + "\s*}.*\]+|" + indexPattern
        nestedPattern = "\${\s*" + variablePattern + "(\${\s*" + variablePattern + "\s*})*" + "\s*}(" + dictPattern +")*"
        valueStrPattern = "[\"|\']\s*[0-9A-Za-z_\-\s*]+[\"|\']"
        valueNumberPattern = "[0-9\.]+"

        if "${" in sInputStr:
            if re.search("\[[0-9\s]*[A-Za-z_]+[0-9\s]*\]", sInputStr):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid syntax! A sub-element in {sInputStr.strip()} has to enclosed in quotes.")
            if re.match("^\s*" + nestedPattern + "\s*,*\]*}*\s*$", sInputStr.lower()):
                sInputStr = re.sub("(" + nestedPattern + ")", "\"\\1\"", sInputStr)
                nestedParam = re.sub("^\s*\"(.+)\"\s*.*$", "\\1", sInputStr)
                self.lNestedParams.append(nestedParam)
            elif re.match("^\s*\"\s*" + nestedPattern + "\"\s*,*\]*}*\s*$", sInputStr.lower()):
                nestedParam = re.sub("^\s*\"(.+)\"\s*.*$", "\\1", sInputStr)
                self.lNestedParams.append(nestedParam)
                sInputStr = sInputStr.replace(nestedParam, nestedParam + CNameMangling.STRINGCONVERT.value)
            elif re.match("\s*{*\[*\".+\"\s*", sInputStr.lower()) and sInputStr.count("\"")==2 \
                and re.search("(" + nestedPattern + ")*", sInputStr.lower()):
                dictPattern = "\[+\s*'[0-9A-Za-z\.\-_${}\[\]]*'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${\s*" + variablePattern + "\s*}\s*\]+"
                nestedPattern = "\${\s*" + variablePattern + "(\${\s*" + variablePattern + "\s*})*" + "\s*}(" + dictPattern +")*"
                lNestedParam = []
                for item in re.findall("(" + nestedPattern + ")", sInputStr):
                    if item[0] not in lNestedParam:
                        lNestedParam.append(item[0])
                lNestedBase = []
                tmpList = []
                for nestedParam in lNestedParam:
                    if nestedParam.count("${") > 1:
                        tmpNested = nestedParam
                        if "[" in tmpNested:
                            pattern = "\[\s*'*\s*(\${\s*[0-9A-Za-z\.\-_${}\[\]]*\s*})\s*'*\s*\]"
                            lNestedBase.append(re.findall(pattern, tmpNested)[0])
                            for item in re.findall(pattern, tmpNested):
                                tmpItem = item
                                while tmpItem.count("${") > 1:
                                    newItem = re.sub("(\${\s*" + variablePattern + "\s*})", "str(\\1)", item)
                                    tmpNested = tmpNested.replace(item, newItem)
                                    item = newItem
                                    tmpItem = re.sub("(str\(.+\))", "", item)
                                sInputStr = sInputStr.replace(nestedParam, tmpNested)
                                patternItem = re.sub(r'([$()\[\]])', r'\\\1', item)
                                tmpNested = re.sub("(" + patternItem + ")", "str(\\1)", tmpNested)
                                sInputStr = re.sub("(" + patternItem + ")", "str(\\1)", sInputStr)
                            pattern = re.sub(r'([$()\[\]])', r'\\\1', tmpNested)
                            sInputStr = re.sub("(" + pattern + ")", "str(\\1)", sInputStr)
                            tmpList.append("str(" + tmpNested + ")")
                        else:
                            pattern = "(\${\s*" + variablePattern + "\s*})"
                            lNestedBase.append(re.findall(pattern, tmpNested)[0])
                            for item in re.findall(pattern, tmpNested):
                                patternItem = re.sub(r'([$()\[\]])', r'\\\1', item)
                                tmpNested = re.sub("(" + patternItem + ")", "str(\\1)", tmpNested)
                                sInputStr = re.sub("(" + patternItem + ")", "str(\\1)", sInputStr)
                            pattern = re.sub(r'([$()\[\]])', r'\\\1', tmpNested)
                            sInputStr = re.sub("(" + pattern + ")", "str(\\1)", sInputStr)
                            tmpList.append("str(" + tmpNested + ")")
                    else:
                        tmpList.append("str(" + nestedParam + ")")
                        nestedBasePattern = re.sub(r'([$()\[\]])', r'\\\1', nestedParam)
                        nestedBasePattern = nestedBasePattern.replace("{", "\{")
                        nestedBasePattern = nestedBasePattern.replace("}", "\}")
                        sInputStr = re.sub("(" + nestedBasePattern + ")", "str(\\1)", sInputStr)
                        lNestedBase.append(nestedParam)
                for nestedBase in lNestedBase:
                    self.lNestedParams.append(nestedBase)

                sInputStr = __recursiveNestedHandling(sInputStr, tmpList)
            elif "," in sInputStr:
                if not re.match("^\s*\".+\"\s*$", sInputStr):
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"Invalid nested parameter format: {sInputStr} - The double quotes are missing!!!")
                listPattern = "^\s*(\"*" + nestedPattern + "\"*\s*,+\s*|" + valueStrPattern + "\s*,+\s*|" + valueNumberPattern + "\s*,+\s*)+" + \
                            "(\"*" + nestedPattern + "\"*\s*,*\s*|" + valueStrPattern + "\s*,*\s*|" + valueNumberPattern + "\s*,*\s*)*\]*}*\s*$"
                lNestedParam = re.findall("(" + nestedPattern + ")", sInputStr)
                for nestedParam in lNestedParam:
                    self.lNestedParams.append(nestedParam[0])
                if re.match(listPattern, sInputStr.lower()):
                    items = sInputStr.split(",")
                    newInputStr = ''
                    for item in items:
                        tmpItem = item
                        if "${" in item:
                            if not re.match("^\s*\"*" + nestedPattern + "\"*\]*}*\s*$", item):
                                self.__reset(bCleanGlobalVars=True)
                                raise Exception(f"Invalid nested parameter format: {item}")
                            elif re.match("^\s*\".*" + nestedPattern + ".*\"\s*$", item):
                                item = re.sub("(" + nestedPattern + ")", "str(\\1)", item)
                                tmpList = []
                                for subItem in re.findall("(str\(" + nestedPattern + "\))", item):
                                    tmpList.append(subItem[0])
                                item = __recursiveNestedHandling(item, tmpList)
                            elif re.match("^\s*" + nestedPattern + "\s*\]*}*\s*$", item):
                                item = re.sub("(" + nestedPattern + ")", "\"\\1\"", item)
                                nestedParam = re.sub("^\s*\"(.+)\"\s*.*$", "\\1", item)
                                self.lNestedParams.append(nestedParam)
                        newInputStr = newInputStr + item if tmpItem==items[len(items)-1] else newInputStr + item + ","
                    sInputStr = newInputStr
            elif re.search("\${\s*}", sInputStr) or re.search("\${.+}\.", sInputStr) \
                or (nestedKey and (sInputStr.count("{") != sInputStr.count("}") or sInputStr.count("[") != sInputStr.count("]"))):
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid parameter format: {sInputStr}")
            elif nestedKey and re.match("^\s*\${[^\(\)\!@#%\^\&\-\+\/\\\=`~\?]+[}\[\]]+\s*$", sInputStr):
                sInputStr = re.sub("^\s*(\${[^\(\)\!@#%\^\&\-\+\/\\\=`~\?]+[}\[\]]+)\s*$", "\"\\1\"", sInputStr)
            else:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"Invalid nested parameter format: {sInputStr} - The double quotes are missing!!!")

        sOutput = sInputStr
        return sOutput

    def __checkDotInParamName(self, oJson : dict):
        '''
   This is recrusive funtion collects all parameters which contain "." in the name.

**Args:**
   **oJson** (*dict*)
   Json object which want to collect all parameter's name contained "."

**Returns:**
   **None**
        '''
        for k, v in oJson.items():
            if "." in k and k not in self.lDotInParamName:
                self.lDotInParamName.append(k)
            if isinstance(v, dict):
                self.__checkDotInParamName(v)

    def jsonLoad(self, jFile : str, masterFile : bool = True):
        '''
   This function is the entry point of JsonPreprocessor.

   It loads the json file, preprocesses it and returns the preprocessed result as data structure.

**Args:**

   **jFile** (*string*)

      Relative/absolute path to main json file.

      ``%envvariable%`` and ``${envvariable}`` can be used, too in order to access environment variables.

**Returns:**

   **oJson** (*dict*)

      Preprocessed json file(s) as dictionary data structure
        '''
        
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
            pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[+\s*'[0-9A-Za-z\._]+'\s*\]+|\[+\s*\d+\s*\]+)*"
            tmpDict = copy.deepcopy(dInput)
            for k, v in tmpDict.items():
                if isinstance(v, list) and v[0]==CNameMangling.DUPLICATEDKEY_01.value:
                    i=1
                    dupKey = ''
                    if re.search(pattern, k):
                        varPattern = "[0-9A-Za-z_]+[0-9A-Za-z\-_]*"
                        dupKey = re.search("\.(" + varPattern + ")\s*}\s*$|\['(" + varPattern + ")'\]\s*$", k)[1]
                    if dupKey != '' and dupKey is not None:
                        tmpKey = dupKey
                    else:
                        tmpKey = k
                    tmpPattern = "\${\s*" + tmpKey + "\s*}|\${\s*" + tmpKey + "\.|\[\s*'"+ tmpKey + "'\s*\]|\." + tmpKey + "\.*"
                    if not re.search(pattern, str(v[-1])) or not re.search(tmpPattern, str(v[-1])):
                        dInput[k] = v[-1]
                        continue
                    while i < len(v):
                        bRecursiveKey = False    
                        if re.search(pattern, str(v[i])) and i>1:
                            if isinstance(v[i], str):
                                if re.search(tmpPattern, v[i]) or tmpKey in v[i]:
                                    v[i] = re.sub(tmpKey, tmpKey + CNameMangling.DUPLICATEDKEY_02.value + str(i-1), v[i])
                                    bRecursiveKey = True
                            if isinstance(v[i], list):
                                newList = []
                                for item in v[i]:
                                    if re.search(tmpPattern, item) or tmpKey in item:
                                        item = re.sub(tmpKey, tmpKey + CNameMangling.DUPLICATEDKEY_02.value + str(i-1), item)
                                        bRecursiveKey = True
                                    newList.append(item)
                                v[i] = newList
                                del newList
                            if bRecursiveKey:
                                if dupKey == '':
                                    k1 = k + CNameMangling.DUPLICATEDKEY_02.value + str(i)
                                else:
                                    k1 = re.sub(dupKey, dupKey + CNameMangling.DUPLICATEDKEY_02.value + str(i), k)
                                dInput[k1] = v[i] 
                        else:
                            if dupKey == '':
                                k1 = k + CNameMangling.DUPLICATEDKEY_02.value + str(i)
                            else:
                                k1 = re.sub(dupKey, dupKey + CNameMangling.DUPLICATEDKEY_02.value + str(i), k)
                            dInput[k1] = v[i]
                        i+=1
                    if dupKey != '' and CNameMangling.DUPLICATEDKEY_02.value in str(v):
                        del dInput[k]
                        k = re.sub(dupKey, dupKey + CNameMangling.DUPLICATEDKEY_00.value, k)
                    dInput[k] = v[1] if len(v)==2 else v
                if isinstance(v, dict):
                    dInput[k] = __handleDuplicatedKey(v)
            del tmpDict
            return dInput
        
        def __removeDuplicatedKey(dInput : dict) -> dict:
            if isinstance(dInput, dict):
                for k, v in list(dInput.items()):
                    if CNameMangling.DUPLICATEDKEY_02.value in k:
                        del dInput[k]
                    else:
                        __removeDuplicatedKey(v)
            elif isinstance(dInput, list):
                for item in dInput:
                    __removeDuplicatedKey(item)

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

        pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+)*"
        sJsonDataUpdated = ""
        for line in sJsonData.splitlines():
            if line == '' or line.isspace():
                continue
            try:
                listDummy = shlex.split(line)
            except Exception as error:
                self.__reset(bCleanGlobalVars=True)
                raise Exception(f"\n{str(error)} in line: '{line}'")

            if re.search(pattern, line):
                lNestedVar = re.findall("\${\s*([0-9A-Za-z_]+[0-9A-Za-z\.\-_]*)\s*}", line)
                for nestedVar in lNestedVar:
                    if nestedVar[0].isdigit():
                        self.__reset(bCleanGlobalVars=True)
                        raise Exception(f"Invalid parameter format in line: {line.strip()}")
                tmpList = re.findall("(\"[^\"]+\")", line)
                line = re.sub("(\"[^\"]+\")", CNameMangling.COLONS.value, line)
                indexPattern = "\[\s*-*\d*\s*:\s*-*\d*\s*\]"
                if re.search(indexPattern, line):
                    indexList = re.findall(indexPattern, line)
                    line = re.sub("(" + indexPattern + ")", CNameMangling.LISTINDEX.value, line)
                items = re.split("\s*:\s*", line)
                newLine = ""
                i=0
                for item in items:
                    nestedKey = False
                    nestedKeyPattern = "^\s*,\s*\${.+[\]}]\s*$"
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
                    if re.search("^\s*\[.+\]\s*,*\s*$", item) and item.count('[')==item.count(']'):
                        item = item.strip()
                        bLastElement = True
                        if item.endswith(","):
                            bLastElement = False
                        item = re.sub("^\[", "", item)
                        item = re.sub("\s*\]\s*,*$", "", item)
                        newSubItem = __handleListElements(item)
                        newSubItem = "[" + newSubItem + "]" if bLastElement else "[" + newSubItem + "],"
                    elif re.search("^\s*\[.*\${.+", item):
                        item = item.strip()
                        item = re.sub("^\[", "", item)
                        newSubItem = __handleListElements(item)
                        newSubItem = "[" + newSubItem
                    elif re.search("]\s*,*\s*", item) and item.count('[') < item.count(']'):
                        item = item.rstrip()
                        bLastElement = True
                        if item.endswith(","):
                            bLastElement = False
                        item = re.sub("\s*\]\s*,*$", "", item)
                        newSubItem = __handleListElements(item)
                        newSubItem = newSubItem + "]" if bLastElement else newSubItem + "],"
                    else:
                        newSubItem = self.__checkAndUpdateKeyValue(item, nestedKey)
                    if i<len(items):
                        newLine = newLine + newSubItem + " : "
                    else:
                        newLine = newLine + newSubItem
                for nestedParam in self.lNestedParams:
                    tmpNestedParam = nestedParam.replace("$", "\$")
                    tmpNestedParam = tmpNestedParam.replace("[", "\[")
                    tmpNestedParam = tmpNestedParam.replace("]", "\]")
                    if re.search("(\s*\"str\(" + tmpNestedParam + "\)\"\s*:)", newLine.replace(CNameMangling.STRINGCONVERT.value, '')) \
                        or re.search("(\s*\"" + tmpNestedParam + "\"\s*:)", newLine.replace(CNameMangling.STRINGCONVERT.value, '')):
                        self.lNestedParams.remove(nestedParam)
                sJsonDataUpdated = sJsonDataUpdated + newLine + "\n"
            else:
                if "${" in line:
                    self.__reset(bCleanGlobalVars=True)
                    invalidPattern1 = "\${\s*[0-9A-Za-z\._]*\[.+\][0-9A-Za-z\._]*\s*}"
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

        try:
            oJson = json.loads(sJsonDataUpdated,
                               cls=CJSONDecoder,
                               object_pairs_hook=self.__processImportFiles)
        except Exception as error:
            self.__reset(bCleanGlobalVars=True)
            raise Exception(f"JSON file: {jFile}\n{error}")

        self.__checkDotInParamName(oJson)

        if masterFile:
            oJson = __handleDuplicatedKey(oJson)
            for k, v in oJson.items():
                if k in self.lDataTypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                globals().update({k:v})
            oJson, bNested = self.__updateAndReplaceNestedParam(oJson)
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

            # Checking availability of nested parameters before updating and replacing.
            for param in self.lNestedParams:
                param = self.__checkParamName(param)
                param = re.sub("\${", "$${", param)
                parseNestedParam = self.__nestedParamHandler(param)
                tmpParseNestedParam = re.sub("'*\${\s*(.*?)\s*}'*", '\\1', parseNestedParam[0])
                sExec = "value = " + tmpParseNestedParam if isinstance(tmpParseNestedParam, str) else \
                        "value = " + str(tmpParseNestedParam)
                try:
                    ldict = {}
                    exec(sExec, globals(), ldict)
                except:
                    self.__reset(bCleanGlobalVars=True)
                    raise Exception(f"The variable '{parseNestedParam[0]}' is not available!")
                
            self.__reset()
            __removeDuplicatedKey(oJson)
        return oJson

    def jsonDump(self, oJson : dict, outFile : str) -> str:
        '''
   This function writes the content of a Python dictionary to a file in JSON format and returns a normalized path to this JSON file.

**Args:**

   **oJson** (*dictionary*)

      Json/Dictionary object.

   **outFile** (*string*)

      Path and name of the JSON output file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

   **outFile** (*string*)

      Normalized path and name of the JSON output file.
        '''

        outFile = CString.NormalizePath(outFile, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        jsonObject = json.dumps(oJson, ensure_ascii=False, indent=4)
        try:
            with open(outFile, "w", encoding='utf-8') as f:
                f.write(jsonObject)
        except Exception as error:
            errorMsg = f"Could not write a JSON file '{outFile}'! Reason: {error}"
            raise Exception(errorMsg)

        return outFile