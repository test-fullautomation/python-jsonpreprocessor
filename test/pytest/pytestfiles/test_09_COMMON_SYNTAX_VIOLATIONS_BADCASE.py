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
# test_09_COMMON_SYNTAX_VIOLATIONS_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 09.08.2023 - 17:28:15
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_COMMON_SYNTAX_VIOLATIONS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (1)",]
   )
   def test_JPP_0950(self, Description):
      nReturn = CExecute.Execute("JPP_0950")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (2)",]
   )
   def test_JPP_0951(self, Description):
      nReturn = CExecute.Execute("JPP_0951")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (3)",]
   )
   def test_JPP_0952(self, Description):
      nReturn = CExecute.Execute("JPP_0952")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (4): file is completely empty",]
   )
   def test_JPP_0953(self, Description):
      nReturn = CExecute.Execute("JPP_0953")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (5): file is empty (multiple pairs of brackets only)",]
   )
   def test_JPP_0954(self, Description):
      nReturn = CExecute.Execute("JPP_0954")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
