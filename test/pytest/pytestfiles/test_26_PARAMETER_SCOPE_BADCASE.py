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
# test_26_PARAMETER_SCOPE_BADCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 10.04.2025 - 17:21:06
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_SCOPE_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (1)",]
   )
   def test_JPP_2050(self, Description):
      nReturn = CExecute.Execute("JPP_2050")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (2)",]
   )
   def test_JPP_2051(self, Description):
      nReturn = CExecute.Execute("JPP_2051")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (3)",]
   )
   def test_JPP_2052(self, Description):
      nReturn = CExecute.Execute("JPP_2052")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (4)",]
   )
   def test_JPP_2053(self, Description):
      nReturn = CExecute.Execute("JPP_2053")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (5)",]
   )
   def test_JPP_2054(self, Description):
      nReturn = CExecute.Execute("JPP_2054")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (6)",]
   )
   def test_JPP_2055(self, Description):
      nReturn = CExecute.Execute("JPP_2055")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (7)",]
   )
   def test_JPP_2056(self, Description):
      nReturn = CExecute.Execute("JPP_2056")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (8)",]
   )
   def test_JPP_2057(self, Description):
      nReturn = CExecute.Execute("JPP_2057")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing a parameter with missing scope (9)",]
   )
   def test_JPP_2058(self, Description):
      nReturn = CExecute.Execute("JPP_2058")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
