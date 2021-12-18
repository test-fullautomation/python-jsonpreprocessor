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
*** Settings ***
Variables     ../../testdata/templates.py
Library    ../../resources/atest_libs.py    WITH NAME    testlibs

*** Test Cases ***
Test Override Param 01
    [Documentation]    The parameters are overrided in the same configuration file
    testlibs.load_json    ../../testdata/config/06_override_params/project_config_01.json
    log   ${CONFIG}
    Should Be Equal   ${CONFIG}[params][global][dSUT][audio][volume][bSupported]   ${PARAMOVERRIDE}[testcase_01a]
    Should Be Equal   ${CONFIG}[version][patchversion]   ${PARAMOVERRIDE}[testcase_01b]
    Should Be Equal   ${CONFIG}[params][global][dSUT][system][sDetails]   ${PARAMOVERRIDE}[testcase_01c]
   
Test Override Param 02
    [Documentation]    The parameters in imported json file are overrided
    testlibs.load_json    ../../testdata/config/06_override_params/project_config_02.json
    log   ${CONFIG}
    Should Be Equal   ${CONFIG}[gPreproString]   ${PARAMOVERRIDE}[testcase_02a]
    Should Be Equal   ${CONFIG}[gPreproStructure][test01]   ${PARAMOVERRIDE}[testcase_02b]
    Should Be Equal   ${CONFIG}[gPreproFloatParam]   ${PARAMOVERRIDE}[testcase_02c]
    
Test Override Param 03
    [Documentation]    The parameters in imported json file are overrided in other imported file,
    ...    overrided json object, added new json object, ...
    testlibs.load_json    ../../testdata/config/06_override_params/project_config_03.json
    log   ${CONFIG}
    Should Be Equal   ${CONFIG}[params][global][dSUT][audio][volume][bSupported]    ${PARAMOVERRIDE}[testcase_03a]
    Should Be Equal   ${CONFIG}[params][global][dSUT][abc]    ${PARAMOVERRIDE}[testcase_03b]
    Should Be Equal   ${CONFIG}[params][global][dSUT][tuner][fm][frequency][bSupported]     ${PARAMOVERRIDE}[testcase_03c]
    Should Be Equal   ${CONFIG}[params][global][newStruct]     ${PARAMOVERRIDE}[testcase_03d]
    Should Be Equal   ${CONFIG}[params][global][TestLogfileName]    ${PARAMOVERRIDE}[testcase_03e]
    Should Be Equal   ${CONFIG}[params][global][dSUT][system][hardware]     ${PARAMOVERRIDE}[testcase_03f]
    Should Be Equal   ${CONFIG}[params][global][Testparms][Testglobal]     ${PARAMOVERRIDE}[testcase_03g]