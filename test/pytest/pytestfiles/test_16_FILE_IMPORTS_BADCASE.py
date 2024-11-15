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
# test_16_FILE_IMPORTS_BADCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 14.11.2024 - 15:38:04
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_FILE_IMPORTS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (JSON file imports itself, fix path)",]
   )
   def test_JPP_1150(self, Description):
      nReturn = CExecute.Execute("JPP_1150")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (JSON file imports another file, that is already imported, fix path)",]
   )
   def test_JPP_1151(self, Description):
      nReturn = CExecute.Execute("JPP_1151")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing parameter within dynamic import path",]
   )
   def test_JPP_1154(self, Description):
      nReturn = CExecute.Execute("JPP_1154")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with not existing import file",]
   )
   def test_JPP_1155(self, Description):
      nReturn = CExecute.Execute("JPP_1155")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with error in [import] key (1)",]
   )
   def test_JPP_1158(self, Description):
      nReturn = CExecute.Execute("JPP_1158")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with error in [import] key (2)",]
   )
   def test_JPP_1159(self, Description):
      nReturn = CExecute.Execute("JPP_1159")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with error in imported file",]
   )
   def test_JPP_1160(self, Description):
      nReturn = CExecute.Execute("JPP_1160")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
