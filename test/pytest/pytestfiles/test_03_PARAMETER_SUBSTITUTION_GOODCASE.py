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
# test_03_PARAMETER_SUBSTITUTION_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023 - 15:09:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_SUBSTITUTION_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / string parameter substitution in parameter value",]
   )
   def test_JPP_0200(self, Description):
      nReturn = CExecute.Execute("JPP_0200")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / string parameter substitution in parameter name",]
   )
   def test_JPP_0201(self, Description):
      nReturn = CExecute.Execute("JPP_0201")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter name / standard notation",]
   )
   def test_JPP_0202(self, Description):
      nReturn = CExecute.Execute("JPP_0202")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter name / dotdict notation",]
   )
   def test_JPP_0203(self, Description):
      nReturn = CExecute.Execute("JPP_0203")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter value / standard notation",]
   )
   def test_JPP_0204(self, Description):
      nReturn = CExecute.Execute("JPP_0204")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / index parameter substitution in parameter value / dotdict notation",]
   )
   def test_JPP_0205(self, Description):
      nReturn = CExecute.Execute("JPP_0205")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter name / standard notation",]
   )
   def test_JPP_0206(self, Description):
      nReturn = CExecute.Execute("JPP_0206")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter name / dotdict notation",]
   )
   def test_JPP_0207(self, Description):
      nReturn = CExecute.Execute("JPP_0207")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter value / standard notation",]
   )
   def test_JPP_0208(self, Description):
      nReturn = CExecute.Execute("JPP_0208")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested parameter / key parameter substitution in parameter value / dotdict notation",]
   )
   def test_JPP_0209(self, Description):
      nReturn = CExecute.Execute("JPP_0209")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
