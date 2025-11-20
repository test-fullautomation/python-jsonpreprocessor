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
# 20.11.2025 - 13:52:43
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
      "Description", ["Python inline code as embedded part of a string within a list",]
   )
   def test_JPP_2153(self, Description):
      nReturn = CExecute.Execute("JPP_2153")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a string within a dictionary",]
   )
   def test_JPP_2154(self, Description):
      nReturn = CExecute.Execute("JPP_2154")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a key name (1)",]
   )
   def test_JPP_2155(self, Description):
      nReturn = CExecute.Execute("JPP_2155")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a key name (2)",]
   )
   def test_JPP_2156(self, Description):
      nReturn = CExecute.Execute("JPP_2156")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as embedded part of a key name (3)",]
   )
   def test_JPP_2157(self, Description):
      nReturn = CExecute.Execute("JPP_2157")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code without quotes at left hand side of the colon (1)",]
   )
   def test_JPP_2158(self, Description):
      nReturn = CExecute.Execute("JPP_2158")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code without quotes at left hand side of the colon (2)",]
   )
   def test_JPP_2159(self, Description):
      nReturn = CExecute.Execute("JPP_2159")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code within quotes at left hand side of the colon (1)",]
   )
   def test_JPP_2160(self, Description):
      nReturn = CExecute.Execute("JPP_2160")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code within quotes at left hand side of the colon (2)",]
   )
   def test_JPP_2161(self, Description):
      nReturn = CExecute.Execute("JPP_2161")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Completely invalid Python inline code at left hand side of the colon (1)",]
   )
   def test_JPP_2162(self, Description):
      nReturn = CExecute.Execute("JPP_2162")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Completely invalid Python inline code at left hand side of the colon (2)",]
   )
   def test_JPP_2163(self, Description):
      nReturn = CExecute.Execute("JPP_2163")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as key name at left hand side of the colon (1)",]
   )
   def test_JPP_2164(self, Description):
      nReturn = CExecute.Execute("JPP_2164")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as key name at left hand side of the colon (2)",]
   )
   def test_JPP_2165(self, Description):
      nReturn = CExecute.Execute("JPP_2165")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as list index at left hand side of the colon",]
   )
   def test_JPP_2166(self, Description):
      nReturn = CExecute.Execute("JPP_2166")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code as dictionary key at left hand side of the colon",]
   )
   def test_JPP_2167(self, Description):
      nReturn = CExecute.Execute("JPP_2167")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code with missing leading angle bracket",]
   )
   def test_JPP_2168(self, Description):
      nReturn = CExecute.Execute("JPP_2168")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code with missing trailing angle bracket",]
   )
   def test_JPP_2169(self, Description):
      nReturn = CExecute.Execute("JPP_2169")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a list with missing leading angle bracket",]
   )
   def test_JPP_2170(self, Description):
      nReturn = CExecute.Execute("JPP_2170")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a list with missing trailing angle bracket",]
   )
   def test_JPP_2171(self, Description):
      nReturn = CExecute.Execute("JPP_2171")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a dictionary with missing leading angle bracket",]
   )
   def test_JPP_2172(self, Description):
      nReturn = CExecute.Execute("JPP_2172")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a dictionary with missing trailing angle bracket",]
   )
   def test_JPP_2173(self, Description):
      nReturn = CExecute.Execute("JPP_2173")
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
      "Description", ["Python inline code with additional trailing angle bracket",]
   )
   def test_JPP_2181(self, Description):
      nReturn = CExecute.Execute("JPP_2181")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a list with additional leading angle bracket",]
   )
   def test_JPP_2182(self, Description):
      nReturn = CExecute.Execute("JPP_2182")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a list with additional trailing angle bracket",]
   )
   def test_JPP_2183(self, Description):
      nReturn = CExecute.Execute("JPP_2183")
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
      "Description", ["Python inline code inside a dictionary with additional trailing angle bracket",]
   )
   def test_JPP_2185(self, Description):
      nReturn = CExecute.Execute("JPP_2185")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Python inline code inside a list returns data type not supported by JSON",]
   )
   def test_JPP_2187(self, Description):
      nReturn = CExecute.Execute("JPP_2187")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Nested Python inline code",]
   )
   def test_JPP_2189(self, Description):
      nReturn = CExecute.Execute("JPP_2189")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Nested Python inline code inside a list",]
   )
   def test_JPP_2190(self, Description):
      nReturn = CExecute.Execute("JPP_2190")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["Nested Python inline code inside a dictionary",]
   )
   def test_JPP_2191(self, Description):
      nReturn = CExecute.Execute("JPP_2191")
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
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file containing Python inline code within a list",]
   )
   def test_JPP_2195(self, Description):
      nReturn = CExecute.Execute("JPP_2195")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
