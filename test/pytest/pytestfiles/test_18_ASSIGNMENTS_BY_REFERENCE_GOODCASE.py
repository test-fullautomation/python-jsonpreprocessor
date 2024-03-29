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
# test_18_ASSIGNMENTS_BY_REFERENCE_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 27.03.2024 - 11:21:23
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_ASSIGNMENTS_BY_REFERENCE_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with list assignments (by reference)",]
   )
   def test_JPP_1901(self, Description):
      nReturn = CExecute.Execute("JPP_1901")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
