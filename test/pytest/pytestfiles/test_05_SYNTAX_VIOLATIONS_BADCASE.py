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
# test_05_SYNTAX_VIOLATIONS_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 04.07.2023 - 16:17:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_SYNTAX_VIOLATIONS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (1)",]
   )
   def test_JPP_0900(self, Description):
      nReturn = CExecute.Execute("JPP_0900")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (2)",]
   )
   def test_JPP_0901(self, Description):
      nReturn = CExecute.Execute("JPP_0901")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (3)",]
   )
   def test_JPP_0902(self, Description):
      nReturn = CExecute.Execute("JPP_0902")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (4): file is completely empty",]
   )
   def test_JPP_0903(self, Description):
      nReturn = CExecute.Execute("JPP_0903")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with syntax error (5): file is empty (multiple pairs of brackets only)",]
   )
   def test_JPP_0904(self, Description):
      nReturn = CExecute.Execute("JPP_0904")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
