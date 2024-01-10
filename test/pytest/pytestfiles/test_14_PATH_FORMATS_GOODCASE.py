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
# test_14_PATH_FORMATS_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 09.01.2024 - 11:50:58
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PATH_FORMATS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor resolves the relative path and returns values from JSON file
   @pytest.mark.parametrize(
      "Description", ["Relative path to JSON file",]
   )
   def test_JPP_1200(self, Description):
      nReturn = CExecute.Execute("JPP_1200")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
