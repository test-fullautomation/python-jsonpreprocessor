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
# test_15_FILE_IMPORTS_GOODCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 14.11.2024 - 15:38:04
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_FILE_IMPORTS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (1))",]
   )
   def test_JPP_1100(self, Description):
      nReturn = CExecute.Execute("JPP_1100")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (2))",]
   )
   def test_JPP_1101(self, Description):
      nReturn = CExecute.Execute("JPP_1101")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (3))",]
   )
   def test_JPP_1102(self, Description):
      nReturn = CExecute.Execute("JPP_1102")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (4))",]
   )
   def test_JPP_1103(self, Description):
      nReturn = CExecute.Execute("JPP_1103")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (5))",]
   )
   def test_JPP_1104(self, Description):
      nReturn = CExecute.Execute("JPP_1104")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (6))",]
   )
   def test_JPP_1105(self, Description):
      nReturn = CExecute.Execute("JPP_1105")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import, recursive (7))",]
   )
   def test_JPP_1106(self, Description):
      nReturn = CExecute.Execute("JPP_1106")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import, alternate (8))",]
   )
   def test_JPP_1107(self, Description):
      nReturn = CExecute.Execute("JPP_1107")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import, parallel (9))",]
   )
   def test_JPP_1108(self, Description):
      nReturn = CExecute.Execute("JPP_1108")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on dictionary key values",]
   )
   def test_JPP_1109(self, Description):
      nReturn = CExecute.Execute("JPP_1109")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on list elemens",]
   )
   def test_JPP_1110(self, Description):
      nReturn = CExecute.Execute("JPP_1110")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns values
   @pytest.mark.parametrize(
      "Description", ["JSON file import based on parameters (dynamic import (7))",]
   )
   def test_JPP_1111(self, Description):
      nReturn = CExecute.Execute("JPP_1111")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
