# **************************************************************************************************************
#
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
#
# **************************************************************************************************************
#
# TestConfig.py
#
# XC-CT/ECA3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
# 07.03.2024
#
# !!! Temporarily tests are deactivated by the following line commented out:
# # # listofdictUsecases.append(dictUsecase)
#
# They will be reactivated until fixes are available.
#
# --------------------------------------------------------------------------------------------------------------

listofdictUsecases = []

# the following keys are optional, all other keys are mandatory.
# dictUsecase['HINT']         = None
# dictUsecase['COMMENT']      = None
# dictUsecase['USERAWPATH']   = False # if True, 'JSONFILE' will not be normalized

# --------------------------------------------------------------------------------------------------------------

# If both 'EXPECTEDEXCEPTION' and 'EXPECTEDRETURN' are None, the check of values returned from JsonPreprocessor
# is skipped and the test case result is UNKNOWN.

# --------------------------------------------------------------------------------------------------------------
#TM***
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0001"
dictUsecase['DESCRIPTION']       = "JSON file with parameters of different data types (basic and composite)"
dictUsecase['EXPECTATION']       = "All values are returned untouched, with their correct data types"
dictUsecase['SECTION']           = "DATA_TYPES"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0001.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (15/1) > {param_01} [STR]  :  'string'
[DICT] (15/2) > {param_02} [INT]  :  123
[DICT] (15/3) > {param_03} [STR]  :  '123'
[DICT] (15/4) > {param_04} [FLOAT]  :  4.56
[DICT] (15/5) > {param_05} [STR]  :  '4.56'
[DICT] (15/6) > {param_06} [LIST] (3/1) > [STR]  :  'A'
[DICT] (15/6) > {param_06} [LIST] (3/2) > [STR]  :  'B'
[DICT] (15/6) > {param_06} [LIST] (3/3) > [STR]  :  'C'
[DICT] (15/7) > {param_07} [STR]  :  '['A', 'B', 'C']'
[DICT] (15/8) > {param_08} [DICT] (3/1) > {A} [INT]  :  1
[DICT] (15/8) > {param_08} [DICT] (3/2) > {B} [INT]  :  2
[DICT] (15/8) > {param_08} [DICT] (3/3) > {C} [INT]  :  3
[DICT] (15/9) > {param_09} [STR]  :  '{'A' : 1, 'B' : 2, 'C' : 3}'
[DICT] (15/10) > {param_10} [BOOL]  :  True
[DICT] (15/11) > {param_11} [STR]  :  'true'
[DICT] (15/12) > {param_12} [BOOL]  :  False
[DICT] (15/13) > {param_13} [STR]  :  'false'
[DICT] (15/14) > {param_14} [NONE]  :  None
[DICT] (15/15) > {param_15} [STR]  :  'null'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0002"
dictUsecase['DESCRIPTION']       = "JSON file containing parameters with dollar operator syntax at right hand side of colon, basic data types"
dictUsecase['EXPECTATION']       = "All parameters referenced by dollar operator are resolved correctly, with their correct data types"
dictUsecase['SECTION']           = "DATA_TYPES"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0002.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (51/1) > {param_01} [STR]  :  'string'
[DICT] (51/2) > {param_02} [INT]  :  123
[DICT] (51/3) > {param_03} [STR]  :  '123'
[DICT] (51/4) > {param_04} [FLOAT]  :  4.56
[DICT] (51/5) > {param_05} [STR]  :  '4.56'
[DICT] (51/6) > {param_06} [BOOL]  :  True
[DICT] (51/7) > {param_07} [STR]  :  'true'
[DICT] (51/8) > {param_08} [BOOL]  :  False
[DICT] (51/9) > {param_09} [STR]  :  'false'
[DICT] (51/10) > {param_10} [NONE]  :  None
[DICT] (51/11) > {param_11} [STR]  :  'null'
[DICT] (51/12) > {param_12} [BOOL]  :  True
[DICT] (51/13) > {param_13} [STR]  :  'True'
[DICT] (51/14) > {param_14} [BOOL]  :  False
[DICT] (51/15) > {param_15} [STR]  :  'False'
[DICT] (51/16) > {param_16} [NONE]  :  None
[DICT] (51/17) > {param_17} [STR]  :  'None'
[DICT] (51/18) > {param_18} [STR]  :  'string'
[DICT] (51/19) > {param_19} [STR]  :  'string'
[DICT] (51/20) > {param_20} [INT]  :  123
[DICT] (51/21) > {param_21} [STR]  :  '123'
[DICT] (51/22) > {param_22} [STR]  :  '123'
[DICT] (51/23) > {param_23} [STR]  :  '123'
[DICT] (51/24) > {param_24} [FLOAT]  :  4.56
[DICT] (51/25) > {param_25} [STR]  :  '4.56'
[DICT] (51/26) > {param_26} [STR]  :  '4.56'
[DICT] (51/27) > {param_27} [STR]  :  '4.56'
[DICT] (51/28) > {param_28} [BOOL]  :  True
[DICT] (51/29) > {param_29} [STR]  :  'True'
[DICT] (51/30) > {param_30} [STR]  :  'true'
[DICT] (51/31) > {param_31} [STR]  :  'true'
[DICT] (51/32) > {param_32} [BOOL]  :  False
[DICT] (51/33) > {param_33} [STR]  :  'False'
[DICT] (51/34) > {param_34} [STR]  :  'false'
[DICT] (51/35) > {param_35} [STR]  :  'false'
[DICT] (51/36) > {param_36} [NONE]  :  None
[DICT] (51/37) > {param_37} [STR]  :  'None'
[DICT] (51/38) > {param_38} [STR]  :  'null'
[DICT] (51/39) > {param_39} [STR]  :  'null'
[DICT] (51/40) > {param_40} [BOOL]  :  True
[DICT] (51/41) > {param_41} [STR]  :  'True'
[DICT] (51/42) > {param_42} [STR]  :  'True'
[DICT] (51/43) > {param_43} [STR]  :  'True'
[DICT] (51/44) > {param_44} [BOOL]  :  False
[DICT] (51/45) > {param_45} [STR]  :  'False'
[DICT] (51/46) > {param_46} [STR]  :  'False'
[DICT] (51/47) > {param_47} [STR]  :  'False'
[DICT] (51/48) > {param_48} [NONE]  :  None
[DICT] (51/49) > {param_49} [STR]  :  'None'
[DICT] (51/50) > {param_50} [STR]  :  'None'
[DICT] (51/51) > {param_51} [STR]  :  'None'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0003"
dictUsecase['DESCRIPTION']       = "JSON file containing parameters with dollar operator syntax at right hand side of colon, composite data type: list"
dictUsecase['EXPECTATION']       = "All parameters referenced by dollar operator are resolved correctly, with their correct data types"
dictUsecase['SECTION']           = "DATA_TYPES"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0003.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (53/1) > {param_01} [STR]  :  'string'
[DICT] (53/2) > {param_02} [INT]  :  123
[DICT] (53/3) > {param_03} [STR]  :  '123'
[DICT] (53/4) > {param_04} [FLOAT]  :  4.56
[DICT] (53/5) > {param_05} [STR]  :  '4.56'
[DICT] (53/6) > {param_06} [BOOL]  :  True
[DICT] (53/7) > {param_07} [STR]  :  'true'
[DICT] (53/8) > {param_08} [BOOL]  :  False
[DICT] (53/9) > {param_09} [STR]  :  'false'
[DICT] (53/10) > {param_10} [NONE]  :  None
[DICT] (53/11) > {param_11} [STR]  :  'null'
[DICT] (53/12) > {param_12} [BOOL]  :  True
[DICT] (53/13) > {param_13} [STR]  :  'True'
[DICT] (53/14) > {param_14} [BOOL]  :  False
[DICT] (53/15) > {param_15} [STR]  :  'False'
[DICT] (53/16) > {param_16} [NONE]  :  None
[DICT] (53/17) > {param_17} [STR]  :  'None'
[DICT] (53/18) > {param_18} [STR]  :  'string'
[DICT] (53/19) > {param_19} [STR]  :  'string'
[DICT] (53/20) > {param_20} [INT]  :  123
[DICT] (53/21) > {param_21} [STR]  :  '123'
[DICT] (53/22) > {param_22} [STR]  :  '123'
[DICT] (53/23) > {param_23} [STR]  :  '123'
[DICT] (53/24) > {param_24} [FLOAT]  :  4.56
[DICT] (53/25) > {param_25} [STR]  :  '4.56'
[DICT] (53/26) > {param_26} [STR]  :  '4.56'
[DICT] (53/27) > {param_27} [STR]  :  '4.56'
[DICT] (53/28) > {param_28} [BOOL]  :  True
[DICT] (53/29) > {param_29} [STR]  :  'True'
[DICT] (53/30) > {param_30} [STR]  :  'true'
[DICT] (53/31) > {param_31} [STR]  :  'true'
[DICT] (53/32) > {param_32} [BOOL]  :  False
[DICT] (53/33) > {param_33} [STR]  :  'False'
[DICT] (53/34) > {param_34} [STR]  :  'false'
[DICT] (53/35) > {param_35} [STR]  :  'false'
[DICT] (53/36) > {param_36} [NONE]  :  None
[DICT] (53/37) > {param_37} [STR]  :  'None'
[DICT] (53/38) > {param_38} [STR]  :  'null'
[DICT] (53/39) > {param_39} [STR]  :  'null'
[DICT] (53/40) > {param_40} [BOOL]  :  True
[DICT] (53/41) > {param_41} [STR]  :  'True'
[DICT] (53/42) > {param_42} [STR]  :  'True'
[DICT] (53/43) > {param_43} [STR]  :  'True'
[DICT] (53/44) > {param_44} [BOOL]  :  False
[DICT] (53/45) > {param_45} [STR]  :  'False'
[DICT] (53/46) > {param_46} [STR]  :  'False'
[DICT] (53/47) > {param_47} [STR]  :  'False'
[DICT] (53/48) > {param_48} [NONE]  :  None
[DICT] (53/49) > {param_49} [STR]  :  'None'
[DICT] (53/50) > {param_50} [STR]  :  'None'
[DICT] (53/51) > {param_51} [STR]  :  'None'
[DICT] (53/52) > {param_100} [LIST] (51/1) > [STR]  :  'string'
[DICT] (53/52) > {param_100} [LIST] (51/2) > [INT]  :  123
[DICT] (53/52) > {param_100} [LIST] (51/3) > [STR]  :  '123'
[DICT] (53/52) > {param_100} [LIST] (51/4) > [FLOAT]  :  4.56
[DICT] (53/52) > {param_100} [LIST] (51/5) > [STR]  :  '4.56'
[DICT] (53/52) > {param_100} [LIST] (51/6) > [BOOL]  :  True
[DICT] (53/52) > {param_100} [LIST] (51/7) > [STR]  :  'true'
[DICT] (53/52) > {param_100} [LIST] (51/8) > [BOOL]  :  False
[DICT] (53/52) > {param_100} [LIST] (51/9) > [STR]  :  'false'
[DICT] (53/52) > {param_100} [LIST] (51/10) > [NONE]  :  None
[DICT] (53/52) > {param_100} [LIST] (51/11) > [STR]  :  'null'
[DICT] (53/52) > {param_100} [LIST] (51/12) > [BOOL]  :  True
[DICT] (53/52) > {param_100} [LIST] (51/13) > [STR]  :  'True'
[DICT] (53/52) > {param_100} [LIST] (51/14) > [BOOL]  :  False
[DICT] (53/52) > {param_100} [LIST] (51/15) > [STR]  :  'False'
[DICT] (53/52) > {param_100} [LIST] (51/16) > [NONE]  :  None
[DICT] (53/52) > {param_100} [LIST] (51/17) > [STR]  :  'None'
[DICT] (53/52) > {param_100} [LIST] (51/18) > [STR]  :  'string'
[DICT] (53/52) > {param_100} [LIST] (51/19) > [STR]  :  'string'
[DICT] (53/52) > {param_100} [LIST] (51/20) > [INT]  :  123
[DICT] (53/52) > {param_100} [LIST] (51/21) > [STR]  :  '123'
[DICT] (53/52) > {param_100} [LIST] (51/22) > [STR]  :  '123'
[DICT] (53/52) > {param_100} [LIST] (51/23) > [STR]  :  '123'
[DICT] (53/52) > {param_100} [LIST] (51/24) > [FLOAT]  :  4.56
[DICT] (53/52) > {param_100} [LIST] (51/25) > [STR]  :  '4.56'
[DICT] (53/52) > {param_100} [LIST] (51/26) > [STR]  :  '4.56'
[DICT] (53/52) > {param_100} [LIST] (51/27) > [STR]  :  '4.56'
[DICT] (53/52) > {param_100} [LIST] (51/28) > [BOOL]  :  True
[DICT] (53/52) > {param_100} [LIST] (51/29) > [STR]  :  'True'
[DICT] (53/52) > {param_100} [LIST] (51/30) > [STR]  :  'true'
[DICT] (53/52) > {param_100} [LIST] (51/31) > [STR]  :  'true'
[DICT] (53/52) > {param_100} [LIST] (51/32) > [BOOL]  :  False
[DICT] (53/52) > {param_100} [LIST] (51/33) > [STR]  :  'False'
[DICT] (53/52) > {param_100} [LIST] (51/34) > [STR]  :  'false'
[DICT] (53/52) > {param_100} [LIST] (51/35) > [STR]  :  'false'
[DICT] (53/52) > {param_100} [LIST] (51/36) > [NONE]  :  None
[DICT] (53/52) > {param_100} [LIST] (51/37) > [STR]  :  'None'
[DICT] (53/52) > {param_100} [LIST] (51/38) > [STR]  :  'null'
[DICT] (53/52) > {param_100} [LIST] (51/39) > [STR]  :  'null'
[DICT] (53/52) > {param_100} [LIST] (51/40) > [BOOL]  :  True
[DICT] (53/52) > {param_100} [LIST] (51/41) > [STR]  :  'True'
[DICT] (53/52) > {param_100} [LIST] (51/42) > [STR]  :  'True'
[DICT] (53/52) > {param_100} [LIST] (51/43) > [STR]  :  'True'
[DICT] (53/52) > {param_100} [LIST] (51/44) > [BOOL]  :  False
[DICT] (53/52) > {param_100} [LIST] (51/45) > [STR]  :  'False'
[DICT] (53/52) > {param_100} [LIST] (51/46) > [STR]  :  'False'
[DICT] (53/52) > {param_100} [LIST] (51/47) > [STR]  :  'False'
[DICT] (53/52) > {param_100} [LIST] (51/48) > [NONE]  :  None
[DICT] (53/52) > {param_100} [LIST] (51/49) > [STR]  :  'None'
[DICT] (53/52) > {param_100} [LIST] (51/50) > [STR]  :  'None'
[DICT] (53/52) > {param_100} [LIST] (51/51) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/1) > [STR]  :  'string'
[DICT] (53/53) > {param_101} [LIST] (51/2) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/3) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/4) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/5) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/6) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/7) > [STR]  :  'true'
[DICT] (53/53) > {param_101} [LIST] (51/8) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/9) > [STR]  :  'false'
[DICT] (53/53) > {param_101} [LIST] (51/10) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/11) > [STR]  :  'null'
[DICT] (53/53) > {param_101} [LIST] (51/12) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/13) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/14) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/15) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/16) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/17) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/18) > [STR]  :  'string'
[DICT] (53/53) > {param_101} [LIST] (51/19) > [STR]  :  'string'
[DICT] (53/53) > {param_101} [LIST] (51/20) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/21) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/22) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/23) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/24) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/25) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/26) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/27) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/28) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/29) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/30) > [STR]  :  'true'
[DICT] (53/53) > {param_101} [LIST] (51/31) > [STR]  :  'true'
[DICT] (53/53) > {param_101} [LIST] (51/32) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/33) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/34) > [STR]  :  'false'
[DICT] (53/53) > {param_101} [LIST] (51/35) > [STR]  :  'false'
[DICT] (53/53) > {param_101} [LIST] (51/36) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/37) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/38) > [STR]  :  'null'
[DICT] (53/53) > {param_101} [LIST] (51/39) > [STR]  :  'null'
[DICT] (53/53) > {param_101} [LIST] (51/40) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/41) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/42) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/43) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/44) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/45) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/46) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/47) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/48) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/49) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/50) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/51) > [STR]  :  'None'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0004"
dictUsecase['DESCRIPTION']       = "JSON file containing parameters with dollar operator syntax at right hand side of colon, composite data type: dict"
dictUsecase['EXPECTATION']       = "All parameters referenced by dollar operator are resolved correctly, with their correct data types"
dictUsecase['SECTION']           = "DATA_TYPES"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0004.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (53/1) > {param_01} [STR]  :  'string'
[DICT] (53/2) > {param_02} [INT]  :  123
[DICT] (53/3) > {param_03} [STR]  :  '123'
[DICT] (53/4) > {param_04} [FLOAT]  :  4.56
[DICT] (53/5) > {param_05} [STR]  :  '4.56'
[DICT] (53/6) > {param_06} [BOOL]  :  True
[DICT] (53/7) > {param_07} [STR]  :  'true'
[DICT] (53/8) > {param_08} [BOOL]  :  False
[DICT] (53/9) > {param_09} [STR]  :  'false'
[DICT] (53/10) > {param_10} [NONE]  :  None
[DICT] (53/11) > {param_11} [STR]  :  'null'
[DICT] (53/12) > {param_12} [BOOL]  :  True
[DICT] (53/13) > {param_13} [STR]  :  'True'
[DICT] (53/14) > {param_14} [BOOL]  :  False
[DICT] (53/15) > {param_15} [STR]  :  'False'
[DICT] (53/16) > {param_16} [NONE]  :  None
[DICT] (53/17) > {param_17} [STR]  :  'None'
[DICT] (53/18) > {param_18} [STR]  :  'string'
[DICT] (53/19) > {param_19} [STR]  :  'string'
[DICT] (53/20) > {param_20} [INT]  :  123
[DICT] (53/21) > {param_21} [STR]  :  '123'
[DICT] (53/22) > {param_22} [STR]  :  '123'
[DICT] (53/23) > {param_23} [STR]  :  '123'
[DICT] (53/24) > {param_24} [FLOAT]  :  4.56
[DICT] (53/25) > {param_25} [STR]  :  '4.56'
[DICT] (53/26) > {param_26} [STR]  :  '4.56'
[DICT] (53/27) > {param_27} [STR]  :  '4.56'
[DICT] (53/28) > {param_28} [BOOL]  :  True
[DICT] (53/29) > {param_29} [STR]  :  'True'
[DICT] (53/30) > {param_30} [STR]  :  'true'
[DICT] (53/31) > {param_31} [STR]  :  'true'
[DICT] (53/32) > {param_32} [BOOL]  :  False
[DICT] (53/33) > {param_33} [STR]  :  'False'
[DICT] (53/34) > {param_34} [STR]  :  'false'
[DICT] (53/35) > {param_35} [STR]  :  'false'
[DICT] (53/36) > {param_36} [NONE]  :  None
[DICT] (53/37) > {param_37} [STR]  :  'None'
[DICT] (53/38) > {param_38} [STR]  :  'null'
[DICT] (53/39) > {param_39} [STR]  :  'null'
[DICT] (53/40) > {param_40} [BOOL]  :  True
[DICT] (53/41) > {param_41} [STR]  :  'True'
[DICT] (53/42) > {param_42} [STR]  :  'True'
[DICT] (53/43) > {param_43} [STR]  :  'True'
[DICT] (53/44) > {param_44} [BOOL]  :  False
[DICT] (53/45) > {param_45} [STR]  :  'False'
[DICT] (53/46) > {param_46} [STR]  :  'False'
[DICT] (53/47) > {param_47} [STR]  :  'False'
[DICT] (53/48) > {param_48} [NONE]  :  None
[DICT] (53/49) > {param_49} [STR]  :  'None'
[DICT] (53/50) > {param_50} [STR]  :  'None'
[DICT] (53/51) > {param_51} [STR]  :  'None'
[DICT] (53/52) > {param_102} [DICT] (51/1) > {key_01} [STR]  :  'string'
[DICT] (53/52) > {param_102} [DICT] (51/2) > {key_02} [INT]  :  123
[DICT] (53/52) > {param_102} [DICT] (51/3) > {key_03} [STR]  :  '123'
[DICT] (53/52) > {param_102} [DICT] (51/4) > {key_04} [FLOAT]  :  4.56
[DICT] (53/52) > {param_102} [DICT] (51/5) > {key_05} [STR]  :  '4.56'
[DICT] (53/52) > {param_102} [DICT] (51/6) > {key_06} [BOOL]  :  True
[DICT] (53/52) > {param_102} [DICT] (51/7) > {key_07} [STR]  :  'true'
[DICT] (53/52) > {param_102} [DICT] (51/8) > {key_08} [BOOL]  :  False
[DICT] (53/52) > {param_102} [DICT] (51/9) > {key_09} [STR]  :  'false'
[DICT] (53/52) > {param_102} [DICT] (51/10) > {key_10} [NONE]  :  None
[DICT] (53/52) > {param_102} [DICT] (51/11) > {key_11} [STR]  :  'null'
[DICT] (53/52) > {param_102} [DICT] (51/12) > {key_12} [BOOL]  :  True
[DICT] (53/52) > {param_102} [DICT] (51/13) > {key_13} [STR]  :  'True'
[DICT] (53/52) > {param_102} [DICT] (51/14) > {key_14} [BOOL]  :  False
[DICT] (53/52) > {param_102} [DICT] (51/15) > {key_15} [STR]  :  'False'
[DICT] (53/52) > {param_102} [DICT] (51/16) > {key_16} [NONE]  :  None
[DICT] (53/52) > {param_102} [DICT] (51/17) > {key_17} [STR]  :  'None'
[DICT] (53/52) > {param_102} [DICT] (51/18) > {key_18} [STR]  :  'string'
[DICT] (53/52) > {param_102} [DICT] (51/19) > {key_19} [STR]  :  'string'
[DICT] (53/52) > {param_102} [DICT] (51/20) > {key_20} [INT]  :  123
[DICT] (53/52) > {param_102} [DICT] (51/21) > {key_21} [STR]  :  '123'
[DICT] (53/52) > {param_102} [DICT] (51/22) > {key_22} [STR]  :  '123'
[DICT] (53/52) > {param_102} [DICT] (51/23) > {key_23} [STR]  :  '123'
[DICT] (53/52) > {param_102} [DICT] (51/24) > {key_24} [FLOAT]  :  4.56
[DICT] (53/52) > {param_102} [DICT] (51/25) > {key_25} [STR]  :  '4.56'
[DICT] (53/52) > {param_102} [DICT] (51/26) > {key_26} [STR]  :  '4.56'
[DICT] (53/52) > {param_102} [DICT] (51/27) > {key_27} [STR]  :  '4.56'
[DICT] (53/52) > {param_102} [DICT] (51/28) > {key_28} [BOOL]  :  True
[DICT] (53/52) > {param_102} [DICT] (51/29) > {key_29} [STR]  :  'True'
[DICT] (53/52) > {param_102} [DICT] (51/30) > {key_30} [STR]  :  'true'
[DICT] (53/52) > {param_102} [DICT] (51/31) > {key_31} [STR]  :  'true'
[DICT] (53/52) > {param_102} [DICT] (51/32) > {key_32} [BOOL]  :  False
[DICT] (53/52) > {param_102} [DICT] (51/33) > {key_33} [STR]  :  'False'
[DICT] (53/52) > {param_102} [DICT] (51/34) > {key_34} [STR]  :  'false'
[DICT] (53/52) > {param_102} [DICT] (51/35) > {key_35} [STR]  :  'false'
[DICT] (53/52) > {param_102} [DICT] (51/36) > {key_36} [NONE]  :  None
[DICT] (53/52) > {param_102} [DICT] (51/37) > {key_37} [STR]  :  'None'
[DICT] (53/52) > {param_102} [DICT] (51/38) > {key_38} [STR]  :  'null'
[DICT] (53/52) > {param_102} [DICT] (51/39) > {key_39} [STR]  :  'null'
[DICT] (53/52) > {param_102} [DICT] (51/40) > {key_40} [BOOL]  :  True
[DICT] (53/52) > {param_102} [DICT] (51/41) > {key_41} [STR]  :  'True'
[DICT] (53/52) > {param_102} [DICT] (51/42) > {key_42} [STR]  :  'True'
[DICT] (53/52) > {param_102} [DICT] (51/43) > {key_43} [STR]  :  'True'
[DICT] (53/52) > {param_102} [DICT] (51/44) > {key_44} [BOOL]  :  False
[DICT] (53/52) > {param_102} [DICT] (51/45) > {key_45} [STR]  :  'False'
[DICT] (53/52) > {param_102} [DICT] (51/46) > {key_46} [STR]  :  'False'
[DICT] (53/52) > {param_102} [DICT] (51/47) > {key_47} [STR]  :  'False'
[DICT] (53/52) > {param_102} [DICT] (51/48) > {key_48} [NONE]  :  None
[DICT] (53/52) > {param_102} [DICT] (51/49) > {key_49} [STR]  :  'None'
[DICT] (53/52) > {param_102} [DICT] (51/50) > {key_50} [STR]  :  'None'
[DICT] (53/52) > {param_102} [DICT] (51/51) > {key_51} [STR]  :  'None'
[DICT] (53/53) > {param_103} [DICT] (51/1) > {key_01} [STR]  :  'string'
[DICT] (53/53) > {param_103} [DICT] (51/2) > {key_02} [STR]  :  '123'
[DICT] (53/53) > {param_103} [DICT] (51/3) > {key_03} [STR]  :  '123'
[DICT] (53/53) > {param_103} [DICT] (51/4) > {key_04} [STR]  :  '4.56'
[DICT] (53/53) > {param_103} [DICT] (51/5) > {key_05} [STR]  :  '4.56'
[DICT] (53/53) > {param_103} [DICT] (51/6) > {key_06} [STR]  :  'True'
[DICT] (53/53) > {param_103} [DICT] (51/7) > {key_07} [STR]  :  'true'
[DICT] (53/53) > {param_103} [DICT] (51/8) > {key_08} [STR]  :  'False'
[DICT] (53/53) > {param_103} [DICT] (51/9) > {key_09} [STR]  :  'false'
[DICT] (53/53) > {param_103} [DICT] (51/10) > {key_10} [STR]  :  'None'
[DICT] (53/53) > {param_103} [DICT] (51/11) > {key_11} [STR]  :  'null'
[DICT] (53/53) > {param_103} [DICT] (51/12) > {key_12} [STR]  :  'True'
[DICT] (53/53) > {param_103} [DICT] (51/13) > {key_13} [STR]  :  'True'
[DICT] (53/53) > {param_103} [DICT] (51/14) > {key_14} [STR]  :  'False'
[DICT] (53/53) > {param_103} [DICT] (51/15) > {key_15} [STR]  :  'False'
[DICT] (53/53) > {param_103} [DICT] (51/16) > {key_16} [STR]  :  'None'
[DICT] (53/53) > {param_103} [DICT] (51/17) > {key_17} [STR]  :  'None'
[DICT] (53/53) > {param_103} [DICT] (51/18) > {key_18} [STR]  :  'string'
[DICT] (53/53) > {param_103} [DICT] (51/19) > {key_19} [STR]  :  'string'
[DICT] (53/53) > {param_103} [DICT] (51/20) > {key_20} [INT]  :  123
[DICT] (53/53) > {param_103} [DICT] (51/21) > {key_21} [STR]  :  '123'
[DICT] (53/53) > {param_103} [DICT] (51/22) > {key_22} [STR]  :  '123'
[DICT] (53/53) > {param_103} [DICT] (51/23) > {key_23} [STR]  :  '123'
[DICT] (53/53) > {param_103} [DICT] (51/24) > {key_24} [FLOAT]  :  4.56
[DICT] (53/53) > {param_103} [DICT] (51/25) > {key_25} [STR]  :  '4.56'
[DICT] (53/53) > {param_103} [DICT] (51/26) > {key_26} [STR]  :  '4.56'
[DICT] (53/53) > {param_103} [DICT] (51/27) > {key_27} [STR]  :  '4.56'
[DICT] (53/53) > {param_103} [DICT] (51/28) > {key_28} [BOOL]  :  True
[DICT] (53/53) > {param_103} [DICT] (51/29) > {key_29} [STR]  :  'true'
[DICT] (53/53) > {param_103} [DICT] (51/30) > {key_30} [STR]  :  'true'
[DICT] (53/53) > {param_103} [DICT] (51/31) > {key_31} [STR]  :  'true'
[DICT] (53/53) > {param_103} [DICT] (51/32) > {key_32} [BOOL]  :  False
[DICT] (53/53) > {param_103} [DICT] (51/33) > {key_33} [STR]  :  'false'
[DICT] (53/53) > {param_103} [DICT] (51/34) > {key_34} [STR]  :  'false'
[DICT] (53/53) > {param_103} [DICT] (51/35) > {key_35} [STR]  :  'false'
[DICT] (53/53) > {param_103} [DICT] (51/36) > {key_36} [BOOL]  :  None
[DICT] (53/53) > {param_103} [DICT] (51/37) > {key_37} [STR]  :  'null'
[DICT] (53/53) > {param_103} [DICT] (51/38) > {key_38} [STR]  :  'null'
[DICT] (53/53) > {param_103} [DICT] (51/39) > {key_39} [STR]  :  'null'
[DICT] (53/53) > {param_103} [DICT] (51/40) > {key_40} [BOOL]  :  True
[DICT] (53/53) > {param_103} [DICT] (51/41) > {key_41} [STR]  :  'True'
[DICT] (53/53) > {param_103} [DICT] (51/42) > {key_42} [STR]  :  'True'
[DICT] (53/53) > {param_103} [DICT] (51/43) > {key_43} [STR]  :  'True'
[DICT] (53/53) > {param_103} [DICT] (51/44) > {key_44} [BOOL]  :  False
[DICT] (53/53) > {param_103} [DICT] (51/45) > {key_45} [STR]  :  'False'
[DICT] (53/53) > {param_103} [DICT] (51/46) > {key_46} [STR]  :  'False'
[DICT] (53/53) > {param_103} [DICT] (51/47) > {key_47} [STR]  :  'False'
[DICT] (53/53) > {param_103} [DICT] (51/48) > {key_48} [BOOL]  :  None
[DICT] (53/53) > {param_103} [DICT] (51/49) > {key_49} [STR]  :  'None'
[DICT] (53/53) > {param_103} [DICT] (51/50) > {key_50} [STR]  :  'None'
[DICT] (53/53) > {param_103} [DICT] (51/51) > {key_51} [STR]  :  'None'
"""
# # # listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0005"
dictUsecase['DESCRIPTION']       = "JSON file with string values containing dollar operators"
dictUsecase['EXPECTATION']       = "All parameters referenced by dollar operator are resolved correctly, outcome is a string containing the values of all referenced parameters"
dictUsecase['SECTION']           = "DATA_TYPES"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0005.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (59/1) > {param_01} [STR]  :  'string'
[DICT] (59/2) > {param_02} [INT]  :  123
[DICT] (59/3) > {param_03} [STR]  :  '123'
[DICT] (59/4) > {param_04} [FLOAT]  :  4.56
[DICT] (59/5) > {param_05} [STR]  :  '4.56'
[DICT] (59/6) > {param_06} [BOOL]  :  True
[DICT] (59/7) > {param_07} [STR]  :  'true'
[DICT] (59/8) > {param_08} [BOOL]  :  False
[DICT] (59/9) > {param_09} [STR]  :  'false'
[DICT] (59/10) > {param_10} [NONE]  :  None
[DICT] (59/11) > {param_11} [STR]  :  'null'
[DICT] (59/12) > {param_12} [BOOL]  :  True
[DICT] (59/13) > {param_13} [STR]  :  'True'
[DICT] (59/14) > {param_14} [BOOL]  :  False
[DICT] (59/15) > {param_15} [STR]  :  'False'
[DICT] (59/16) > {param_16} [NONE]  :  None
[DICT] (59/17) > {param_17} [STR]  :  'None'
[DICT] (59/18) > {param_18} [STR]  :  'string'
[DICT] (59/19) > {param_19} [STR]  :  'string'
[DICT] (59/20) > {param_20} [INT]  :  123
[DICT] (59/21) > {param_21} [STR]  :  '123'
[DICT] (59/22) > {param_22} [STR]  :  '123'
[DICT] (59/23) > {param_23} [STR]  :  '123'
[DICT] (59/24) > {param_24} [FLOAT]  :  4.56
[DICT] (59/25) > {param_25} [STR]  :  '4.56'
[DICT] (59/26) > {param_26} [STR]  :  '4.56'
[DICT] (59/27) > {param_27} [STR]  :  '4.56'
[DICT] (59/28) > {param_28} [BOOL]  :  True
[DICT] (59/29) > {param_29} [STR]  :  'True'
[DICT] (59/30) > {param_30} [STR]  :  'true'
[DICT] (59/31) > {param_31} [STR]  :  'true'
[DICT] (59/32) > {param_32} [BOOL]  :  False
[DICT] (59/33) > {param_33} [STR]  :  'False'
[DICT] (59/34) > {param_34} [STR]  :  'false'
[DICT] (59/35) > {param_35} [STR]  :  'false'
[DICT] (59/36) > {param_36} [NONE]  :  None
[DICT] (59/37) > {param_37} [STR]  :  'None'
[DICT] (59/38) > {param_38} [STR]  :  'null'
[DICT] (59/39) > {param_39} [STR]  :  'null'
[DICT] (59/40) > {param_40} [BOOL]  :  True
[DICT] (59/41) > {param_41} [STR]  :  'True'
[DICT] (59/42) > {param_42} [STR]  :  'True'
[DICT] (59/43) > {param_43} [STR]  :  'True'
[DICT] (59/44) > {param_44} [BOOL]  :  False
[DICT] (59/45) > {param_45} [STR]  :  'False'
[DICT] (59/46) > {param_46} [STR]  :  'False'
[DICT] (59/47) > {param_47} [STR]  :  'False'
[DICT] (59/48) > {param_48} [NONE]  :  None
[DICT] (59/49) > {param_49} [STR]  :  'None'
[DICT] (59/50) > {param_50} [STR]  :  'None'
[DICT] (59/51) > {param_51} [STR]  :  'None'
[DICT] (59/52) > {param_201} [STR]  :  '01: string / 02: 123 / 03: 123 / 04: 4.56 / 05: 4.56 / 06: True / 07: true'
[DICT] (59/53) > {param_202} [STR]  :  '08: False / 09: false / 10: None / 11: null / 12: True / 13: True / 14: False'
[DICT] (59/54) > {param_203} [STR]  :  '15: False / 16: None / 17: None / 18: string / 19: string / 20: 123 / 21: 123'
[DICT] (59/55) > {param_204} [STR]  :  '22: 123 / 23: 123 / 24: 4.56 / 25: 4.56 / 26: 4.56 / 27: 4.56 / 28: True'
[DICT] (59/56) > {param_205} [STR]  :  '29: True / 30: true / 31: true / 32: False / 33: False / 34: false / 35: false'
[DICT] (59/57) > {param_206} [STR]  :  '36: None / 37: None / 38: null / 39: null / 40: True / 41: True / 42: True'
[DICT] (59/58) > {param_207} [STR]  :  '43: True / 44: False / 45: False / 46: False / 47: False / 48: None / 49: None'
[DICT] (59/59) > {param_208} [STR]  :  '50: None / 51: None'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0100"
dictUsecase['DESCRIPTION']       = "JSON file is empty (single pair of brackets only)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns empty dictionary"
dictUsecase['SECTION']           = "DATA_INTEGRITY"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0100.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = "[DICT]  :  {}"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0101"
dictUsecase['DESCRIPTION']       = "JSON file with string containing several separator characters and blanks; no parameters"
dictUsecase['EXPECTATION']       = "String is returned unchanged"
dictUsecase['SECTION']           = "DATA_INTEGRITY"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0101.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = "[DICT] (1/1) > {teststring_data_integrity} [STR]  :  'a.1,b.2;c.3,d.4  ;  e.5  ,  f.6'"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0102"
dictUsecase['DESCRIPTION']       = "JSON file with string containing more special characters, masked special characters and escape sequences"
dictUsecase['EXPECTATION']       = "String is returned unchanged (but with masked special characters and escape sequences resolved)"
dictUsecase['SECTION']           = "DATA_INTEGRITY"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0102.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = r"[DICT] (1/1) > {teststring_data_integrity} [STR]  :  'Ä.1/B.2\C.3$D.4&E.5?F.6=G.7#H.8~I.9§J.10,{K.11};L.12@M.12" + "\"N.13/Ö.14%1P.15;(Q.16),[R.17]'"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0200"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / string parameter substitution in parameter value"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0200.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (21/1) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (21/2) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (21/2) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (21/3) > {list_variant_index} [INT]  :  0
[DICT] (21/4) > {variant_number} [STR]  :  '1'
[DICT] (21/5) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (21/5) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (21/6) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (21/7) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (21/8) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (21/9) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (21/10) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (21/11) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (21/12) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (21/13) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (21/13) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (21/13) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (21/14) > {list_milestone_index} [INT]  :  1
[DICT] (21/15) > {milestone_number} [STR]  :  '2'
[DICT] (21/16) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (21/16) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (21/16) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (21/17) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (21/18) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (21/19) > {ilesto} [STR]  :  'ilesto'
[DICT] (21/20) > {milestone} [STR]  :  'milestone'
[DICT] (21/21) > {variant_1} [STR]  :  'VARIANT_1 (new value)'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0201"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / string parameter substitution in parameter name"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0201.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (21/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (21/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (21/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (21/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (21/4) > {list_variant_index} [INT]  :  0
[DICT] (21/5) > {variant_number} [STR]  :  '1'
[DICT] (21/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (21/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (21/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (21/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (21/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (21/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (21/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (21/12) > {milestone_2} [STR]  :  'MILESTONE_2 (new value)'
[DICT] (21/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (21/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (21/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (21/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (21/15) > {list_milestone_index} [INT]  :  1
[DICT] (21/16) > {milestone_number} [STR]  :  '2'
[DICT] (21/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (21/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (21/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (21/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (21/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (21/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (21/21) > {milestone} [STR]  :  'milestone'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0202"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter name / standard notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0202.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR_VARIANT_1_MS_MILESTONE_2_param} [STR]  :  'value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0203"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter name / dotdict notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0203.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR_VARIANT_1_MS_MILESTONE_2_param} [STR]  :  'value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0204"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter value / standard notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0204.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR_VARIANT_1_MS_MILESTONE_2 value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0205"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter value / dotdict notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0205.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR_VARIANT_1_MS_MILESTONE_2 value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0206"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter name / standard notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0206.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR_VARIANT_1_MS_MILESTONE_2_param} [STR]  :  'value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0207"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter name / dotdict notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0207.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR_VARIANT_1_MS_MILESTONE_2_param} [STR]  :  'value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0208"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter value / standard notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0208.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR_VARIANT_1_MS_MILESTONE_2 value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0209"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter value / dotdict notation"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0209.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT_1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT_2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE_1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE_2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE_3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR_VARIANT_1_MS_MILESTONE_2 value'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0250"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / string parameter substitution in parameter value / innermost parameter not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0250.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0251"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / string parameter substitution in parameter name / in between parameter not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0251.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0252"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter name / standard notation / index parameter not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0252.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0253"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter name / dotdict notation / index parameter not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0253.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0254"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter value / standard notation / index parameter not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0254.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0255"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / index parameter substitution in parameter value / dotdict notation / index parameter not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0255.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0256"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter name / standard notation / variant number not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0256.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0257"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter name / dotdict notation / milestone number not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0257.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0258"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter value / standard notation / variant number not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0258.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0259"
dictUsecase['DESCRIPTION']       = "JSON file with nested parameter / key parameter substitution in parameter value / dotdict notation / milestone number not existing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0259.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The variable '${IAMNOTEXISTING}' is not available!"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0260"
dictUsecase['DESCRIPTION']       = "JSON file with list parameter substitution in parameter name (composite data types not allowed in names) / (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0260.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Found expression '${param}' with at least one parameter of composite data type ('${param}' is of type <class 'list'>). Because of this expression is the name of a parameter, only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0261"
dictUsecase['DESCRIPTION']       = "JSON file with list parameter substitution in parameter name (composite data types not allowed in names) / (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0261.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0262"
dictUsecase['DESCRIPTION']       = "JSON file with dictionary parameter substitution in parameter name (composite data types not allowed in names) / (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0262.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Found expression '${param}' with at least one parameter of composite data type ('${param}' is of type <class 'dict'>). Because of this expression is the name of a parameter, only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0263"
dictUsecase['DESCRIPTION']       = "JSON file with dictionary parameter substitution in parameter name (composite data types not allowed in names) / (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0263.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0264"
dictUsecase['DESCRIPTION']       = "JSON file with list parameter substitution in key name (composite data types not allowed in names) / (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0264.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0265"
dictUsecase['DESCRIPTION']       = "JSON file with list parameter substitution in key name (composite data types not allowed in names) / (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0265.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0266"
dictUsecase['DESCRIPTION']       = "JSON file with dictionary parameter substitution in key name (composite data types not allowed in names) / (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0266.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0267"
dictUsecase['DESCRIPTION']       = "JSON file with dictionary parameter substitution in key name (composite data types not allowed in names) / (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0267.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside."
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0268"
dictUsecase['DESCRIPTION']       = "JSON file containing a list; list index is defined by a parameter and wrapped in single quotes"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "List indices must be of type 'int'"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0268.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "List indices must be of type 'int' (error message placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0300"
dictUsecase['DESCRIPTION']       = "JSON file with parameter of type 'list' / index (in square brackets) defined outside the curly brackets (valid syntax)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Checklist rule 1"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0300.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (4/1) > {list_param} [LIST] (3/1) > [INT]  :  12
[DICT] (4/1) > {list_param} [LIST] (3/2) > [FLOAT]  :  3.4
[DICT] (4/1) > {list_param} [LIST] (3/3) > [INT]  :  56
[DICT] (4/2) > {val1} [INT]  :  12
[DICT] (4/3) > {val2} [STR]  :  '3.4'
[DICT] (4/4) > {val3} [STR]  :  'value_56'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0301"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (valid syntax)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Checklist rule 3"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0301.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (12/1) > {par1} [FLOAT]  :  1.23
[DICT] (12/2) > {par2} [LIST] (2/1) > [STR]  :  'A'
[DICT] (12/2) > {par2} [LIST] (2/2) > [STR]  :  'B'
[DICT] (12/3) > {par3} [LIST] (1/1) > [STR]  :  'par'
[DICT] (12/4) > {ara} [STR]  :  'ara'
[DICT] (12/5) > {param} [STR]  :  'param'
[DICT] (12/6) > {param2} [LIST] (1/1) > [STR]  :  'par'
[DICT] (12/7) > {val1} [STR]  :  '{par1}am}'
[DICT] (12/8) > {val2} [STR]  :  '1.23am}'
[DICT] (12/9) > {val3} [STR]  :  'param}'
[DICT] (12/10) > {val4} [STR]  :  'param}'
[DICT] (12/11) > {val5} [STR]  :  'param2}[0]'
[DICT] (12/12) > {val6} [STR]  :  'param2.0}'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0302"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}' / no further matching '${' and '}' in between (valid syntax)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Checklist rule 4"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0302.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (8/1) > {param1} [INT]  :  123
[DICT] (8/2) > {param2} [LIST] (1/1) > [INT]  :  123
[DICT] (8/3) > {val1} [INT]  :  123
[DICT] (8/4) > {val2} [STR]  :  '123'
[DICT] (8/5) > {val3} [INT]  :  123
[DICT] (8/6) > {val4} [STR]  :  '123'
[DICT] (8/7) > {val5} [INT]  :  123
[DICT] (8/8) > {val6} [STR]  :  '123'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0303"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (nested) (valid syntax)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Checklist rule 5"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0303.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (7/1) > {ara} [STR]  :  'ara'
[DICT] (7/2) > {lara} [LIST] (1/1) > [STR]  :  'ara'
[DICT] (7/3) > {param} [INT]  :  123
[DICT] (7/4) > {param1} [LIST] (1/1) > [FLOAT]  :  4.56
[DICT] (7/5) > {val1} [STR]  :  '123'
[DICT] (7/6) > {val2} [STR]  :  '4.56'
[DICT] (7/7) > {val3} [STR]  :  '4.56'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0304"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (valid syntax)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Checklist rule 6"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0304.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (10/1) > {param1} [STR]  :  'param1'
[DICT] (10/2) > {param2} [STR]  :  'param2'
[DICT] (10/3) > {param3} [LIST] (2/1) > [INT]  :  123
[DICT] (10/3) > {param3} [LIST] (2/2) > [FLOAT]  :  4.56
[DICT] (10/4) > {lara} [LIST] (1/1) > [STR]  :  'ara'
[DICT] (10/5) > {ara} [STR]  :  'ara'
[DICT] (10/6) > {val1} [STR]  :  'param1param2'
[DICT] (10/7) > {val2} [STR]  :  '1234.56'
[DICT] (10/8) > {val3} [STR]  :  '1234.56'
[DICT] (10/9) > {val4} [STR]  :  'ABC, param1, param2, XYZ'
[DICT] (10/10) > {val5} [STR]  :  'param1, ABC ; XYZ / param2'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0350"
dictUsecase['DESCRIPTION']       = "JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax 1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 1 / pattern 1"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0350.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0351"
dictUsecase['DESCRIPTION']       = "JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax 2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 1 / pattern 2"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0351.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0352"
dictUsecase['DESCRIPTION']       = "JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax 3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 1 / pattern 3"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0352.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0353"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 1"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0353.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0354"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 2"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0354.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0355"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 3"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0355.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid nested parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0356"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 4)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 4"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0356.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "One or more than one opened or closed curly bracket is missing in expression"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0357"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 5)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 5"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0357.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0358"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 6)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 6"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0358.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "One or more than one opened or closed curly bracket is missing in expression" # wording to be improved (issues/109)
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0359"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 6)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 7"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0359.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0360"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 9)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 2 / pattern 8"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0360.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "One or more than one opened or closed curly bracket is missing in expression"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0361"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 3 / pattern 1"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0361.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting property name enclosed in double quotes"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0362"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 3 / pattern 2"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0362.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid nested parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0363"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 3 / pattern 3"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0363.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid nested parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0364"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 4)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 3 / pattern 4"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0364.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid nested parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0365"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 5)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 3 / pattern 5"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0365.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid nested parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0366"
dictUsecase['DESCRIPTION']       = "JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 6)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 3 / pattern 6"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0366.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid nested parameter format"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0367"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 6 / pattern 1"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0367.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0368"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 6 / pattern 2"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0368.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0369"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 6 / pattern 3"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0369.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0370"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 4)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 6 / pattern 4"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0370.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0371"
dictUsecase['DESCRIPTION']       = "JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 5)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "VALUE_DETECTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Checklist rule 6 / pattern 5"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0371.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The double quotes are missing"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0450"
dictUsecase['DESCRIPTION']       = "JSON file with parameter name containing not allowed special characters"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "NAMING_CONVENTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0450.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "detected unexpected characters in parameter name (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0500"
dictUsecase['DESCRIPTION']       = "JSON file with composite data structure (nested lists and dictionaries 1)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Standard notation"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0500.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/1) > {dict_1_key_1} [STR]  :  'dict_1_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/2) > {dict_1_key_2} [LIST] (2/1) > [STR]  :  'dict_1_key_2 value 1'
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/2) > {dict_1_key_2} [LIST] (2/2) > [STR]  :  'dict_1_key_2 value 2'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/1) > {dict_2_key_1} [STR]  :  'dict_2_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/1) > {dict_2_A_key_1} [STR]  :  'dict_2_A_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/1) > [STR]  :  'dict_2_A_key_2 list value 1'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/2) > [STR]  :  'dict_2_A_key_2 list value 2'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/3) > [DICT] (2/1) > {dict_2_A_key_2_subkey_1} [STR]  :  'dict_2_A_key_2_subkey_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/3) > [DICT] (2/2) > {dict_2_A_key_2_subkey_2} [LIST] (2/1) > [STR]  :  'value_1'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/3) > [DICT] (2/2) > {dict_2_A_key_2_subkey_2} [LIST] (2/2) > [STR]  :  'value_2'
[DICT] (2/2) > {param} [STR]  :  'value_2'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0501"
dictUsecase['DESCRIPTION']       = "JSON file with composite data structure (nested lists and dictionaries 2)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Dotdict notation"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0501.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/1) > {dict_1_key_1} [STR]  :  'dict_1_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/2) > {dict_1_key_2} [LIST] (2/1) > [STR]  :  'dict_1_key_2 value 1'
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/2) > {dict_1_key_2} [LIST] (2/2) > [STR]  :  'dict_1_key_2 value 2'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/1) > {dict_2_key_1} [STR]  :  'dict_2_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/1) > {dict_2_A_key_1} [STR]  :  'dict_2_A_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/1) > [STR]  :  'dict_2_A_key_2 list value 1'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/2) > [STR]  :  'dict_2_A_key_2 list value 2'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/3) > [DICT] (2/1) > {dict_2_A_key_2_subkey_1} [STR]  :  'dict_2_A_key_2_subkey_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/3) > [DICT] (2/2) > {dict_2_A_key_2_subkey_2} [LIST] (2/1) > [STR]  :  'value_1'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict_2_A_key_2} [LIST] (3/3) > [DICT] (2/2) > {dict_2_A_key_2_subkey_2} [LIST] (2/2) > [STR]  :  'value_2'
[DICT] (2/2) > {param} [STR]  :  'value_2'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0502"
dictUsecase['DESCRIPTION']       = "JSON file with composite data structure (nested lists and dictionaries 3 / some key names with dots inside)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Standard notation"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0502.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/1) > {dict_1_key_1} [STR]  :  'dict_1_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/2) > {dict_1_key_2} [LIST] (2/1) > [STR]  :  'dict_1_key_2 value 1'
[DICT] (2/1) > {params} [LIST] (2/1) > [DICT] (2/2) > {dict_1_key_2} [LIST] (2/2) > [STR]  :  'dict_1_key_2 value 2'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/1) > {dict_2_key_1} [STR]  :  'dict_2_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/1) > {dict.2.A.key.1} [STR]  :  'dict_2_A_key_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict.2.A.key.2} [LIST] (3/1) > [STR]  :  'dict_2_A_key_2 list value 1'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict.2.A.key.2} [LIST] (3/2) > [STR]  :  'dict_2_A_key_2 list value 2'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict.2.A.key.2} [LIST] (3/3) > [DICT] (2/1) > {dict_2_A_key_2_subkey_1} [STR]  :  'dict_2_A_key_2_subkey_1 value'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict.2.A.key.2} [LIST] (3/3) > [DICT] (2/2) > {dict_2_A_key_2_subkey_2} [LIST] (2/1) > [STR]  :  'value_1'
[DICT] (2/1) > {params} [LIST] (2/2) > [DICT] (2/2) > {dict_2_key_2} [DICT] (2/2) > {dict.2.A.key.2} [LIST] (3/3) > [DICT] (2/2) > {dict_2_A_key_2_subkey_2} [LIST] (2/2) > [STR]  :  'value_2'
[DICT] (2/2) > {param} [STR]  :  'value_2'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0503"
dictUsecase['DESCRIPTION']       = "JSON file with composite data structure (some lists)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0503.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (10/1) > {param1} [LIST] (1/1) > [LIST] (1/1) > [LIST] (1/1) > [LIST] (1/1) > [INT]  :  1
[DICT] (10/2) > {val1} [INT]  :  1
[DICT] (10/3) > {val2} [STR]  :  '1'
[DICT] (10/4) > {val3} [INT]  :  1
[DICT] (10/5) > {val4} [STR]  :  '1'
[DICT] (10/6) > {lparam2} [LIST] (1/1) > [INT]  :  1
[DICT] (10/7) > {lparam3} [LIST] (2/1) > [INT]  :  0
[DICT] (10/7) > {lparam3} [LIST] (2/2) > [INT]  :  2
[DICT] (10/8) > {lparam4} [LIST] (3/1) > [INT]  :  0
[DICT] (10/8) > {lparam4} [LIST] (3/2) > [INT]  :  1
[DICT] (10/8) > {lparam4} [LIST] (3/3) > [INT]  :  2
[DICT] (10/9) > {val5} [INT]  :  2
[DICT] (10/10) > {val6} [STR]  :  '2'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0504"
dictUsecase['DESCRIPTION']       = "JSON file with composite data structure (some dictionaries)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0504.jsonp"       # current issue: Expecting value: line 20 column 14 (char 1088)'!
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (20/1) > {param1} [DICT] (1/1) > {A} [DICT] (1/1) > {B} [DICT] (1/1) > {C} [DICT] (1/1) > {D} [FLOAT]  :  1.23
[DICT] (20/2) > {param2} [DICT] (1/1) > {E} [DICT] (1/1) > {F} [DICT] (1/1) > {G} [DICT] (1/1) > {H} [STR]  :  'X'
[DICT] (20/3) > {param3} [DICT] (1/1) > {K} [DICT] (1/1) > {L} [DICT] (1/1) > {M} [DICT] (1/1) > {N} [STR]  :  'Y'
[DICT] (20/4) > {param4} [DICT] (1/1) > {O} [DICT] (1/1) > {P} [DICT] (1/1) > {Q} [DICT] (1/1) > {R} [STR]  :  'Z'
[DICT] (20/5) > {param5} [DICT] (1/1) > {X} [DICT] (1/1) > {Y} [DICT] (1/1) > {Z} [INT]  :  345
[DICT] (20/6) > {val1} [FLOAT]  :  1.23
[DICT] (20/7) > {val2} [STR]  :  '1.23'
[DICT] (20/8) > {val3} [FLOAT]  :  1.23
[DICT] (20/9) > {val4} [STR]  :  '1.23'
[DICT] (20/10) > {val5} [STR]  :  'X'
[DICT] (20/11) > {val6} [STR]  :  'Y'
[DICT] (20/12) > {val7} [STR]  :  'Z'
[DICT] (20/13) > {val8} [INT]  :  345
[DICT] (20/14) > {val9} [STR]  :  '345'
[DICT] (20/15) > {val10} [INT]  :  345
[DICT] (20/16) > {val11} [STR]  :  '345'
[DICT] (20/17) > {val12} [INT]  :  345
[DICT] (20/18) > {val13} [STR]  :  '345'
[DICT] (20/19) > {val14} [INT]  :  345
[DICT] (20/20) > {val15} [STR]  :  '345'
"""
# # # listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0505"
dictUsecase['DESCRIPTION']       = "JSON file with composite strings containing several times a colon and a comma (JSON syntax elements)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0505.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (5/1) > {param1} [STR]  :  'value :,: 1'
[DICT] (5/2) > {param2} [STR]  :  'value :,: 2'
[DICT] (5/3) > {val1} [STR]  :  'The values are: 'value :,: 1' and: 'value :,: 2', and so on'
[DICT] (5/4) > {val2} [STR]  :  'The values are: 'value :,: 1' and: 'value :,: 2', and so on'
[DICT] (5/5) > {val3} [STR]  :  ':'The values are: 'value :,: 1' and: 'value :,: 2', and so on'::,::'The values are: 'value :,: 1' and: 'value :,: 2', and so on':'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0506"
dictUsecase['DESCRIPTION']       = "JSON file with composite strings containing several combinations of curly brackets and special characters before"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0506.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (12/1) > {param1} [DICT] (2/1) > {A} [INT]  :  1
[DICT] (12/1) > {param1} [DICT] (2/2) > {B} [INT]  :  2
[DICT] (12/2) > {param2} [LIST] (3/1) > [INT]  :  1
[DICT] (12/2) > {param2} [LIST] (3/2) > [INT]  :  2
[DICT] (12/2) > {param2} [LIST] (3/3) > [INT]  :  3
[DICT] (12/3) > {param3} [STR]  :  'value'
[DICT] (12/4) > {var1} [STR]  :  'value 1 > {'A': 1, 'B': 2}'
[DICT] (12/5) > {var2} [STR]  :  'value 2 > [1, 2, 3]'
[DICT] (12/6) > {var3} [STR]  :  'value 3 > value'
[DICT] (12/7) > {var4} [STR]  :  'value 4 > &{param1}'
[DICT] (12/8) > {var5} [STR]  :  'value 5 > &{param2}'
[DICT] (12/9) > {var6} [STR]  :  'value 6 > &{param3}'
[DICT] (12/10) > {var7} [STR]  :  'value 7 > @{param1}'
[DICT] (12/11) > {var8} [STR]  :  'value 8 > @{param2}'
[DICT] (12/12) > {var9} [STR]  :  'value 9 > @{param3}'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0507"
dictUsecase['DESCRIPTION']       = "JSON file containing several string concatenations in separate lines (1)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0507.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (1/1) > {teststring_1} [STR]  :  'prefix.teststring_1.value.suffix-1.suffix-2.suffix-3'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0508"
dictUsecase['DESCRIPTION']       = "JSON file containing several string concatenations in separate lines (2)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0508.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (1/1) > {teststring_1} [STR]  :  'teststring_1.value.suffix-1'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
# can be combined with previous test cases after issue is solved
dictUsecase['TESTID']            = "JPP_0509"
dictUsecase['DESCRIPTION']       = "JSON file containing several parameter assignments in separate lines (different syntax)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0509.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (1/1) > {teststring} [STR]  :  'teststring.value.5'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
# can be combined with previous test cases after issue is solved
dictUsecase['TESTID']            = "JPP_0510"
dictUsecase['DESCRIPTION']       = "JSON file containing several parameter assignments in separate lines (extended string concatenation)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0510.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (1/1) > {params} [DICT] (1/1) > {global} [DICT] (4/1) > {teststring_1} [STR]  :  'prefix.teststring_1.value.suffix_1.suffix_2.suffix_3'
[DICT] (1/1) > {params} [DICT] (1/1) > {global} [DICT] (4/2) > {teststring_2} [STR]  :  'teststring_2.value.suffix_1'
[DICT] (1/1) > {params} [DICT] (1/1) > {global} [DICT] (4/3) > {teststring_3} [STR]  :  'teststring_3.value.5'
[DICT] (1/1) > {params} [DICT] (1/1) > {global} [DICT] (4/4) > {testdict} [DICT] (1/1) > {key} [DICT] (1/1) > {teststring_4} [STR]  :  'teststring_4.initial_value.suffix_1.suffix_2'"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0511"
dictUsecase['DESCRIPTION']       = "JSON file containing a list; list index is defined by a parameter"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0511.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (2/1) > {intval} [INT]  :  1
[DICT] (2/2) > {listval} [LIST] (2/1) > [STR]  :  'B'
[DICT] (2/2) > {listval} [LIST] (2/2) > [INT]  :  4"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0512"
dictUsecase['DESCRIPTION']       = "JSON file containing a nested use of lists and dictionaries, with the same parameter used several times within the same expression"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0512.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (4/1) > {dict_param} [DICT] (2/1) > {A} [INT]  :  0
[DICT] (4/1) > {dict_param} [DICT] (2/2) > {B} [INT]  :  1
[DICT] (4/2) > {list_param} [LIST] (2/1) > [STR]  :  'A'
[DICT] (4/2) > {list_param} [LIST] (2/2) > [STR]  :  'B'
[DICT] (4/3) > {param1} [STR]  :  'A'
[DICT] (4/4) > {param2} [STR]  :  '0'"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0513"
dictUsecase['DESCRIPTION']       = "JSON file containing several square bracket expressions (as list index and dictionary key) with and without single quotes"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0513.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (21/1) > {intparam} [INT]  :  0
[DICT] (21/2) > {stringparam} [STR]  :  'A'
[DICT] (21/3) > {listparam} [LIST] (2/1) > [STR]  :  'C'
[DICT] (21/3) > {listparam} [LIST] (2/2) > [STR]  :  'D'
[DICT] (21/4) > {dictparam} [DICT] (3/1) > {0} [INT]  :  3
[DICT] (21/4) > {dictparam} [DICT] (3/2) > {A} [INT]  :  5
[DICT] (21/4) > {dictparam} [DICT] (3/3) > {B} [INT]  :  6
[DICT] (21/5) > {val01} [STR]  :  'A'
[DICT] (21/6) > {val02} [STR]  :  'B'
[DICT] (21/7) > {val03} [INT]  :  0
[DICT] (21/8) > {val04} [INT]  :  1
[DICT] (21/9) > {val05} [INT]  :  1
[DICT] (21/10) > {val06} [INT]  :  1
[DICT] (21/11) > {val07} [STR]  :  'A'
[DICT] (21/12) > {val08} [STR]  :  'B'
[DICT] (21/13) > {val09} [STR]  :  '0'
[DICT] (21/14) > {val10} [STR]  :  '1'
[DICT] (21/15) > {val11} [STR]  :  '1'
[DICT] (21/16) > {val12} [STR]  :  '1'
[DICT] (21/17) > {C} [STR]  :  'E'
[DICT] (21/18) > {D} [STR]  :  'F'
[DICT] (21/19) > {3} [INT]  :  3
[DICT] (21/20) > {5} [INT]  :  5
[DICT] (21/21) > {6} [INT]  :  6"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0514"
dictUsecase['DESCRIPTION']       = "JSON file containing nested dollar operator expressions"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0514.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (5/1) > {keyP} [STR]  :  'A'
[DICT] (5/2) > {B} [INT]  :  1
[DICT] (5/3) > {dictP} [DICT] (2/1) > {A} [STR]  :  'B'
[DICT] (5/3) > {dictP} [DICT] (2/2) > {C} [INT]  :  2
[DICT] (5/4) > {newparam_1} [STR]  :  '1'
[DICT] (5/5) > {newparam_2} [STR]  :  '1'"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0515"
dictUsecase['DESCRIPTION']       = "JSON file containing nested dollar operator expressions"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0515.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (12/1) > {keyP} [STR]  :  'A'
[DICT] (12/2) > {B} [STR]  :  'keyP'
[DICT] (12/3) > {dictP} [DICT] (1/1) > {A} [STR]  :  'B'
[DICT] (12/4) > {newparam_1} [STR]  :  'B'
[DICT] (12/5) > {newparam_2} [STR]  :  'keyP'
[DICT] (12/6) > {newparam_3} [STR]  :  'A'
[DICT] (12/7) > {newparam_4} [STR]  :  'B'
[DICT] (12/8) > {newparam_5} [STR]  :  'keyP'
[DICT] (12/9) > {newparam_6} [STR]  :  'A'
[DICT] (12/10) > {newparam_7} [STR]  :  'B'
[DICT] (12/11) > {newparam_8} [STR]  :  'keyP'
[DICT] (12/12) > {newparam_9} [STR]  :  'A'"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0516"
dictUsecase['DESCRIPTION']       = "JSON file containing string expressions with additional curly brackets and dollar characters (that must not cause syntax issues!)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns expected value"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0516.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (9/1) > {listparam} [LIST] (3/1) > [STR]  :  'A'
[DICT] (9/1) > {listparam} [LIST] (3/2) > [STR]  :  'B'
[DICT] (9/1) > {listparam} [LIST] (3/3) > [STR]  :  'C'
[DICT] (9/2) > {param_1} [STR]  :  '}A{'
[DICT] (9/3) > {param_2} [STR]  :  '{A}'
[DICT] (9/4) > {param_3} [STR]  :  '$}A$}'
[DICT] (9/5) > {param_4} [STR]  :  '{$}A{$}'
[DICT] (9/6) > {param_5} [STR]  :  '}{$}A{$}{'
[DICT] (9/7) > {param_6} [STR]  :  '{}{$}A{$}{}'
[DICT] (9/8) > {param_7} [STR]  :  '{}A{$}B{$}C{}'
[DICT] (9/9) > {param_8} [STR]  :  '{}$A{$$}$B{$$}$C{}'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0550"
dictUsecase['DESCRIPTION']       = "JSON file with composite data structure (nested lists and dictionaries / some key names with dots inside)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "Dotdict notation (ambiguous in this case)"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0550.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "is not available"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0551"
dictUsecase['DESCRIPTION']       = "JSON file containing a list; list index is defined by a parameter and wrapped in single quotes"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = "List indices must be of type 'int'"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0551.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Could not set variable '${listval}['${intval}']' with value '4'! Reason: list indices must be integers"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0552"
dictUsecase['DESCRIPTION']       = "JSON file containing a list; list index is defined by a parameter and placed inside the curly brackets (invalid syntax)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0552.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index or sub-element inside curly brackets in the parameter '${listval[${intval}]}'"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0553"
dictUsecase['DESCRIPTION']       = "JSON file containing a list; list index is defined by a parameter, wrapped in single quotes and placed inside the curly brackets (invalid syntax)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0553.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index or sub-element inside curly brackets in the parameter '${listval['${intval}']}'"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0554"
dictUsecase['DESCRIPTION']       = "JSON file containing a dictionary; the dictionary key is defined by a parameter and placed inside the curly brackets (invalid syntax)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0554.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index or sub-element inside curly brackets"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0555"
dictUsecase['DESCRIPTION']       = "JSON file containing a dictionary; the dictionary key is defined by a parameter, wrapped in single quotes and placed inside the curly brackets (invalid syntax)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMPOSITE_EXPRESSIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0555.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid syntax: Found index or sub-element inside curly brackets"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0600"
dictUsecase['DESCRIPTION']       = "JSON file with several combinations of code comments"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns remaining content of JSON file (valid parameters)"
dictUsecase['SECTION']           = "CODE_COMMENTS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0600.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (6/1) > {param1} [STR]  :  'value1'
[DICT] (6/2) > {param2} [STR]  :  'value2'
[DICT] (6/3) > {testdict1} [DICT] (3/1) > {A} [INT]  :  1
[DICT] (6/3) > {testdict1} [DICT] (3/2) > {B} [INT]  :  2
[DICT] (6/3) > {testdict1} [DICT] (3/3) > {C} [INT]  :  3
[DICT] (6/4) > {testdict2} [DICT] (2/1) > {A} [INT]  :  1
[DICT] (6/4) > {testdict2} [DICT] (2/2) > {C} [INT]  :  3
[DICT] (6/5) > {testdict3} [DICT] (2/1) > {A} [INT]  :  1
[DICT] (6/5) > {testdict3} [DICT] (2/2) > {D} [INT]  :  4
[DICT] (6/6) > {testlist} [LIST] (2/1) > [STR]  :  'A1'
[DICT] (6/6) > {testlist} [LIST] (2/2) > [STR]  :  'D4'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0950"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0950.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting ':' delimiter:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0951"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0951.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "No closing quotation in line"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0952"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0952.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting ',' delimiter:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0953"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (4): file is completely empty"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0953.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting value:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0954"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (5): file is empty (multiple pairs of brackets only)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0954.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting property name enclosed in double quotes:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# # >> needs clarification
# # https://github.com/test-fullautomation/python-jsonpreprocessor/issues/104
# dictUsecase = {}
# dictUsecase['TESTID']            = "JPP_0955"
# dictUsecase['DESCRIPTION']       = "JSON file with index applied to string variable"
# dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
# dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
# dictUsecase['SUBSECTION']        = "BADCASE"
# dictUsecase['HINT']              = None
# dictUsecase['COMMENT']           = None
# dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0955.jsonp"
# dictUsecase['EXPECTEDEXCEPTION'] = None
# dictUsecase['EXPECTEDRETURN']    = None
# listofdictUsecases.append(dictUsecase)
# del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1000"
dictUsecase['DESCRIPTION']       = "JSON file with dictionary keys to be created implicitly"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1000.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (2/1) > {dTestDict} [DICT] (5/1) > {kVal_1} [STR]  :  'Val_1'
[DICT] (2/1) > {dTestDict} [DICT] (5/2) > {kVal_2} [DICT] (1/1) > {I_am_not_existing_1} [DICT] (1/1) > {I_am_not_existing_2} [STR]  :  'Val_1'
[DICT] (2/1) > {dTestDict} [DICT] (5/3) > {kVal_3} [DICT] (1/1) > {I_am_not_existing_3} [DICT] (1/1) > {I_am_not_existing_4} [STR]  :  'Val_1_extended'
[DICT] (2/1) > {dTestDict} [DICT] (5/4) > {kVal_3b} [DICT] (1/1) > {I_am_not_existing_3b} [DICT] (1/1) > {I_am_not_existing_4b} [STR]  :  'Val_1'
[DICT] (2/1) > {dTestDict} [DICT] (5/5) > {kVal_4} [DICT] (1/1) > {kVal_4B} [DICT] (1/1) > {kVal_4C} [DICT] (3/1) > {A} [INT]  :  1
[DICT] (2/1) > {dTestDict} [DICT] (5/5) > {kVal_4} [DICT] (1/1) > {kVal_4B} [DICT] (1/1) > {kVal_4C} [DICT] (3/2) > {B} [LIST] (2/1) > [INT]  :  1
[DICT] (2/1) > {dTestDict} [DICT] (5/5) > {kVal_4} [DICT] (1/1) > {kVal_4B} [DICT] (1/1) > {kVal_4C} [DICT] (3/2) > {B} [LIST] (2/2) > [INT]  :  2
[DICT] (2/1) > {dTestDict} [DICT] (5/5) > {kVal_4} [DICT] (1/1) > {kVal_4B} [DICT] (1/1) > {kVal_4C} [DICT] (3/3) > {kVal_4D} [DICT] (1/1) > {kVal_4E} [DICT] (1/1) > {kVal_4F} [DICT] (1/1) > {kVal_4G} [DICT] (2/1) > {C} [INT]  :  2
[DICT] (2/1) > {dTestDict} [DICT] (5/5) > {kVal_4} [DICT] (1/1) > {kVal_4B} [DICT] (1/1) > {kVal_4C} [DICT] (3/3) > {kVal_4D} [DICT] (1/1) > {kVal_4E} [DICT] (1/1) > {kVal_4F} [DICT] (1/1) > {kVal_4G} [DICT] (2/2) > {D} [LIST] (2/1) > [INT]  :  3
[DICT] (2/1) > {dTestDict} [DICT] (5/5) > {kVal_4} [DICT] (1/1) > {kVal_4B} [DICT] (1/1) > {kVal_4C} [DICT] (3/3) > {kVal_4D} [DICT] (1/1) > {kVal_4E} [DICT] (1/1) > {kVal_4F} [DICT] (1/1) > {kVal_4G} [DICT] (2/2) > {D} [LIST] (2/2) > [INT]  :  4
[DICT] (2/2) > {Val_1_extended} [STR]  :  'Val_1'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1001"
dictUsecase['DESCRIPTION']       = "JSON file with dictionary keys to be created implicitly (same key names at all levels)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1001.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (3/1) > {param1} [DICT] (1/1) > {subkey} [DICT] (1/1) > {subkey} [DICT] (1/1) > {subkey} [STR]  :  'subkey value'
[DICT] (3/2) > {param2} [DICT] (1/1) > {subkey} [DICT] (1/1) > {subkey} [DICT] (1/1) > {subkey} [STR]  :  'subkey value extended'
[DICT] (3/3) > {param3} [DICT] (1/1) > {subkey} [DICT] (1/1) > {subkey} [DICT] (2/1) > {paramA} [STR]  :  'subkey value extended'
[DICT] (3/3) > {param3} [DICT] (1/1) > {subkey} [DICT] (1/1) > {subkey} [DICT] (2/2) > {paramB} [STR]  :  'subkey value extended'
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1002"
dictUsecase['DESCRIPTION']       = "JSON file with combinations of implicit and explicit creation / with and without initialization"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1002.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (5/1) > {testdict_1} [DICT] (1/1) > {subKey} [DICT] (1/1) > {subKey} [DICT] (1/1) > {paramA} [DICT] (1/1) > {A} [INT]  :  1
[DICT] (5/2) > {paramD} [STR]  :  'D'
[DICT] (5/3) > {paramE} [STR]  :  'E'
[DICT] (5/4) > {testdict_2} [DICT] (1/1) > {subKey} [DICT] (1/1) > {subKey} [DICT] (1/1) > {paramA} [DICT] (3/1) > {B} [INT]  :  2
[DICT] (5/4) > {testdict_2} [DICT] (1/1) > {subKey} [DICT] (1/1) > {subKey} [DICT] (1/1) > {paramA} [DICT] (3/2) > {paramB} [DICT] (1/1) > {C} [INT]  :  3
[DICT] (5/4) > {testdict_2} [DICT] (1/1) > {subKey} [DICT] (1/1) > {subKey} [DICT] (1/1) > {paramA} [DICT] (3/3) > {paramC} [DICT] (1/1) > {D} [INT]  :  4
[DICT] (5/5) > {testdict_3} [DICT] (1/1) > {paramD} [DICT] (1/1) > {paramE} [DICT] (1/1) > {paramD} [DICT] (1/1) > {E} [DICT] (1/1) > {F} [INT]  :  6
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
# ====== still one line in jpp-test_config_1003.jsonp commented out; remaining code run properly
dictUsecase['TESTID']            = "JPP_1003"
dictUsecase['DESCRIPTION']       = "JSON file with combinations of implicit and explicit creation / access to implicitly created keys by parameters / dict assignment by reference"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns values"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1003.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = """
[DICT] (7/1) > {testdict2} [DICT] (1/1) > {subKey1} [DICT] (1/1) > {subKey2} [DICT] (1/1) > {subKey3} [DICT] (1/1) > {subKey4} [INT]  :  3
[DICT] (7/2) > {param1} [STR]  :  'subKey1'
[DICT] (7/3) > {param2} [STR]  :  'subKey2'
[DICT] (7/4) > {param3} [STR]  :  'subKey3'
[DICT] (7/5) > {param4} [STR]  :  'subKey4'
[DICT] (7/6) > {param5} [INT]  :  3
[DICT] (7/7) > {testdict1} [DICT] (1/1) > {subKey1} [DICT] (1/1) > {subKey2} [DICT] (1/1) > {subKey3} [DICT] (1/1) > {subKey4} [INT]  :  3
"""
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1050"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1050.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The implicit creation of data structures based on nested parameter is not supported"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1051"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1051.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The implicit creation of data structures based on nested parameter is not supported"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1052"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1052.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The implicit creation of data structures based on nested parameter is not supported"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1053"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (4)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1053.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1054"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (5)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1054.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1055"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (5)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1055.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "only simple data types are allowed to be substituted inside"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1056"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (6)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1056.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The implicit creation of data structures based on nested parameter is not supported"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1057"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (7)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1057.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The implicit creation of data structures based on nested parameter is not supported"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1058"
dictUsecase['DESCRIPTION']       = "JSON file with implicit creation of data structures based on parameters (8)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "IMPLICIT_CREATION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1058.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "The implicit creation of data structures based on nested parameter is not supported"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1150"
dictUsecase['DESCRIPTION']       = "JSON file with cyclic imports (JSON file imports itself)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "CYCLIC_IMPORTS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1150.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Cyclic imported json file"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1151"
dictUsecase['DESCRIPTION']       = "JSON file with cyclic imports (JSON file imports another file, that is already imported)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "CYCLIC_IMPORTS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_1151.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Cyclic imported json file"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_1200"
# In all other use cases the path 'JSONFILE' is normalized by the self test (component_test.py) before the JsonPreprocessor is called.
# The reference for relative paths is the position of this file.
# In this use case the path 'JSONFILE' is not normalized by the self test.
# Therefore the path must be relative to the position of the executing script (in this case: component_test.py).
dictUsecase['DESCRIPTION']       = "Relative path to JSON file"
dictUsecase['EXPECTATION']       = "JsonPreprocessor resolves the relative path and returns values from JSON file"
dictUsecase['SECTION']           = "PATH_FORMATS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = "Works with raw path to JSON file (path not normalized internally)"
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_1200.jsonp"
dictUsecase['USERAWPATH']        = True
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = "[DICT] (1/1) > {teststring} [STR]  :  'relative path teststring value'"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------






