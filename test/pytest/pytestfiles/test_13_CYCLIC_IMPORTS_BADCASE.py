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
# test_13_CYCLIC_IMPORTS_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 09.01.2024 - 11:50:58
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_CYCLIC_IMPORTS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (JSON file imports itself)",]
   )
   def test_JPP_1150(self, Description):
      nReturn = CExecute.Execute("JPP_1150")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with cyclic imports (JSON file imports another file, that is already imported)",]
   )
   def test_JPP_1151(self, Description):
      nReturn = CExecute.Execute("JPP_1151")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
