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
# test_20_SELF_ASSIGNMENTS_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 17.04.2024 - 17:34:52
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_SELF_ASSIGNMENTS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns expected value
   @pytest.mark.parametrize(
      "Description", ["JSON file with self assignments of strings, lists and dictionaries",]
   )
   def test_JPP_1800(self, Description):
      nReturn = CExecute.Execute("JPP_1800")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
