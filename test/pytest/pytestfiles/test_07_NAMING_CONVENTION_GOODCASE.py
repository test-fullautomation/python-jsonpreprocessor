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
# test_07_NAMING_CONVENTION_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 25.10.2024 - 20:21:51
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NAMING_CONVENTION_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: All names are accepted (in definition and in reference)
   @pytest.mark.parametrize(
      "Description", ["JSON file with several parameter names w.r.t. the naming convention",]
   )
   def test_JPP_0400(self, Description):
      nReturn = CExecute.Execute("JPP_0400")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
