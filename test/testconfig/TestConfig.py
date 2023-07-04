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
# 04.07.2023
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
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0001.jsonp"
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
[DICT] (15/11) > {param_11} [STR]  :  '"true"'
[DICT] (15/12) > {param_12} [BOOL]  :  False
[DICT] (15/13) > {param_13} [STR]  :  '"false"'
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
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0002.jsonp"
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
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0003.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = None
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
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0004.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
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
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0005.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase

# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0100"
dictUsecase['DESCRIPTION']       = "JSON file is empty (single pair of brackets only)"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns empty dictionary"
dictUsecase['SECTION']           = "DATA_INTGRITY"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0100.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = "[DICT]  :  {}"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0101"
dictUsecase['DESCRIPTION']       = "JSON file with string containing several separator characters and blanks; no parameters"
dictUsecase['EXPECTATION']       = "String is returned unchanged"
dictUsecase['SECTION']           = "DATA_INTGRITY"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0101.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = "[DICT] (1/1) > {teststring_data_integrity} [STR]  :  'a.1,b.2;c.3,d.4  ;  e.5  ,  f.6'"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0102"
dictUsecase['DESCRIPTION']       = "JSON file with string containing more special characters, masked special characters and escape sequences"
dictUsecase['EXPECTATION']       = "String is returned unchanged (but with masked special characters and escape sequences resolved)"
dictUsecase['SECTION']           = "DATA_INTGRITY"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0102.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = r"[DICT] (1/1) > {teststring_data_integrity} [STR]  :  'Ä.1/B.2\C.3$D.4&E.5?F.6=G.7#H.8~I.9§J.10,{K.11};L.12@M.12" + "\"N.13/Ö.14%1P.15;(Q.16),[R.17]'"
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0200"
dictUsecase['DESCRIPTION']       = "JSON file with composite string on right hand side of colon: parameters and hard coded string parts"
dictUsecase['EXPECTATION']       = "JsonPreprocessor returns a string with parameter values resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0200.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0201"
dictUsecase['DESCRIPTION']       = "JSON file with composite string on left hand side of colon: parameters and hard coded string parts"
dictUsecase['EXPECTATION']       = "JsonPreprocessor creates a parameter with parameter values resolved as string"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "GOODCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0201.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = None
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0250"
dictUsecase['DESCRIPTION']       = "JSON file with composite string on right hand side of colon: parameters and hard coded string parts; quotes around expression are missing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0250.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting value:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0251"
dictUsecase['DESCRIPTION']       = "JSON file with composite string on left hand side of colon: parameters and hard coded string parts; quotes around expression are missing"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "PARAMETER_SUBSTITUTION"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0251.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting value:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------

# >> OUTLOOK:
# NESTED_REFERENCES
# NESTED_IMPORTS (incl. file not existing)
# CYCLIC_IMPORT
# IMPLICIT_SUBKEYS
# SPECIAL_CHARACTERS
# missing JSON file

# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0900"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (1)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0900.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting ':' delimiter:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0901"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (2)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0901.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Invalid control character"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0902"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (3)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0902.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting ',' delimiter:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0903"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (4): file is completely empty"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0903.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting value:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']            = "JPP_0904"
dictUsecase['DESCRIPTION']       = "JSON file with syntax error (5): file is empty (multiple pairs of brackets only)"
dictUsecase['EXPECTATION']       = "No values are returned, and JsonPreprocessor throws an exception"
dictUsecase['SECTION']           = "SYNTAX_VIOLATIONS"
dictUsecase['SUBSECTION']        = "BADCASE"
dictUsecase['HINT']              = None
dictUsecase['COMMENT']           = None
dictUsecase['JSONFILE']          = r".\testfiles\jpp-test_config_0904.jsonp"
dictUsecase['EXPECTEDEXCEPTION'] = "Expecting property name enclosed in double quotes:"
dictUsecase['EXPECTEDRETURN']    = None
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------







