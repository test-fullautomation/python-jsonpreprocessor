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
# test_16_FILE_IMPORTS_BADCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 30.10.2026 - 12:27:16
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
      "Description", ["JSON file with cyclic imports (JSON file imports itself, dynamic path)",]
   )
   def test_JPP_1152(self, Description):
      nReturn = CExecute.Execute("JPP_1152")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (JSON file imports another file, that is already imported, dynamic path)",]
   )
   def test_JPP_1153(self, Description):
      nReturn = CExecute.Execute("JPP_1153")
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
      "Description", ["JSON file with syntax error in import path (1)",]
   )
   def test_JPP_1156(self, Description):
      nReturn = CExecute.Execute("JPP_1156")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error in import path (2)",]
   )
   def test_JPP_1157(self, Description):
      nReturn = CExecute.Execute("JPP_1157")
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
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with invalid data type of [import] key (1)",]
   )
   def test_JPP_1161(self, Description):
      nReturn = CExecute.Execute("JPP_1161")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with invalid data type of [import] key (2)",]
   )
   def test_JPP_1162(self, Description):
      nReturn = CExecute.Execute("JPP_1162")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with invalid data type of [import] key (3)",]
   )
   def test_JPP_1163(self, Description):
      nReturn = CExecute.Execute("JPP_1163")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with invalid data type of [import] key (4)",]
   )
   def test_JPP_1164(self, Description):
      nReturn = CExecute.Execute("JPP_1164")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (sawtooth, stopped)",]
   )
   def test_JPP_1165(self, Description):
      nReturn = CExecute.Execute("JPP_1165")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (sawtooth, endless)",]
   )
   def test_JPP_1166(self, Description):
      nReturn = CExecute.Execute("JPP_1166")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object containing an invalid key",]
   )
   def test_JPP_1167(self, Description):
      nReturn = CExecute.Execute("JPP_1167")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object without key 'file'",]
   )
   def test_JPP_1168(self, Description):
      nReturn = CExecute.Execute("JPP_1168")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object with key 'else' but without key 'if'",]
   )
   def test_JPP_1169(self, Description):
      nReturn = CExecute.Execute("JPP_1169")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object with invalid data type of key 'if' (1)",]
   )
   def test_JPP_1170(self, Description):
      nReturn = CExecute.Execute("JPP_1170")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object with invalid data type of key 'if' (2)",]
   )
   def test_JPP_1171(self, Description):
      nReturn = CExecute.Execute("JPP_1171")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object with condition referring to a not existing parameter",]
   )
   def test_JPP_1172(self, Description):
      nReturn = CExecute.Execute("JPP_1172")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object with key 'optional' not being a literal boolean value",]
   )
   def test_JPP_1173(self, Description):
      nReturn = CExecute.Execute("JPP_1173")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import?] key and [import] object as value",]
   )
   def test_JPP_1174(self, Description):
      nReturn = CExecute.Execute("JPP_1174")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object with invalid data type of key 'file'",]
   )
   def test_JPP_1175(self, Description):
      nReturn = CExecute.Execute("JPP_1175")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with conditional import (condition true, file not existing, not optional)",]
   )
   def test_JPP_1176(self, Description):
      nReturn = CExecute.Execute("JPP_1176")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with [import] object containing a duplicate key",]
   )
   def test_JPP_1177(self, Description):
      nReturn = CExecute.Execute("JPP_1177")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with invalid data type of [import?] key",]
   )
   def test_JPP_1178(self, Description):
      nReturn = CExecute.Execute("JPP_1178")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with optional import of a file containing a not optional import of a not existing file",]
   )
   def test_JPP_1179(self, Description):
      nReturn = CExecute.Execute("JPP_1179")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
