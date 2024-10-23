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
# test_22_PARAMETER_SCOPE_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 23.10.2024 - 19:41:03
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_SCOPE_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested dictionary, in which a parameter is overwritten (1)",]
   )
   def test_JPP_2000(self, Description):
      nReturn = CExecute.Execute("JPP_2000")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested dictionary, in which a parameter is overwritten (2)",]
   )
   def test_JPP_2001(self, Description):
      nReturn = CExecute.Execute("JPP_2001")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested dictionary, in which a parameter is overwritten (3)",]
   )
   def test_JPP_2002(self, Description):
      nReturn = CExecute.Execute("JPP_2002")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested dictionary, in which a parameter is overwritten (4)",]
   )
   def test_JPP_2003(self, Description):
      nReturn = CExecute.Execute("JPP_2003")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with nested dictionary, in which a parameter is overwritten (8)",]
   )
   def test_JPP_2007(self, Description):
      nReturn = CExecute.Execute("JPP_2007")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
