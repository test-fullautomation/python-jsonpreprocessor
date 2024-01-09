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
# test_12_IMPLICIT_CREATION_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 09.01.2024 - 11:50:58
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_IMPLICIT_CREATION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (1)",]
   )
   def test_JPP_1050(self, Description):
      nReturn = CExecute.Execute("JPP_1050")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (2)",]
   )
   def test_JPP_1051(self, Description):
      nReturn = CExecute.Execute("JPP_1051")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (3)",]
   )
   def test_JPP_1052(self, Description):
      nReturn = CExecute.Execute("JPP_1052")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (4)",]
   )
   def test_JPP_1053(self, Description):
      nReturn = CExecute.Execute("JPP_1053")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (5)",]
   )
   def test_JPP_1054(self, Description):
      nReturn = CExecute.Execute("JPP_1054")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (5)",]
   )
   def test_JPP_1055(self, Description):
      nReturn = CExecute.Execute("JPP_1055")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (6)",]
   )
   def test_JPP_1056(self, Description):
      nReturn = CExecute.Execute("JPP_1056")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with implicit creation of data structures based on parameters (7)",]
   )
   def test_JPP_1057(self, Description):
      nReturn = CExecute.Execute("JPP_1057")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
