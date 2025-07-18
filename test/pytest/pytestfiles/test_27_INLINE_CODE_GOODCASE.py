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
# test_27_INLINE_CODE_GOODCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 18.07.2025 - 16:02:56
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_INLINE_CODE_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected values
   @pytest.mark.parametrize(
      "Description", ["JSON file containing Python inline code",]
   )
   def test_JPP_2100(self, Description):
      nReturn = CExecute.Execute("JPP_2100")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
