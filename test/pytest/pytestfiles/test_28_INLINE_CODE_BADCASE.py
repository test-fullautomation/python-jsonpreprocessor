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
# test_28_INLINE_CODE_BADCASE.py
#
# XC-HWP/ESW3-Queckenstedt
#
# 11.08.2025 - 16:48:21
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_INLINE_CODE_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a string (1)",]
   )
   def test_JPP_2150(self, Description):
      nReturn = CExecute.Execute("JPP_2150")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a string (2)",]
   )
   def test_JPP_2151(self, Description):
      nReturn = CExecute.Execute("JPP_2151")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a string (3)",]
   )
   def test_JPP_2152(self, Description):
      nReturn = CExecute.Execute("JPP_2152")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code with additional leading angle bracket",]
   )
   def test_JPP_2180(self, Description):
      nReturn = CExecute.Execute("JPP_2180")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a dictionary with additional leading angle bracket",]
   )
   def test_JPP_2184(self, Description):
      nReturn = CExecute.Execute("JPP_2184")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code is parameter name",]
   )
   def test_JPP_2192(self, Description):
      nReturn = CExecute.Execute("JPP_2192")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code is parameter name inside a list",]
   )
   def test_JPP_2193(self, Description):
      nReturn = CExecute.Execute("JPP_2193")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code is parameter name inside a dictionary",]
   )
   def test_JPP_2194(self, Description):
      nReturn = CExecute.Execute("JPP_2194")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
