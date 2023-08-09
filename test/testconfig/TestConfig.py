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
# 09.08.2023
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
[DICT] (53/53) > {param_101} [LIST] (51/20) > [INT]  :  123
[DICT] (53/53) > {param_101} [LIST] (51/21) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/22) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/23) > [STR]  :  '123'
[DICT] (53/53) > {param_101} [LIST] (51/24) > [FLOAT]  :  4.56
[DICT] (53/53) > {param_101} [LIST] (51/25) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/26) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/27) > [STR]  :  '4.56'
[DICT] (53/53) > {param_101} [LIST] (51/28) > [BOOL]  :  True
[DICT] (53/53) > {param_101} [LIST] (51/29) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/30) > [STR]  :  'true'
[DICT] (53/53) > {param_101} [LIST] (51/31) > [STR]  :  'true'
[DICT] (53/53) > {param_101} [LIST] (51/32) > [BOOL]  :  False
[DICT] (53/53) > {param_101} [LIST] (51/33) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/34) > [STR]  :  'false'
[DICT] (53/53) > {param_101} [LIST] (51/35) > [STR]  :  'false'
[DICT] (53/53) > {param_101} [LIST] (51/36) > [NONE]  :  None
[DICT] (53/53) > {param_101} [LIST] (51/37) > [STR]  :  'None'
[DICT] (53/53) > {param_101} [LIST] (51/38) > [STR]  :  'null'
[DICT] (53/53) > {param_101} [LIST] (51/39) > [STR]  :  'null'
[DICT] (53/53) > {param_101} [LIST] (51/40) > [BOOL]  :  True
[DICT] (53/53) > {param_101} [LIST] (51/41) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/42) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/43) > [STR]  :  'True'
[DICT] (53/53) > {param_101} [LIST] (51/44) > [BOOL]  :  False
[DICT] (53/53) > {param_101} [LIST] (51/45) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/46) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/47) > [STR]  :  'False'
[DICT] (53/53) > {param_101} [LIST] (51/48) > [NONE]  :  None
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
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (21/1) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (21/2) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (21/2) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (21/3) > {list_variant_index} [INT]  :  0
[DICT] (21/4) > {variant_number} [STR]  :  '1'
[DICT] (21/5) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (21/5) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (21/6) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (21/7) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (21/8) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (21/9) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (21/10) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (21/11) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (21/12) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (21/13) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (21/13) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (21/13) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (21/14) > {list_milestone_index} [INT]  :  1
[DICT] (21/15) > {milestone_number} [STR]  :  '2'
[DICT] (21/16) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (21/16) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (21/16) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (21/17) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (21/18) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (21/19) > {ilesto} [STR]  :  'ilesto'
[DICT] (21/20) > {milestone} [STR]  :  'milestone'
[DICT] (21/21) > {variant_1} [STR]  :  'VARIANT-1 (new value)'
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
[DICT] (21/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (21/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (21/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (21/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (21/4) > {list_variant_index} [INT]  :  0
[DICT] (21/5) > {variant_number} [STR]  :  '1'
[DICT] (21/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (21/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (21/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (21/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (21/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (21/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (21/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (21/12) > {milestone_2} [STR]  :  'MILESTONE-2 (new value)'
[DICT] (21/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (21/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (21/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (21/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (21/15) > {list_milestone_index} [INT]  :  1
[DICT] (21/16) > {milestone_number} [STR]  :  '2'
[DICT] (21/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (21/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (21/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR-VARIANT-1_MS-milestone_2_param} [STR]  :  'value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR-VARIANT-1_MS-milestone_2_param} [STR]  :  'value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR-VARIANT-1_MS-MILESTONE-2 value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR-VARIANT-1_MS-MILESTONE-2 value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR-VARIANT-1_MS-MILESTONE-2_param} [STR]  :  'value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {VAR-VARIANT-1_MS-MILESTONE-2_param} [STR]  :  'value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR-VARIANT-1_MS-MILESTONE-2 value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (22/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/1) > [INT]  :  1
[DICT] (22/3) > {list_variant_numbers} [LIST] (2/2) > [INT]  :  2
[DICT] (22/4) > {list_variant_index} [INT]  :  0
[DICT] (22/5) > {variant_number} [STR]  :  '1'
[DICT] (22/6) > {dict_variants} [DICT] (2/1) > {variant_1} [STR]  :  'VARIANT-1'
[DICT] (22/6) > {dict_variants} [DICT] (2/2) > {variant_2} [STR]  :  'VARIANT-2'
[DICT] (22/7) > {variant_key_1} [STR]  :  'variant_1'
[DICT] (22/8) > {INNERMOST_VARIANT_VALUE} [STR]  :  'RIA'
[DICT] (22/9) > {ARIAN} [STR]  :  'ARIAN'
[DICT] (22/10) > {VARIANT} [STR]  :  'VARIANT'
[DICT] (22/11) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/12) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/13) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/1) > [INT]  :  1
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/2) > [INT]  :  2
[DICT] (22/14) > {list_milestone_numbers} [LIST] (3/3) > [INT]  :  3
[DICT] (22/15) > {list_milestone_index} [INT]  :  1
[DICT] (22/16) > {milestone_number} [STR]  :  '2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/1) > {milestone_1} [STR]  :  'MILESTONE-1'
[DICT] (22/17) > {dict_milestones} [DICT] (3/2) > {milestone_2} [STR]  :  'MILESTONE-2'
[DICT] (22/17) > {dict_milestones} [DICT] (3/3) > {milestone_3} [STR]  :  'MILESTONE-3'
[DICT] (22/18) > {milestone_key_2} [STR]  :  'milestone_2'
[DICT] (22/19) > {innermost_milestone_name} [STR]  :  'est'
[DICT] (22/20) > {ilesto} [STR]  :  'ilesto'
[DICT] (22/21) > {milestone} [STR]  :  'milestone'
[DICT] (22/22) > {param} [STR]  :  'VAR-VARIANT-1_MS-MILESTONE-2 value'
"""
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "composite data types not allowed in names (placeholder)"
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
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (13/1) > {par1} [FLOAT]  :  1.23
[DICT] (13/1) > {par2} [LIST] (2/1) > [STR]  :  'A'
[DICT] (13/1) > {par2} [LIST] (2/2) > [STR]  :  'B'
[DICT] (13/2) > {par3} [LIST] (1/1) > [STR]  :  'par'
[DICT] (13/3) > {ara} [STR]  :  'ara'
[DICT] (13/4) > {param} [STR]  :  'param'
[DICT] (13/5) > {param2} [LIST] (1/1) > [STR]  :  'par'
[DICT] (13/6) > {val1} [STR]  :  '{par1}am}'
[DICT] (13/6) > {val2} [STR]  :  'param}'
[DICT] (13/6) > {val3} [STR]  :  'param}'
[DICT] (13/6) > {val4} [STR]  :  'param}'
[DICT] (13/6) > {val5} [STR]  :  'param2}[0]'
[DICT] (13/6) > {val6} [STR]  :  'param2.0}'
"""
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (10/1) > {ara} [STR]  :  'ara'
[DICT] (10/2) > {lara} [STR]  :  'ara'
[DICT] (10/3) > {param} [INT]  :  123
[DICT] (10/4) > {param} [LIST] (1/1) > [FLOAT]  :  4.56
[DICT] (10/5) > {val1} [INT]  :  123
[DICT] (10/6) > {val2} [STR]  :  '123'
[DICT] (10/7) > {val3} [STR]  :  [FLOAT]  :  4.56
[DICT] (10/8) > {val4} [STR]  :  [STR]  :  '4.56'
[DICT] (10/9) > {val5} [STR]  :  [FLOAT]  :  4.56
[DICT] (10/10) > {val6} [STR]  :  [STR]  :  '4.56'
"""
# # # listofdictUsecases.append(dictUsecase)
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
[DICT] (10/4) > {lara} [LIST] (1/1) > [STR]  :  "ara"
[DICT] (10/5) > {ara} [STR]  :  'ara'
[DICT] (10/6) > {val1} [STR]  :  'param1param2'
[DICT] (10/7) > {val2} [STR]  :  '1234.56'
[DICT] (10/8) > {val3} [STR]  :  '1234.56'
[DICT] (10/9) > {val4} [STR]  :  'ABC, param1, param2, XYZ'
[DICT] (10/10) > {val5} [STR]  :  'param1, ABC ; XYZ / param2'
"""
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "invalid syntax (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "Key name or value is a mix of nested parameters and hard coded parts"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "Key name or value is a mix of nested parameters and hard coded parts"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "Key name or value is a mix of nested parameters and hard coded parts"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "Key name or value is a mix of nested parameters and hard coded parts"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['EXPECTEDEXCEPTION'] = "Key name or value is a mix of nested parameters and hard coded parts"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0504.jsonp"
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
[DICT] (5/1) > {param1} [STR]  :  'value : 1'
[DICT] (5/2) > {param2} [STR]  :  'value : 2'
[DICT] (5/3) > {val1} [STR]  :  'The values are: 'value :,: 1' and: 'value :,: 2', and so on'
[DICT] (5/4) > {val2} [STR]  :  'The values are: 'value :,: 1' and: 'value :,: 2', and so on'
[DICT] (5/5) > {val3} [STR]  :  ':'The values are: 'value :,: 1' and: 'value :,: 2', and so on'::,::'The values are: 'value :,: 1' and: 'value :,: 2', and so on':'
"""
# # # listofdictUsecases.append(dictUsecase)
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
# # # listofdictUsecases.append(dictUsecase)
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
dictUsecase['COMMENT']           = "Needs clarification!"
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0550.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "detected ambiguous expression (= variable not found) (placeholder)"
dictUsecase['EXPECTEDRETURN']    = None
# # # listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0900"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error, that is commented out"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns remaining content of JSON file (valid parameters)"
dictUsecase['SECTION']           = "COMMON_SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r"..\testfiles\jpp-test_config_0900.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = "[DICT] (1/1) > {param} [STR]  :  'value'"
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







