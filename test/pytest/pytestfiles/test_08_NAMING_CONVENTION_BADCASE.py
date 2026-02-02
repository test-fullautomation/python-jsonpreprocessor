# **************************************************************************************************************
#  Copyright 2020-2026 Robert Bosch GmbH
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
# test_08_NAMING_CONVENTION_BADCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 02.02.2026 - 10:50:05
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NAMING_CONVENTION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with several invalid parameter names (10)",]
   )
   def test_JPP_0459(self, Description):
      nReturn = CExecute.Execute("JPP_0459")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with several invalid parameter names (11)",]
   )
   def test_JPP_0460(self, Description):
      nReturn = CExecute.Execute("JPP_0460")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with several invalid parameter names (12)",]
   )
   def test_JPP_0461(self, Description):
      nReturn = CExecute.Execute("JPP_0461")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with several invalid parameter names (13)",]
   )
   def test_JPP_0462(self, Description):
      nReturn = CExecute.Execute("JPP_0462")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with several invalid parameter names (14)",]
   )
   def test_JPP_0463(self, Description):
      nReturn = CExecute.Execute("JPP_0463")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with several invalid parameter names (15)",]
   )
   def test_JPP_0464(self, Description):
      nReturn = CExecute.Execute("JPP_0464")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
