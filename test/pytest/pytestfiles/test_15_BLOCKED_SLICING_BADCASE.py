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
# test_15_BLOCKED_SLICING_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 25.03.2024 - 11:42:32
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_BLOCKED_SLICING_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (-1)",]
   )
   def test_JPP_1350(self, Description):
      nReturn = CExecute.Execute("JPP_1350")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (-1)",]
   )
   def test_JPP_1351(self, Description):
      nReturn = CExecute.Execute("JPP_1351")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (-1)",]
   )
   def test_JPP_1352(self, Description):
      nReturn = CExecute.Execute("JPP_1352")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (:)",]
   )
   def test_JPP_1353(self, Description):
      nReturn = CExecute.Execute("JPP_1353")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (:)",]
   )
   def test_JPP_1354(self, Description):
      nReturn = CExecute.Execute("JPP_1354")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (:)",]
   )
   def test_JPP_1355(self, Description):
      nReturn = CExecute.Execute("JPP_1355")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (1:-1)",]
   )
   def test_JPP_1356(self, Description):
      nReturn = CExecute.Execute("JPP_1356")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (1:-1)",]
   )
   def test_JPP_1357(self, Description):
      nReturn = CExecute.Execute("JPP_1357")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (1:-1)",]
   )
   def test_JPP_1358(self, Description):
      nReturn = CExecute.Execute("JPP_1358")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (${index}-1:${index}+1)",]
   )
   def test_JPP_1359(self, Description):
      nReturn = CExecute.Execute("JPP_1359")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (${index}-1:${index}+1)",]
   )
   def test_JPP_1360(self, Description):
      nReturn = CExecute.Execute("JPP_1360")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (${index}-1:${index}+1)",]
   )
   def test_JPP_1361(self, Description):
      nReturn = CExecute.Execute("JPP_1361")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (0:${negindex})",]
   )
   def test_JPP_1362(self, Description):
      nReturn = CExecute.Execute("JPP_1362")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (left hand side of colon)",]
   )
   def test_JPP_1363(self, Description):
      nReturn = CExecute.Execute("JPP_1363")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (left hand side of colon)",]
   )
   def test_JPP_1364(self, Description):
      nReturn = CExecute.Execute("JPP_1364")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with blocked slicing notation (combinations with negative integer parameter)",]
   )
   def test_JPP_1365(self, Description):
      nReturn = CExecute.Execute("JPP_1365")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
