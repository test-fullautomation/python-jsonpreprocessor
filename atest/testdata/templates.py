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
PROPERCONFIGFILE = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

IMPORTEDFILE01 = {
    'gPreprolIntParam': 1,
    'gPreproFloatParam': 1.332,
    'gPreproString': 'This is a string',
    'gPreproStructure': {
        'general': 'general'
    },
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

IMPORTEDFILE02 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'gPreprolIntParam': 1,
    'gPreproFloatParam': 1.332,
    'gPreproString': 'This is a string',
    'gPreproStructure': {
        'general': 'general'
    },
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

IMPORTEDFILE03 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01',
    'gPreprolIntParam': 1,
    'gPreproFloatParam': 1.332,
    'gPreproString': 'This is a string',
    'gPreproStructure': {
        'general': 'general'
    }
}

IMPORTEDFILE04 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'gPreprolIntParam': 1,
        'gPreproFloatParam': 1.332,
        'gPreproString': 'This is a string',
        'gPreproStructure': {
            'general': 'general'
        },
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

IMPORTEDFILES01 = {
    'gPreprolIntParam': 1,
    'gPreproFloatParam': 1.332,
    'gPreproString': 'This is a string',
    'gPreproStructure': {
        'general': 'general'
    },
    'file02IntParam': 100,
    'file02FloatParam': 0.145,
    'file02StructureParam': {
        'iTestParam': 999,
        'general': {
            'general01': 'general01',
            'general02': 10
        }
    },
    'file02StringParam': 'Imported file 02',
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

IMPORTEDFILES02 = {
    'gPreprolIntParam': 1,
    'gPreproFloatParam': 1.332,
    'gPreproString': 'This is a string',
    'gPreproStructure': {
        'general': 'general'
    },
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01',
    'file02IntParam': 100,
    'file02FloatParam': 0.145,
    'file02StructureParam': {
        'iTestParam': 999,
        'general': {
            'general01': 'general01',
            'general02': 10
        }
    },
    'file02StringParam': 'Imported file 02'
}

IMPORTEDFILES03 = {
    'Project': 'JsonPreprocessor',
    'gPreprolIntParam': 1,
    'gPreproFloatParam': 1.332,
    'gPreproString': 'This is a string',
    'gPreproStructure': {
        'general': 'general'
    },
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'file02IntParam': 100,
        'file02FloatParam': 0.145,
        'file02StructureParam': {
            'iTestParam': 999,
            'general': {
                'general01': 'general01',
                'general02': 10
            }
        },
        'file02StringParam': 'Imported file 02',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

IMPORTEDFILES04 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'gPreprolIntParam': 1,
        'gPreproFloatParam': 1.332,
        'gPreproString': 'This is a string',
        'gPreproStructure': {
            'general': 'general'
        },
        'minorversion': '1',
        'patchversion': '1',
        'file02IntParam': 100,
        'file02FloatParam': 0.145,
        'file02StructureParam': {
            'iTestParam': 999,
            'general': {
                'general01': 'general01',
                'general02': 10
            }
        },
        'file02StringParam': 'Imported file 02'
    },
    'TargetName': 'Device@01'
}

NESTEDIMPORT01 = {
    'iNestedParam1': 11,
    'oNestedParam2': {
        'general': 'general'
    },
    'gPreprolIntParam': 11,
    'gPreproStructure': {
        'general': 'general'
    },
    'gPreproString': 'This is a string',
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

NESTEDIMPORT02 = {
    'Project': 'JsonPreprocessor',
    'iNestedParam1': 11,
    'oNestedParam2': {
        'general': 'general'
    },
    'gPreprolIntParam': 11,
    'gPreproStructure': {
        'general': 'general'
    },
    'gPreproString': 'This is a string',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

NESTEDIMPORT03 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'iNestedParam1': 11,
        'oNestedParam2': {
            'general': 'general'
        },
        'gPreprolIntParam': 11,
        'gPreproStructure': {
            'general': 'general'
        },
        'gPreproString': 'This is a string',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

NESTEDIMPORT04 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01',
    'iNestedParam1': 11,
    'oNestedParam2': {
        'general': 'general'
    },
    'gPreprolIntParam': 11,
    'gPreproStructure': {
        'general': 'general'
    },
    'gPreproString': 'This is a string',
}

NESTEDIMPORT05 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'gPreprolIntParam': 11,
        'gPreproStructure': {
            'iNestedParam1': 11,
            'oNestedParam2': {
                'general': 'general'
            },
            'general': 'general'
        },
        'gPreproString': 'This is a string',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

NESTEDIMPORT06 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01',
    'gPreprolIntParam': 11,
    'gPreproStructure': {
        'general': 'general'
    },
    'gPreproString': 'This is a string',
    'iNestedParam1': 11,
    'oNestedParam2': {
        'general': 'general'
    }
}

NESTEDIMPORT07 = {
    'Project': 'JsonPreprocessor',
    "iNestedParam1" : 11,
    "oNestedParam2": {
        "general": "general"
    },
    "iNestedTest1" : 9999,
    "oNestedTest2": {
        "testObject1": "testObject1",
        "testObject2": "testObject2"
    },
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01',
    'gPreprolIntParam': 11,
    'gPreproStructure': {
        'general': 'general'
    },
    'gPreproString': 'This is a string'
}

