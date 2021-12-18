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
Test Sub Data Structure 01
   [Documentation]   Updated 1 parameter without nested variable
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_01
   Log    ${CONFIG}
   testlibs.load_json     ../../testdata/config/05_sub_datastructure/json_update_01.json
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.preprocessor.definitions.preproFloatParam}    ${SUBDATASTRUCTURE}[testcase_01]
   
Test Sub Data Structure 02
   [Documentation]   Updated more than 1 parameter without nested variable
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_01
   Log    ${CONFIG}
   testlibs.load_json     ../../testdata/config/05_sub_datastructure/json_update_02.json
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.params.glo.globalString}    ${SUBDATASTRUCTURE}[testcase_02a]
   Should Be Equal    ${CONFIG.preprocessor.definitions.preproStructure.variable_01}    ${SUBDATASTRUCTURE}[testcase_02b]
   Should Be Equal    ${CONFIG.Project}     ${SUBDATASTRUCTURE}[testcase_02c]
   
Test Sub Data Structure 03
   [Documentation]   Updated 1 parameter with nested variable in element name
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_01
   Log    ${CONFIG}
   testlibs.load_json     ../../testdata/config/05_sub_datastructure/json_update_03.json
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.preprocessor.definitions.preproStructure.general}    ${SUBDATASTRUCTURE}[testcase_03]
   
Test Sub Data Structure 04
   [Documentation]   Updated 1 parameter with nested variable in element value
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_01
   Log    ${CONFIG}
   testlibs.load_json     ../../testdata/config/05_sub_datastructure/json_update_04.json
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.params.glo.globalString}   ${SUBDATASTRUCTURE}[testcase_04]
   
Test Sub Data Structure 05
   [Documentation]   Updated 1 parameter with nested variable in both element name and value
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_01
   Log    ${CONFIG}
   testlibs.load_json     ../../testdata/config/05_sub_datastructure/json_update_05.json
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.preprocessor.definitions.preproTest.checkParam}   ${SUBDATASTRUCTURE}[testcase_05]
   
Test Sub Data Structure 06
   [Documentation]   Updated more than 1 parameter with nested variable
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_01
   Log    ${CONFIG}
   testlibs.load_json     ../../testdata/config/05_sub_datastructure/json_update_06.json
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.sWelcome}    ${SUBDATASTRUCTURE}[testcase_06a]
   Should Be Equal    ${CONFIG.params.glo}    ${SUBDATASTRUCTURE}[testcase_06b]
   Should Be Equal    ${CONFIG.params.Test01}    ${SUBDATASTRUCTURE}[testcase_06c]
   Should Be Equal    ${CONFIG.preprocessor.definitions}    ${SUBDATASTRUCTURE}[testcase_06d]
   
Test Sub Data Structure 07
   [Documentation]   The value is list contained dictionary element
   testlibs.load_json    ../../testdata/config/testsuites_config.json   ${2}    sub_datastructure_02
   Log    ${CONFIG}
   Should Be Equal    ${CONFIG.arrayTest01[2].test1}    ${SUBDATASTRUCTURE}[testcase_07a]
   Should Be Equal    ${CONFIG.preprocessor.definitions.preproStructure.arrayTest02[1].check1}    ${SUBDATASTRUCTURE}[testcase_07b]