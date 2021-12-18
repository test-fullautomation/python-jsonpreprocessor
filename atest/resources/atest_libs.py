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
import os
from os.path import abspath, dirname
from JsonPreprocessor import CJsonPreprocessor
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from dotdict import dotdict


ddictJson = dotdict()

class CJsonDotDict():
    def __init__(self):
        self.lTmpParam = ['ddictJson']
    
    def __del__(self):
        ddictJson = dotdict()
        del self.lTmpParam
    
    def dotdictConvert(self, oJson):
        if len(self.lTmpParam) == 1:
            ddictJson.update(oJson)
        
        for k,v in oJson.items():
            sExec = ""
            if isinstance(v, dict):
                self.lTmpParam.append(k)
                for i in self.lTmpParam:
                    sExec = i if i==self.lTmpParam[0] else sExec + "." + i
                sExec = sExec + " = dotdict(" + str(v) + ")"
                try:
                    exec(sExec, globals())
                except:
                    logger.info("Could not convert: %s to dotdict" %(sExec))
                    pass

                self.dotdictConvert(v)
                
            elif isinstance(v, list):
                n = 0
                for item in v:
                    if isinstance(item, dict):
                        self.lTmpParam.append(k+"["+str(n)+"]")
                        for i in self.lTmpParam:
                            sExec = i if i == self.lTmpParam[0] else sExec + "." + i
                        sExec = sExec + " = dotdict(" + str(item) + ")"
                        try:
                            exec(sExec, globals())
                        except:
                            logger.info("Could not convert: %s to dotdict" %(sExec))
                            pass
                            
                        self.dotdictConvert(item)
                    n = n+1
                
        self.lTmpParam = self.lTmpParam[:-1]
        return ddictJson

oParams = {}
@keyword
def load_json(jsonfile, level=1, variant='default'):
    '''
    This keyword uses to load json file then return json object.
       - Level = 1 -> loads the content of jsonfile.
       - level != 1 -> loads the json file which is set with variant (likes loading
         config level2)
    '''
    curdir = os.getcwd()
    suiteFilePath = BuiltIn().get_variable_value('${SUITE_SOURCE}')
    os.chdir(dirname(suiteFilePath))
    jsonFileDir = dirname(abspath(jsonfile))
    oJsonPreprocessor = CJsonPreprocessor()
    bDotdict = False
    if level == 1:
        oJsonData = oJsonPreprocessor.jsonLoad(jsonfile)
        os.chdir(curdir)
        oParams.update(oJsonData)
        dotdictObj = CJsonDotDict()
        try:
            jsonDotdict = dotdictObj.dotdictConvert(oParams)
            bDotdict = True
        except:
            logger.info("Could not convert json config to dotdict!!!")
            pass
        
        if bDotdict:
            BuiltIn().set_global_variable("${CONFIG}", jsonDotdict)
        else:
            BuiltIn().set_global_variable("${CONFIG}", oParams)
            
        del dotdictObj
        return oJsonData
    else:
        oJsonFristLevel = oJsonPreprocessor.jsonLoad(jsonfile)
        if variant not in oJsonFristLevel:
            BuiltIn().log("The variant: '%s' is not existing." % variant, level="ERROR")
            BuiltIn().log("Existing variants are:", level="ERROR")
            for variant in oJsonFristLevel:
               BuiltIn().log(variant, level="ERROR")   
            os.chdir(curdir)
            return {}
        jsonFileLoaded = jsonFileDir + oJsonFristLevel[variant]['path'] + '/' + oJsonFristLevel[variant]['name']
        oJsonData = oJsonPreprocessor.jsonLoad(jsonFileLoaded)
        os.chdir(curdir)
        oParams.update(oJsonData)
        dotdictObj = CJsonDotDict()
        try:
            jsonDotdict = dotdictObj.dotdictConvert(oParams)
            bDotdict = True
        except:
            logger.info("Could not convert json config to dotdict!!!")
            pass
        
        if bDotdict:
            BuiltIn().set_global_variable("${CONFIG}", jsonDotdict)
        else:
            BuiltIn().set_global_variable("${CONFIG}", oParams)
        del dotdictObj
        return oJsonData
