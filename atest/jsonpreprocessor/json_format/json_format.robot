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
Test Json Config Format 01
    [Documentation]    Test with json config file has standard format without commnent
    testlibs.load_json    ../../testdata/config/07_json_format/json_format_01.json
    Log    ${CONFIG}
    Should Be Equal   ${CONFIG}    ${JSONFORMAT}
    
Test Json Config Format 02
    [Documentation]    Test with the standard json config file has commnents
    testlibs.load_json    ../../testdata/config/07_json_format/json_format_02.json
    Log    ${CONFIG}
    Should Be Equal   ${CONFIG}    ${JSONFORMAT}
    
Test Json Config Format 03
    [Documentation]    Test with the json config file has commnents.
    ...    The elements and values contain // 
    testlibs.load_json    ../../testdata/config/07_json_format/json_format_03.json
    Log    ${CONFIG}
    Should Be Equal   ${CONFIG}    ${JSONFORMAT}
    
Test Json Config Format 04
    [Documentation]    Test with the json config file has commnents.
    ...    The elements and values contain //
    ...    Some unusual new lines in json config file 
    testlibs.load_json    ../../testdata/config/07_json_format/json_format_04.json
    Log    ${CONFIG}
    Should Be Equal   ${CONFIG}    ${JSONFORMAT}
    
Test Json Config Format 05
    [Documentation]    Test with the json config file has only 1 line with //
    testlibs.load_json    ../../testdata/config/07_json_format/json_format_05.json
    Log    ${CONFIG}
    Should Be Equal   ${CONFIG}    ${JSONFORMAT}