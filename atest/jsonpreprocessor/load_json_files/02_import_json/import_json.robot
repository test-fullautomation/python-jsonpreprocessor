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
Test Import One File 01
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    one_file_01
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILE01}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILE01}
   
Test Import One File 02
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    one_file_02
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILE02}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILE02}
   
Test Import One File 03
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    one_file_03
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILE03}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILE03}
   
Test Import One File 04
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    one_file_04
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILE04}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILE04}
   
Test Import Files 05
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    files_01
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILES01}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILES01}
   
Test Import Files 06
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    files_02
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILES02}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILES02}
   
Test Import Files 07
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    files_03
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILES03}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILES03}
   
Test Import Files 08
   ${JSONDATA} =    testlibs.load_json    ../../../testdata/config/testsuites_config.json   ${2}    files_04
   Log    ${JSONDATA}
   Log    ${IMPORTEDFILES04}
   Should Be Equal    ${JSONDATA}    ${IMPORTEDFILES04}