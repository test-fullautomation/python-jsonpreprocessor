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
# test_09_CODE_COMMENTS_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.10.2023 - 17:37:45
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_CODE_COMMENTS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: JsonPreprocessor returns remaining content of JSON file (valid parameters)
   @pytest.mark.parametrize(
      "Description", ["JSON file with several combinations of code comments",]
   )
   def test_JPP_0600(self, Description):
      nReturn = CExecute.Execute("JPP_0600")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
