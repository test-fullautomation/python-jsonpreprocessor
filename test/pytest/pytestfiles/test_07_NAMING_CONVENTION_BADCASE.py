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
# test_07_NAMING_CONVENTION_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023 - 15:09:36
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NAMING_CONVENTION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (1)",]
   )
   def test_JPP_0450(self, Description):
      nReturn = CExecute.Execute("JPP_0450")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (2)",]
   )
   def test_JPP_0451(self, Description):
      nReturn = CExecute.Execute("JPP_0451")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (3)",]
   )
   def test_JPP_0452(self, Description):
      nReturn = CExecute.Execute("JPP_0452")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (4)",]
   )
   def test_JPP_0453(self, Description):
      nReturn = CExecute.Execute("JPP_0453")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (5)",]
   )
   def test_JPP_0454(self, Description):
      nReturn = CExecute.Execute("JPP_0454")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (6)",]
   )
   def test_JPP_0455(self, Description):
      nReturn = CExecute.Execute("JPP_0455")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (7)",]
   )
   def test_JPP_0456(self, Description):
      nReturn = CExecute.Execute("JPP_0456")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with Python keywords used as parameter names (8)",]
   )
   def test_JPP_0457(self, Description):
      nReturn = CExecute.Execute("JPP_0457")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: No values are returned, and JsonPreprocessor throws an exception
   @pytest.mark.parametrize(
      "Description", ["JSON file with parameter name containing not allowed special characters",]
   )
   def test_JPP_0458(self, Description):
      nReturn = CExecute.Execute("JPP_0458")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
