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
# test_08_COMPOSITE_EXPRESSIONS_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023 - 13:24:42
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_COMPOSITE_EXPRESSIONS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite data structure (nested lists and dictionaries 1)",]
   )
   def test_JPP_0500(self, Description):
      nReturn = CExecute.Execute("JPP_0500")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite data structure (nested lists and dictionaries 2)",]
   )
   def test_JPP_0501(self, Description):
      nReturn = CExecute.Execute("JPP_0501")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite data structure (nested lists and dictionaries 3 / some key names with dots inside)",]
   )
   def test_JPP_0502(self, Description):
      nReturn = CExecute.Execute("JPP_0502")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite data structure (some lists)",]
   )
   def test_JPP_0503(self, Description):
      nReturn = CExecute.Execute("JPP_0503")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite data structure (some dictionaries)",]
   )
   def test_JPP_0504(self, Description):
      nReturn = CExecute.Execute("JPP_0504")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
