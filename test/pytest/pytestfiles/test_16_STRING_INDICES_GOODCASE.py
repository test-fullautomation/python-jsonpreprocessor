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
# test_16_STRING_INDICES_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 25.03.2024 - 13:09:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_STRING_INDICES_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with indices applied to a string (inside lists and inside dictionaries)",]
   )
   def test_JPP_1500(self, Description):
      nReturn = CExecute.Execute("JPP_1500")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
