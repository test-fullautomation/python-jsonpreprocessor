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
# test_08_COMPOSITE_EXPRESSIONS_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 13.09.2023 - 10:58:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_COMPOSITE_EXPRESSIONS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite data structure (nested lists and dictionaries / some key names with dots inside)",]
   )
   def test_JPP_0550(self, Description):
      nReturn = CExecute.Execute("JPP_0550")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
