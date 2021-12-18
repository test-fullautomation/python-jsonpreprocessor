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
Variables     ../../../testdata/templates.py
Library    ../../../resources/atest_libs.py    WITH NAME    testlibs

*** Test Cases ***
Test Nested Import One File 01
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_01
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT01}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT01}
   
Test Nested Import One File 02
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_02
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT02}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT02}
   
Test Nested Import One File 03
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_03
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT03}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT03}
   
Test Nested Import One File 04
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_04
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT04}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT04}
   
Test Nested Import Files 05
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_05
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT05}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT05}
   
Test Nested Import Files 06
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_06
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT06}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT06}
   
Test Nested Import Files 07
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_07
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT07}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT07}
   
Test Nested Import Files 08
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_08
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT08}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT08}
   
Test Nested Import Files 09
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    nested_09
   Log    ${JSONDATA}
   Log    ${NESTEDIMPORT09}
   Should Be Equal    ${JSONDATA}    ${NESTEDIMPORT09}