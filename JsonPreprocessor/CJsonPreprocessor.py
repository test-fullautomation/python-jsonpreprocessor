#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
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

class CSyntaxType():
    python = "python"
    json = "json"

NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))

class CPythonJSONDecoder(json.JSONDecoder):
    """ Add below python values when scanning json data

    +---------------+-------------------+
    | True          | True              |
    +---------------+-------------------+
    | False         | False             |
    +---------------+-------------------+
    | None          | None              |
    +---------------+-------------------+
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_once = self.custom_scan_once

    def _custom_scan_once(self, string, idx):
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

        m = NUMBER_RE.match(string, idx)
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

    def custom_scan_once(self, string, idx):
        try:
            return self._custom_scan_once(string, idx)
        finally:
            self.memo.clear()

class CJsonPreprocessor():
    '''
    CJsonPreprocessor helps to handle configuration file as json format:
        - Allow comment within json file
        - Allow import json file within json file
    '''
    def __init__(self, syntax=CSyntaxType.json, currentCfg={}):
        self.lImportedFiles = []
        self.recursive_level = 0
        self.syntax = syntax
        self.currentCfg = currentCfg
        self.lUpdatedParams = []
            

    '''
    Method: __processImportFiles this is custom decorder of object_pairs_hook function.
    This method helps to import json file which is provided in '[import]' keyword into current json file.
    Returns:
        Dictionary is parsed from json file.
    '''
    def __processImportFiles(self, input_data):
        out_dict = {}
        for key, value in input_data:
            if re.match('^\s*\[\s*import\s*\]\s*', key.lower()):
                abs_path_file = os.path.abspath(value)
                
                # Use recursive_level and lImportedFiles to avoid cyclic import
                self.recursive_level = self.recursive_level + 1     # increase recursive level
                # length of lImportedFiles should equal to recursive_level
                self.lImportedFiles = self.lImportedFiles[:self.recursive_level]
                if abs_path_file in self.lImportedFiles:
                    raise Exception('Cyclic imported json file \'%s\'' %str(abs_path_file))
                
                oJsonImport = self.jsonLoad(value, masterFile=False)
                out_dict.update(oJsonImport)
                self.recursive_level = self.recursive_level - 1     # descrease recursive level
            else:
                out_dict[key] = value
        return out_dict

    '''
    Method: __removeComments loads json config file which allows comments inside
    Args:
        jsonFile: string
    Returns:
        lJsonData: list, list of string data from jsonFile after removing comment(s).
    '''
    def __removeComments(self, jsonFile):
        jsonPath = ''
        if '/' in jsonFile:
            for item in jsonFile.split('/')[:-1]:
                jsonPath += item + '/'
        else:
            for item in jsonFile.split('\\')[:-1]:
                jsonPath += item + '\\'
      
        '''
        Removes comment parts in json file then store in temporary json file
        '''
        lJsonData = []
        
        with open(jsonFile) as fr:
            for line in fr:
                if re.match('^\s*//', line):
                    continue
                elif '//' in line:
                    reEx1 = re.search("(\s*{*\s*\'.+\')\s*:\s*(\'.+\'\s*,*)*\s*(.*)", line)
                    if reEx1 is None:
                        reEx1 = re.search("(\s*{*\s*\".+\")\s*:\s*(\".+\"\s*,*)*\s*(.*)", line)
                    if reEx1 is None:
                        line = re.sub('//.*', '', line)
                    elif reEx1.group(1) is not None and reEx1.group(2) is not None:
                        line = reEx1.group(1) + ": " + reEx1.group(2) if reEx1.group(3) is None else \
                               reEx1.group(1) + ": " + reEx1.group(2) + re.sub('//.*', '', reEx1.group(3))
                    else:
                        reEx2 = re.search("(\s*{*\s*\'.+\')\s*:\s*(.+,*)\s*//\s*.*", line)
                        if reEx2 is None:
                            reEx2 = re.search("(\s*{*\s*\".+\")\s*:\s*(.+,*)\s*(//\s*.*)*", line)
                        if reEx2 is not None:
                            line = reEx2.group(1) + ": " + re.sub('//.*', '', reEx2.group(2))
                            
                lJsonData.append(line)
        return lJsonData, jsonPath
    
    '''
    private __nestedParamHandler: This method handles the nested variable in param names or value
                                  in updated json config file.
    Args:
        sInputStr: string - param name or value which contains nested variable
    Returns:
        sStrHandled: string
    '''
    def __nestedParamHandler(self, sInputStr):
        
        #globals().update(currentCfg)
        referVars = re.findall('(\${\s*.*?\s*})', sInputStr)
        if len(referVars) > 1:
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
                        raise Exception('The variable %s is not available' % (var))
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
                    raise Exception('The variable %s is not available!!!' % (fullVariable))
                pattern = re.sub('\[', '\\[', fullVariable)
                pattern = re.sub('\]', '\\]', pattern)
                sInputStr = re.sub('\\' + pattern, '\'' + tmpValue + '\'', sInputStr) if isinstance(tmpValue, str) else \
                            re.sub('\\' + pattern, '\'' + str(tmpValue) + '\'', sInputStr)
            sStrHandled = sUpdateVar + sInputStr
            return sStrHandled
                    
        else:
            pattern = '(\\' + referVars[0] + '\s*\[\s*.*?\s*\])'
            variable = re.findall(pattern, sInputStr)
            if variable == []:
                sStrHandled = referVars[0]
                return sStrHandled
            else:
                fullVariable = variable[0]
                while variable != []:
                    pattern = pattern[:-1] + '\[\s*.*?\s*\])'
                    variable = re.findall(pattern, sInputStr)
                    if variable != []:
                        fullVariable = variable[0]
                sStrHandled = fullVariable
                return sStrHandled
            
    '''
    private __updateAndReplaceNestedParam: this method replaces all nested params in key and value of Json object
    Args:
        oJson: dict
        currentCfg: dict
    Returns:
        oJsonOut: dict
    '''
    def __updateAndReplaceNestedParam(self, oJson, recursive=False):
        
        if bool(self.currentCfg) and not recursive:
            for k, v in self.currentCfg.items():
                globals().update({k:v})
        
        tmpJson = {}            
        bNested = False
        for k, v in oJson.items():
            if re.match('^\s*\${\s*', k.lower()):
                keyAfterProcessed = self.__nestedParamHandler(k)
                k = re.sub('^\s*\${\s*(.*?)\s*}', '\\1', keyAfterProcessed)
                bNested = True
                
            if isinstance(v, dict):
                v = self.__updateAndReplaceNestedParam(v, recursive=True)
                if bNested:
                    if '[' in k:
                        sExec = k + " = \'" + v + "\'" if isinstance(v, str) else k + " = " + str(v) 
                        try:
                            exec(sExec, globals())
                        except:
                            raise Exception("Could not set variable \'%s\' with value \'%s\'" %(k, v))
                    else:
                        tmpJson[k] = v 
                    bNested = False
                else:
                    tmpJson[k] = v
            
            elif isinstance(v, str) and re.match('^.*\s*\${\s*', v.lower()):
                
                valueAfterProcessed = self.__nestedParamHandler(v)
                tmpValueAfterProcessed = re.sub('\\${\s*(.*?)\s*}', '\\1', valueAfterProcessed)
                sExec = "value = " + tmpValueAfterProcessed if isinstance(tmpValueAfterProcessed, str) else \
                        "value = " + str(tmpValueAfterProcessed)

                try:
                    ldict = {}
                    exec(sExec, globals(), ldict)
                    v = ldict['value'] if v.strip()==valueAfterProcessed else \
                        v.replace(valueAfterProcessed, str(ldict['value']))
                except:
                    raise Exception('The variable %s is not available!!!' % (tmpValueAfterProcessed))
                
                if bNested:
                    if '[' in k:
                        sExec = k + " = \'" + v + "\'" if isinstance(v, str) else k + " = " + str(v) 
                        try:
                            exec(sExec, globals())
                        except:
                            raise Exception("Could not set variable \'%s\' with value \'%s\'" %(k, v))
                    else:
                        tmpJson[k] = v 
                    bNested = False
                else:
                    tmpJson[k] = v
                
            else:
                if bNested:
                    if '[' in k:
                        sExec = k + " = \'" + v + "\'" if isinstance(v, str) else k + " = " + str(v) 
                        try:
                            exec(sExec, globals())
                        except:
                            raise Exception("Could not set variable \'%s\' with value \'%s\'" %(k, v))
                    else:
                        tmpJson[k] = v
                    
                    bNested = False
                    
        oJson.update(tmpJson)

        return oJson

    def jsonLoad(self, jFile, masterFile=True):
        '''
        Method: jsonLoad loads the json file then parses to dict object
        
        Args:
            jFile: string, json file input
        Returns:
            oJson: dict
        '''
        try:
            lJsonData, jsonPath = self.__removeComments(jFile)
        except Exception as reason:
            raise Exception("Could not read json configuration file %s due to: %s \n\
                             Please input 'utf-8' format in Json configuration file only" %(jFile, reason))

        currentDir = os.getcwd()
        self.lImportedFiles.append(os.path.abspath(jFile))
        os.chdir(jsonPath)
        CJSONDecoder = None
        if self.syntax != CSyntaxType.json:
            if self.syntax == CSyntaxType.python:
                CJSONDecoder = CPythonJSONDecoder
            else:
                raise Exception('Provided syntax \'%s\' is not supported.' %self.syntax)

        try:
            oJson = json.loads("\n".join(lJsonData), 
                               cls=CJSONDecoder , 
                               object_pairs_hook=self.__processImportFiles)
        except Exception as error:
            raise Exception("JSON configuration file '%s': %s" %(jFile, error))
        
        os.chdir(currentDir)
        if masterFile:
            for k, v in oJson.items():
                globals().update({k:v})
            oJson = self.__updateAndReplaceNestedParam(oJson)
        # oJson['JsonPath'] = jsonPath      # is JsonPath required?
            
        return oJson