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
# test_06_VALUE_DETECTION_BADDCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 14.07.2023 - 19:07:06
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VALUE_DETECTION_BADDCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with parameter of type 'list' / index (in square brackets) defined inside the curly brackets (invalid syntax)",]
   )
   def test_JPP_0350(self, Description):
      nReturn = CExecute.Execute("JPP_0350")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more opening elements '${' than closing elements '}' (invalid syntax)",]
   )
   def test_JPP_0351(self, Description):
      nReturn = CExecute.Execute("JPP_0351")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax)",]
   )
   def test_JPP_0352(self, Description):
      nReturn = CExecute.Execute("JPP_0352")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
