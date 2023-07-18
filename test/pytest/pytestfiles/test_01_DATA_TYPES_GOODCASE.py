# **************************************************************************************************************
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
# --------------------------------------------------------------------------------------------------------------
#
# test_01_DATA_TYPES_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023 - 15:09:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_DATA_TYPES_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: All values are returned untouched, with their correct data types
   @pytest.mark.parametrize(
      "Description", ["JSON file with parameters of different data types (basic and composite)",]
   )
   def test_JPP_0001(self, Description):
      nReturn = CExecute.Execute("JPP_0001")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: All parameters referenced by dollar operator are resolved correctly, with their correct data types
   @pytest.mark.parametrize(
      "Description", ["JSON file containing parameters with dollar operator syntax at right hand side of colon, basic data types",]
   )
   def test_JPP_0002(self, Description):
      nReturn = CExecute.Execute("JPP_0002")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: All parameters referenced by dollar operator are resolved correctly, with their correct data types
   @pytest.mark.parametrize(
      "Description", ["JSON file containing parameters with dollar operator syntax at right hand side of colon, composite data type: list",]
   )
   def test_JPP_0003(self, Description):
      nReturn = CExecute.Execute("JPP_0003")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: All parameters referenced by dollar operator are resolved correctly, with their correct data types
   @pytest.mark.parametrize(
      "Description", ["JSON file containing parameters with dollar operator syntax at right hand side of colon, composite data type: dict",]
   )
   def test_JPP_0004(self, Description):
      nReturn = CExecute.Execute("JPP_0004")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: All parameters referenced by dollar operator are resolved correctly, outcome is a string containing the values of all referenced parameters
   @pytest.mark.parametrize(
      "Description", ["JSON file with string values containing dollar operators",]
   )
   def test_JPP_0005(self, Description):
      nReturn = CExecute.Execute("JPP_0005")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
