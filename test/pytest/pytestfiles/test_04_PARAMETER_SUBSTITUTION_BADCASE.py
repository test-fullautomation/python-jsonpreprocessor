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
# test_04_PARAMETER_SUBSTITUTION_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 04.07.2023 - 16:17:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_SUBSTITUTION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite string on right hand side of colon: parameters and hard coded string parts; quotes around expression are missing",]
   )
   def test_JPP_0250(self, Description):
      nReturn = CExecute.Execute("JPP_0250")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with composite string on left hand side of colon: parameters and hard coded string parts; quotes around expression are missing",]
   )
   def test_JPP_0251(self, Description):
      nReturn = CExecute.Execute("JPP_0251")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
