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
# test_23_PARAMETER_SCOPE_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 23.10.2024 - 19:41:03
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_SCOPE_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (1)",]
   )
   def test_JPP_2500(self, Description):
      nReturn = CExecute.Execute("JPP_2500")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (2)",]
   )
   def test_JPP_2501(self, Description):
      nReturn = CExecute.Execute("JPP_2501")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (3)",]
   )
   def test_JPP_2502(self, Description):
      nReturn = CExecute.Execute("JPP_2502")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (4)",]
   )
   def test_JPP_2503(self, Description):
      nReturn = CExecute.Execute("JPP_2503")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (5)",]
   )
   def test_JPP_2504(self, Description):
      nReturn = CExecute.Execute("JPP_2504")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (7)",]
   )
   def test_JPP_2506(self, Description):
      nReturn = CExecute.Execute("JPP_2506")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (8)",]
   )
   def test_JPP_2507(self, Description):
      nReturn = CExecute.Execute("JPP_2507")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (9)",]
   )
   def test_JPP_2508(self, Description):
      nReturn = CExecute.Execute("JPP_2508")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
