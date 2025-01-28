# **************************************************************************************************************
#
#  Copyright 2020-2025 Robert Bosch GmbH
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
#
# **************************************************************************************************************
#
# osd6_issue_test.py
#
# XC-HWP/ESW3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
VERSION      = "0.1.0"
VERSION_DATE = "28.01.2025"
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, time, platform
import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Utils.CUtils import *

from robot import get_version

# --------------------------------------------------------------------------------------------------------------
# !!! the module under test !!!
from JsonPreprocessor.CJsonPreprocessor import CJsonPreprocessor
# --------------------------------------------------------------------------------------------------------------

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN
COLBB = col.Style.BRIGHT + col.Fore.BLUE

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg, prefix=None):
   if prefix is None:
      sError = COLBR + f"Error: {sMsg}!\n\n"
   else:
      sError = COLBR + f"{prefix}:\n{sMsg}!\n\n"
   sys.stderr.write(sError)

# --------------------------------------------------------------------------------------------------------------
# [EXECUTION]
# --------------------------------------------------------------------------------------------------------------
#TM***

print("Executing osd6_issue_test")
print()

# !!! the object under test !!!
oJsonPreprocessor = CJsonPreprocessor()

json_strdata = """
{
    "C"  : 1,
    "params" : [
                  2,
                  {"A" : 3,
                   "B" : [
                            {
                               "C" : 4,
                               ${params.1.B.0.C} : 10,
                               "D" : 5,
                               ${params}[1]['B'][0]['D'] : 11
                            },
                            6
                         ]
                  },
                  7
               ]
}
"""

parsed_data_jpp = oJsonPreprocessor.jsonLoads(json_strdata)
PrettyPrintD(parsed_data_jpp)

print()
print("===== Environment")
print()

sOSName         = os.name
sPlatformSystem = platform.system()
sPython         = sys.executable
sPythonVersion  = sys.version

print(f" OS....: {sOSName} / {sPlatformSystem}")
print(f" Python: {sPythonVersion} / '{sPython}'")
print()

ROBOTFRAMEWORKVERSION = get_version()
print(f" RF: {ROBOTFRAMEWORKVERSION}")
print()

print("===== Installed packages")
print()

listofTuplesPackages, bSuccess, sResult = CUtils.GetInstalledPackages()

for tuplePackages in listofTuplesPackages:
    print(f"{tuplePackages}")

sys.exit(0)

