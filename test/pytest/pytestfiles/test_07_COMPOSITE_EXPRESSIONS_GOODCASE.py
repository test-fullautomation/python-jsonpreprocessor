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
# test_07_COMPOSITE_EXPRESSIONS_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 28.09.2023 - 11:51:44
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
      "Description", ["JSON file with composite strings containing several times a colon and a comma (JSON syntax elements)",]
   )
   def test_JPP_0505(self, Description):
      nReturn = CExecute.Execute("JPP_0505")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite strings containing several combinations of curly brackets and special characters before",]
   )
   def test_JPP_0506(self, Description):
      nReturn = CExecute.Execute("JPP_0506")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
