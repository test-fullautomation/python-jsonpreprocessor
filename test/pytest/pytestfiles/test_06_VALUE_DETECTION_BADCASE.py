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
# test_06_VALUE_DETECTION_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023 - 15:09:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VALUE_DETECTION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax 1)",]
   )
   def test_JPP_0350(self, Description):
      nReturn = CExecute.Execute("JPP_0350")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax 2)",]
   )
   def test_JPP_0351(self, Description):
      nReturn = CExecute.Execute("JPP_0351")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax 3)",]
   )
   def test_JPP_0352(self, Description):
      nReturn = CExecute.Execute("JPP_0352")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 1)",]
   )
   def test_JPP_0353(self, Description):
      nReturn = CExecute.Execute("JPP_0353")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 2)",]
   )
   def test_JPP_0354(self, Description):
      nReturn = CExecute.Execute("JPP_0354")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 3)",]
   )
   def test_JPP_0355(self, Description):
      nReturn = CExecute.Execute("JPP_0355")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 4)",]
   )
   def test_JPP_0356(self, Description):
      nReturn = CExecute.Execute("JPP_0356")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 5)",]
   )
   def test_JPP_0357(self, Description):
      nReturn = CExecute.Execute("JPP_0357")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 6)",]
   )
   def test_JPP_0358(self, Description):
      nReturn = CExecute.Execute("JPP_0358")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 6)",]
   )
   def test_JPP_0359(self, Description):
      nReturn = CExecute.Execute("JPP_0359")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax 9)",]
   )
   def test_JPP_0360(self, Description):
      nReturn = CExecute.Execute("JPP_0360")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 1)",]
   )
   def test_JPP_0361(self, Description):
      nReturn = CExecute.Execute("JPP_0361")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 2)",]
   )
   def test_JPP_0362(self, Description):
      nReturn = CExecute.Execute("JPP_0362")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 3)",]
   )
   def test_JPP_0363(self, Description):
      nReturn = CExecute.Execute("JPP_0363")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 4)",]
   )
   def test_JPP_0364(self, Description):
      nReturn = CExecute.Execute("JPP_0364")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 5)",]
   )
   def test_JPP_0365(self, Description):
      nReturn = CExecute.Execute("JPP_0365")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 6)",]
   )
   def test_JPP_0366(self, Description):
      nReturn = CExecute.Execute("JPP_0366")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 1)",]
   )
   def test_JPP_0367(self, Description):
      nReturn = CExecute.Execute("JPP_0367")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 2)",]
   )
   def test_JPP_0368(self, Description):
      nReturn = CExecute.Execute("JPP_0368")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 3)",]
   )
   def test_JPP_0369(self, Description):
      nReturn = CExecute.Execute("JPP_0369")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 4)",]
   )
   def test_JPP_0370(self, Description):
      nReturn = CExecute.Execute("JPP_0370")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression starting with '${' and ending with '}', further matching '${' and '}' in between (not all nested) (invalid syntax 5)",]
   )
   def test_JPP_0371(self, Description):
      nReturn = CExecute.Execute("JPP_0371")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