NESTEDIMPORT08 = {
    'Project': 'JsonPreprocessor',
    'WelcomeString': 'Hello... JsonPreprocessor selftest is running now!',
    'version': {
        'majorversion': '0',
        "gPreprolIntParam" : 11,
        "iNestedParam1" : 11,

        "oNestedParam2": {
            "general": "general"
        },
        "gPreproStructure": {
            "iNestedTest1" : 9999,
            "oNestedTest2": {
                "testObject1": "testObject1",
                "testObject2": "testObject2"
            },
            "general": "general"
        },
        "gPreproString"   : "This is a string",
        'minorversion': '1',
        'patchversion': '1'
    },
    'TargetName': 'Device@01'
}

NESTEDIMPORT09 = {
    "Project": "JsonPreprocessor",
    "WelcomeString": "Hello... JsonPreprocessor selftest is running now!",
    "version": {
        "majorversion": "0",
        "gPreprolIntParam" : 11,
        "iParam1" : 9999,

        "oParam2": {
            "iNestedParam1" : 11,

            "oNestedParam2": {
                "general": "general"
            },
            "paramObject2": "paramObject2"
        },
        "gPreproStructure": {
            "iNestedTest1" : 9999,

            "oNestedTest2": {
                "testObject1": "testObject1",
                "testObject2": "testObject2"
            },
            "general": "general"
        },

        "gPreproString"   : "This is a string",
        "minorversion": "1",
        "patchversion": "1"
    },
    "TargetName" : "Device@01"
}

SUBDATASTRUCTURE = {
    "testcase_01": 1999,
    "testcase_02a": "Welcome to Jsonpreprocessor Acceptance Test",
    "testcase_02b": 0.192,
    "testcase_02c": "Acceptance Testing",
    "testcase_03": 0.92,
    "testcase_04": "For testing purpose",
    "testcase_05": "This is a string",
    "testcase_06a": "JsonPreprocessor",
    "testcase_06b": {
      "globalFloatParam": 97,
      "gCheck01": 12,
      "globalIntParam": 69
    },
    "testcase_06c": 23,
    "testcase_06d": {
      "preproStructure": {
        "addNewPreParam": "Adds new param",
        "newStruct": {
          "check1": 1,
          "check2": 2
        },
        "variable_01": 1
      },
      "preproTest": {
        "param_01": "Updated new value"
      }
    },
    "testcase_07a": "test1",
    "testcase_07b": "check1"
}

PARAMOVERRIDE = {
    "testcase_01a": False,
    "testcase_01b": 1,
    "testcase_01c": "Params override testing",
    "testcase_02a": "Override string param in imported file.",
    "testcase_02b": 99,
    "testcase_02c": 9.876,
    "testcase_03a": False,
    "testcase_03b": {
            "bSupported": True,
            "struct": {
                    "test1": 1,
                    "test2": "https://www.abc.com"
                }
        },
    "testcase_03c": False,
    "testcase_03d": {
            "param01": 1,
            "param02": "param02"
        },
    "testcase_03e": "variant_0_RobotTestLog.log",
    "testcase_03f": {
            "sID": "Not defined yet",
            "sSample": "TBD"
        },
    "testcase_03g": {
            "TesttestParams1": "testParams1",
            "TesttestParams2": "testParams2"
        }
}

JSONFORMAT = {
  "Project": "https://www.robfwaio.com",
  "WelcomeString": "Hello... JsonPreprocessor selftest is running now!",
  "version//test": {
    "majorversion": "0",
    "minorversion": "1",
    "patchversion": "1"
  },
  "params": {
    "global": {
      "gGlobalIntParam" : 1,
      "gGlobalFloatParam" : 1.332,
      "gGlobal//String"   : "https://www.robfwaio.com",
      "gGlobalStructure": {
        "general": "general"
      }
    }
  },
  "preprocessor": {
    "definitions": {

      "gPreprolIntParam" : 1,

      "gPreproFloatParam" : 1.332,

      "gPrepro//String"   : "This is a string",

      "gPreproStructure": {
                             "general": "general",
                             "testing": 19,
                             "check//01": "check//Param"
                          }
    }
  },
  "abc" : "This is a multline string\nwith\nhttp://www.google.de\na link inside",
  "Target//Name" : "gen3flex//dlt"
}

JSONFORMAT_NONE_TRUE_FALSE = {
  "params": {
    "global": {
      "gGlobalIntParam" : 1,
      "gGlobalFloatParam" : 1.332,
      "Null_variable": None,
      "None_variable": None,
      "True_variable": True,
      "False_variable": False,
      "gGlobalString"   : "This is a string",
      "gGlobalStructure": {
        "general": "general"
      }
    }
  },
  "preprocessor": {
    "definitions": {
      "gPreprolIntParam" : 1,
      "gPreproFloatParam" : 1.332,
      "gPreproString"   : "This is a string",
      "gPreproStructure": {
                             "general": "general",
                             "testing": 19,
                             "check01": "checkParam"
                          }
    }
  }
}
