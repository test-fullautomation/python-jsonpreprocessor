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
# test_04_PARAMETER_SUBSTITUTION_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 12.07.2023 - 19:43:13
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_SUBSTITUTION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / string parameter substitution in parameter value / innermost parameter not existing",]
   )
   def test_JPP_0250(self, Description):
      nReturn = CExecute.Execute("JPP_0250")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / string parameter substitution in parameter name / in between parameter not existing",]
   )
   def test_JPP_0251(self, Description):
      nReturn = CExecute.Execute("JPP_0251")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter name / standard notation / index parameter not existing",]
   )
   def test_JPP_0252(self, Description):
      nReturn = CExecute.Execute("JPP_0252")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter name / dotdict notation / index parameter not existing",]
   )
   def test_JPP_0253(self, Description):
      nReturn = CExecute.Execute("JPP_0253")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter value / standard notation / index parameter not existing",]
   )
   def test_JPP_0254(self, Description):
      nReturn = CExecute.Execute("JPP_0254")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter value / dotdict notation / index parameter not existing",]
   )
   def test_JPP_0255(self, Description):
      nReturn = CExecute.Execute("JPP_0255")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter name / standard notation / variant number not existing",]
   )
   def test_JPP_0256(self, Description):
      nReturn = CExecute.Execute("JPP_0256")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter name / dotdict notation / milestone number not existing",]
   )
   def test_JPP_0257(self, Description):
      nReturn = CExecute.Execute("JPP_0257")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter value / standard notation / variant number not existing",]
   )
   def test_JPP_0258(self, Description):
      nReturn = CExecute.Execute("JPP_0258")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter value / dotdict notation / milestone number not existing",]
   )
   def test_JPP_0259(self, Description):
      nReturn = CExecute.Execute("JPP_0259")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------