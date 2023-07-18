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
# test_02_DATA_INTEGRITY_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023 - 13:24:42
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_DATA_INTEGRITY_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns empty dictionary
   @pytest.mark.parametrize(
      "Description", ["JSON file is empty (single pair of brackets only)",]
   )
   def test_JPP_0100(self, Description):
      nReturn = CExecute.Execute("JPP_0100")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: String is returned unchanged
   @pytest.mark.parametrize(
      "Description", ["JSON file with string containing several separator characters and blanks; no parameters",]
   )
   def test_JPP_0101(self, Description):
      nReturn = CExecute.Execute("JPP_0101")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: String is returned unchanged (but with masked special characters and escape sequences resolved)
   @pytest.mark.parametrize(
      "Description", ["JSON file with string containing more special characters, masked special characters and escape sequences",]
   )
   def test_JPP_0102(self, Description):
      nReturn = CExecute.Execute("JPP_0102")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
