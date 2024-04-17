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
# test_11_IMPLICIT_CREATION_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 17.04.2024 - 20:03:38
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_IMPLICIT_CREATION_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file with dictionary keys to be created implicitly",]
   )
   def test_JPP_1000(self, Description):
      nReturn = CExecute.Execute("JPP_1000")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file with dictionary keys to be created implicitly (same key names at all levels)",]
   )
   def test_JPP_1001(self, Description):
      nReturn = CExecute.Execute("JPP_1001")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file with combinations of implicit and explicit creation / with and without initialization",]
   )
   def test_JPP_1002(self, Description):
      nReturn = CExecute.Execute("JPP_1002")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file with combinations of implicit and explicit creation / access to implicitly created keys by parameters / dict assignment by reference",]
   )
   def test_JPP_1003(self, Description):
      nReturn = CExecute.Execute("JPP_1003")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file with combinations of ascending and descending dotdict syntax",]
   )
   def test_JPP_1004(self, Description):
      nReturn = CExecute.Execute("JPP_1004")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
