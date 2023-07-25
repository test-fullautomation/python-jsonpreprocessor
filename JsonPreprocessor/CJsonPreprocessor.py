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

class CSyntaxType():
    python = "python"
    json = "json"

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

    def __init__(self, syntax: CSyntaxType = CSyntaxType.json , currentCfg : dict = {}) -> None:
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
        self.lImportedFiles = []
        self.recursive_level = 0
        self.syntax = syntax
        self.currentCfg = currentCfg
        self.lUpdatedParams = {}
        self.lNestedParams = []
        self.lDotInParamName = []

    def __reset(self) -> None:
        '''
   Reset initial variables which are set in constructor method after master Json file is loaded.
        '''
        self.lImportedFiles = []
        self.recursive_level = 0
        self.lUpdatedParams = {}
        self.lNestedParams = []
        self.lDotInParamName = []

    def __sNormalizePath(self, sPath : str) -> str:
        """
   Python struggles with

      - UNC paths

         e.g. ``\\hi-z4939\ccstg\....``

      - escape sequences in windows paths

         e.g. ``c:\autotest\tuner   \t`` will be interpreted as tab, the result
      after processing it with an regexp would be ``c:\autotest   uner``

   In order to solve this problems any slash will be replaced from backslash
   to slash, only the two UNC backslashes must be kept if contained.

**Args:**

   **sPath** (*string*)

      Absolute or relative path as input.

      Allows environment variables with ``%variable%`` or ``${variable}`` syntax.

**Returns:**

   **sPath** (*string*)

      Normalized path as string
        """
        # make all backslashes to slash, but mask
        # UNC indicator \\ before and restore after.
        def __mkslash(sPath : str) -> str:
            if sPath.strip()=='':
                return ''

            sNPath=re.sub(r"\\\\",r"#!#!#",sPath.strip())
            sNPath=re.sub(r"\\",r"/",sNPath)
            sNPath=re.sub(r"#!#!#",r"\\\\",sNPath)

            return sNPath
            if sPath.strip()=='':
                return ''

        # TML Syntax uses %Name%-syntax to reference an system- or framework
        # environment variable. Linux requires ${Name} to do the same.
        # Therefore change on Linux systems to ${Name}-syntax to make
        # expandvars working here, too.
        # This makes same TML code working on both platforms
        if platform.system().lower()!="windows":
            sPath=re.sub("%(.*?)%","${\\1}",sPath)

        #in a windows system normpath turns all slashes to backslash
        #this is unwanted. Therefore turn back after normpath execution.
        sNPath=os.path.normpath(os.path.expandvars(sPath.strip()))
        #make all backslashes to slash, but mask
        #UNC indicator \\ before and restore after.
        sNPath=__mkslash(sNPath)

        return sNPath


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
                abs_path_file = os.path.abspath(value)

                # Use recursive_level and lImportedFiles to avoid cyclic import
                self.recursive_level = self.recursive_level + 1     # increase recursive level

                # length of lImportedFiles should equal to recursive_level
                self.lImportedFiles = self.lImportedFiles[:self.recursive_level]
                if abs_path_file in self.lImportedFiles:
                    raise Exception(f"Cyclic imported json file '{abs_path_file}'!")

                oJsonImport = self.jsonLoad(abs_path_file, masterFile=False)
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
                    if k1 == key:
                        del out_dict[k1]
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
                sInput = re.sub(param, "JPavoidDataType_" + param, sInput, count=1)
            if "." in param and "JPavoidDataType_" + param.split('.')[0] in globals():
                sInput = re.sub(param, "JPavoidDataType_" + param, sInput, count=1)
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
                dotdictVariable = re.sub('\${\s*(.*?)\s*}', '\\1', referVar)
                lDotdictVariable = dotdictVariable.split(".")
                lParams = self.__handleDotdictFormat(lDotdictVariable, [])
                sParam = '${' + lParams[0] + '}'
                lParams.pop(0)
                for item in lParams:
                    sParam = sParam + "['" + item + "']"
                sInputStr = re.sub('\${\s*([^\}]*)\s*}', sParam, sInputStr)
                referVar = re.findall('(\${\s*.*?\s*})', sInputStr)[0]
            pattern = '(\\' + referVar + '\s*\[\s*.*?\s*\])'
            variable = re.findall(pattern, sInputStr)
            if variable == []:
                return referVar
            else:
                fullVariable = variable[0]
                while variable != []:
                    pattern = pattern[:-1] + '\[\s*.*?\s*\])'
                    variable = re.findall(pattern, sInputStr)
                    if variable != []:
                        fullVariable = variable[0]
                referVar = fullVariable
                return referVar


        pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}"
        referVars = re.findall("(" + pattern + ")", sInputStr)
        lNestedParam = []
        if len(referVars) > 1:
            if not bKey:
                for referVar in referVars:
                    lNestedParam.append(__referVarHandle(referVar, sInputStr)) 
                return lNestedParam
            else:
                sUpdateVar =  referVars[0]
                referVars = referVars[1:]
                sInputStr = re.sub('\\' + sUpdateVar, '', sInputStr, count=1)
                for var in referVars[::-1]:
                    pattern = '(\\' + var + '\s*\[\s*.*?\s*\])'
                    variable = re.findall(pattern, sInputStr)
                    if variable == []:
                        sExec = "value = " + re.search('^\s*\${(\s*.*?)}', var).group(1)
                        try:
                            ldict = {}
                            exec(sExec, globals(), ldict)
                            tmpValue = ldict['value']
                        except:
                            raise Exception(f"The variable '{var}' is not available!")
                        sInputStr = re.sub('\\' + var, tmpValue, sInputStr) if isinstance(tmpValue, str) else \
                                    re.sub('\\' + var, str(tmpValue), sInputStr)
                        continue
                    while variable != []:
                        fullVariable = variable[0]
                        pattern = pattern[:-1] + '\[\s*.*?\s*\])'
                        variable = re.findall(pattern, sInputStr)
                        if variable != []:
                            fullVariable = variable[0]
                    sExec = "value = " + re.sub('\${\s*(.*?)\s*}', '\\1', fullVariable)
                    try:
                        ldict = {}
                        exec(sExec, globals(), ldict)
                        tmpValue = ldict['value']
                    except:
                        raise Exception(f"The variable '{fullVariable}' is not available!")
                    pattern = re.sub('\[', '\\[', fullVariable)
                    pattern = re.sub('\]', '\\]', pattern)
                    sInputStr = re.sub('\\' + pattern, '\'' + tmpValue + '\'', sInputStr) if isinstance(tmpValue, str) else \
                                re.sub('\\' + pattern, '\'' + str(tmpValue) + '\'', sInputStr)
                sKeyHandled = sUpdateVar + sInputStr
                lNestedParam.append(sKeyHandled)
                return lNestedParam
        else:
            lNestedParam.append(__referVarHandle(referVars[0], sInputStr))
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
                if '[' in k:
                    sExec = k + " = \"" + v + "\"" if isinstance(v, str) else k + " = " + str(v)
                    try:
                        exec(sExec, globals())
                    except:
                        raise Exception(f"Could not set variable '{k}' with value '{v}'!")

                    if "JPavoidDataType_" in k:
                        k = re.sub("JPavoidDataType_", "", k)
                    if isinstance(v, str):
                        sExec = "oJson['" + k.split('[', 1)[0] + "'][" + k.split('[', 1)[1] + " = \"" + v + "\""
                    else:
                        sExec = "oJson['" + k.split('[', 1)[0] + "'][" + k.split('[', 1)[1] + " = " + str(v)
                    try:
                        exec(sExec, globals())
                    except:
                        pass
                else:
                    if "JPavoidDataType_" in k:
                        k = re.sub("JPavoidDataType_", "", k)
                    oJson[k] = v

            else:
                if bNested:
                    if "JPavoidDataType_" in k:
                        k = re.sub("JPavoidDataType_", "", k) 
                    oJson[k] = v

        if bool(self.currentCfg) and not recursive:
            for k, v in self.currentCfg.items():
                if k in self.lDataTypes:
                    k = "JPavoidDataType_" + k
                globals().update({k:v})

        tmpJson = copy.deepcopy(oJson)
        for k, v in tmpJson.items():
            keyNested = ''
            if re.match('.*\${\s*', k.lower()):
                keyNested = k
                pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[\s*.+\s*\])*"
                if re.match("str\(\s*\${.+", k.lower()):
                    k = re.sub("str\(\s*(" + pattern + ")\s*\)", "\\1", k)
                if len(re.findall(pattern, k.lower())) > 1 or k.count('{') != k.count('}'):
                    raise Exception(f"Could not overwrite parameter {k} due to wrong format.\n \
          Please check key '{k}' in config file!!!")
                k = self.__checkParamName(k)
                keyAfterProcessed = self.__nestedParamHandler(k, bKey=True)
                k = re.sub('^\s*\${\s*(.*?)\s*}', '\\1', keyAfterProcessed[0])

            if isinstance(v, dict):
                v, bNested = self.__updateAndReplaceNestedParam(v, bNested, recursive=True)

            elif isinstance(v, list):
                tmpValue = []
                for item in v:
                    if isinstance(item, str) and re.match('^.*\s*\${\s*', item.lower()):
                        bStringValue = False
                        bNested = True
                        if re.match("str\(\s*\${.+", item.lower()):
                            item = re.sub("str\(\s*(\${.+)\s*\)", "\\1", item)
                            bStringValue = True
                        item = self.__checkParamName(item)
                        itemAfterProcessed = self.__nestedParamHandler(item)
                        tmpItemAfterProcessed = re.sub('\${\s*(.*?)\s*}', '\\1', itemAfterProcessed[0])
                        sExec = "value = " + tmpItemAfterProcessed if isinstance(tmpItemAfterProcessed, str) else \
                                "value = " + str(tmpItemAfterProcessed)
                        try:
                            ldict = {}
                            exec(sExec, globals(), ldict)
                            if bStringValue:
                                item = str(ldict['value'])
                            else:
                                item = ldict['value']
                        except:
                            raise Exception(f"The variable '{itemAfterProcessed[0]}' is not available!")

                    tmpValue.append(item)
                v = tmpValue

            elif isinstance(v, str):
                if re.match('^.*\s*\${\s*', v.lower()):
                    bStringValue = False
                    bNested = True
                    pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[\s*.+\s*\])*"
                    if re.search("(str\(\s*" + pattern + "\))", v.lower()):
                        v = re.sub("str\(\s*(" + pattern + ")\s*\)", "\\1", v)
                        bStringValue = True
                    v = self.__checkParamName(v)
                    valueAfterProcessed = self.__nestedParamHandler(v)
                    for valueProcessed in valueAfterProcessed:
                        tmpValueAfterProcessed = re.sub('\\${\s*(.*?)\s*}', '\\1', valueProcessed)
                        sExec = "value = " + tmpValueAfterProcessed if isinstance(tmpValueAfterProcessed, str) else \
                                "value = " + str(tmpValueAfterProcessed)
                        try:
                            ldict = {}
                            exec(sExec, globals(), ldict)
                            if bStringValue:
                                v = re.sub("(\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[\s*.+\s*\])*)", str(ldict['value']), v, count=1)
                            else:
                                v = ldict['value']
                        except:
                            raise Exception(f"The variable '{valueProcessed}' is not available!")

            __jsonUpdated(k, v, oJson, bNested, keyNested)
            if keyNested != '':
                self.lUpdatedParams.update({k:v})

        return oJson, bNested

    def __checkAndUpdateKeyValue(self, sInputStr: str) -> str:
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
        pattern = "\${\s*[0-9A-Za-z_]+[0-9A-Za-z\.\-_]*\s*}(\[\s*.+\s*\])*"
        if re.match("\s*\".+\"\s*", sInputStr.lower()) and re.search("(" + pattern + ")*", sInputStr.lower()):
            lNestedParam = re.findall("(" + pattern + ")", sInputStr)
            for nestedParam in lNestedParam:
                self.lNestedParams.append(nestedParam[0])
            sInputStr = re.sub("(" + pattern + ")", "str(\\1)", sInputStr)
        elif re.search("^\s*" + pattern + "\s*\]*\}*,*\s*$", sInputStr.lower()):
            sInputStr = re.sub("(" + pattern + ")", "\"\\1\"", sInputStr)
            nestedParam = re.sub("^\s*\"(.+)\"\s*.*$", "\\1", sInputStr)
            self.lNestedParams.append(nestedParam)
        else:
            if len(re.findall(pattern, sInputStr.lower()))>1:
                raise Exception(f"Key name or value is a mix of nested parameters and hard coded parts. \n \
          The entire expression {sInputStr.strip()} must be enclosed in quotes")

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

        jFile=jFile.strip()

        if not re.match("^[a-zA-Z]:",jFile) and not re.match("^[\\/]",jFile):
            jFile=self.__sNormalizePath(os.path.dirname(sys.argv[0])+"/"+jFile)

        if  not(os.path.isfile(jFile)):
            raise Exception(f"File '{jFile}' is not existing!")

        self.lImportedFiles.append(os.path.abspath(jFile))
        (jsonPath,tail)=os.path.split(jFile)

        try:
            sJsonData= self.__load_and_removeComments(os.path.abspath(jFile))
        except Exception as reason:
            raise Exception(f"Could not read json file '{jFile}' due to: '{reason}'!")

        sJsonDataUpdated = ""
        for line in sJsonData.splitlines():
            if line == '' or line.isspace():
                continue
            if re.search("\${.+}", line):
                items = re.split("\s*:\s*", line)
                newLine = ""
                if len(items) > 1:
                    if re.match("^\s*\${.+", items[0]):
                        items[0] = '"' + items[0].strip() + '"'
                        newLine = items[0] + ": "
                        items.pop(0)
                else:
                    items[0] = items[0].strip()
                i=0
                for item in items:
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
                        newSubItem = self.__checkAndUpdateKeyValue(item)
                    if i<len(items):
                        newLine = newLine + newSubItem + " : "
                    else:
                        newLine = newLine + newSubItem
                for nestedParam in self.lNestedParams:
                    tmpNestedParam = nestedParam.replace("$", "\$")
                    tmpNestedParam = tmpNestedParam.replace("[", "\[")
                    tmpNestedParam = tmpNestedParam.replace("]", "\]")
                    if re.search("(\s*\"str\(" + tmpNestedParam + "\)\"\s*:)", newLine) \
                        or re.search("(\s*\"" + tmpNestedParam + "\"\s*:)", newLine):
                        self.lNestedParams.remove(nestedParam)
                sJsonDataUpdated = sJsonDataUpdated + newLine + "\n"
            else:
                sJsonDataUpdated = sJsonDataUpdated + line + "\n"

        currentDir = os.getcwd()
        os.chdir(jsonPath)

        CJSONDecoder = None
        if self.syntax != CSyntaxType.json:
            if self.syntax == CSyntaxType.python:
                CJSONDecoder = CPythonJSONDecoder
            else:
                raise Exception(f"Provided syntax '{self.syntax}' is not supported.")

        try:
            oJson = json.loads(sJsonDataUpdated,
                               cls=CJSONDecoder,
                               object_pairs_hook=self.__processImportFiles)
        except Exception as error:
            raise Exception(f"json file '{jFile}': '{error}'")

        os.chdir(currentDir)

        self.__checkDotInParamName(oJson)

        if masterFile:
            for k, v in oJson.items():
                if k in self.lDataTypes:
                    k = "JPavoidDataType_" + k
                globals().update({k:v})
            oJson, bNested = self.__updateAndReplaceNestedParam(oJson)
            for k, v in self.lUpdatedParams.items():
                if '[' in k:
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
                parseNestedParam = self.__nestedParamHandler(param)
                tmpParseNestedParam = re.sub('\\${\s*(.*?)\s*}', '\\1', parseNestedParam[0])
                sExec = "value = " + tmpParseNestedParam if isinstance(tmpParseNestedParam, str) else \
                        "value = " + str(tmpParseNestedParam)
                try:
                    ldict = {}
                    exec(sExec, globals(), ldict)
                except:
                    raise Exception(f"The variable '{parseNestedParam[0]}' is not available!")
                
            self.__reset()

        return oJson
