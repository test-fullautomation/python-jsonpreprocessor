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
# test_17_NOT_EXISTING_PARAMETERS_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 26.03.2024 - 14:29:20
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NOT_EXISTING_PARAMETERS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (1)",]
   )
   def test_JPP_1650(self, Description):
      nReturn = CExecute.Execute("JPP_1650")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (2)",]
   )
   def test_JPP_1651(self, Description):
      nReturn = CExecute.Execute("JPP_1651")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (3)",]
   )
   def test_JPP_1652(self, Description):
      nReturn = CExecute.Execute("JPP_1652")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (4)",]
   )
   def test_JPP_1653(self, Description):
      nReturn = CExecute.Execute("JPP_1653")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (6)",]
   )
   def test_JPP_1655(self, Description):
      nReturn = CExecute.Execute("JPP_1655")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (8)",]
   )
   def test_JPP_1657(self, Description):
      nReturn = CExecute.Execute("JPP_1657")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (9)",]
   )
   def test_JPP_1658(self, Description):
      nReturn = CExecute.Execute("JPP_1658")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (10)",]
   )
   def test_JPP_1659(self, Description):
      nReturn = CExecute.Execute("JPP_1659")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (11)",]
   )
   def test_JPP_1660(self, Description):
      nReturn = CExecute.Execute("JPP_1660")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameters at several positions (12)",]
   )
   def test_JPP_1661(self, Description):
      nReturn = CExecute.Execute("JPP_1661")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
