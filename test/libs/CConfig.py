# **************************************************************************************************************
#
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
#
# **************************************************************************************************************
#
# CConfig.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.07.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
Python module containing the configuration for **component_test.py**.
"""

# --------------------------------------------------------------------------------------------------------------

import os, sys, time, platform, json, argparse
import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.Utils.CUtils import *

col.init(autoreset=True)
COLBR = col.Style.BRIGHT + col.Fore.RED
COLBG = col.Style.BRIGHT + col.Fore.GREEN
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLNY = col.Style.NORMAL + col.Fore.YELLOW
COLBW = col.Style.BRIGHT + col.Fore.WHITE

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
   sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

class CConfig():

   def __init__(self, sCalledBy=None):
      """
      """

      sMethod = "CConfig.__init__"

      if sCalledBy is None:
         raise Exception(CString.FormatResult(sMethod, None, "sCalledBy is None"))

      # -- configuration init
      self.__dictConfig = {}

      # -- configuration: basic environment

      THISSCRIPT = CString.NormalizePath(sCalledBy)
      self.__dictConfig['THISSCRIPT']     = THISSCRIPT
      self.__dictConfig['THISSCRIPTNAME'] = os.path.basename(THISSCRIPT)
      REFERENCEPATH = os.path.dirname(THISSCRIPT) # position of main() script is reference for all relative paths
      self.__dictConfig['REFERENCEPATH']  = REFERENCEPATH
      self.__dictConfig['TESTCONFIGPATH'] = f"{REFERENCEPATH}/testconfig" # reference for all relative paths inside TestConfig.py
      OSNAME = os.name
      self.__dictConfig['OSNAME']         = OSNAME
      PLATFORMSYSTEM = platform.system()
      self.__dictConfig['PLATFORMSYSTEM'] = PLATFORMSYSTEM
      PYTHON = CString.NormalizePath(sys.executable)
      self.__dictConfig['PYTHON']         = PYTHON
      PYTHONPATH = os.path.dirname(PYTHON)
      self.__dictConfig['PYTHONPATH']     = PYTHONPATH
      self.__dictConfig['PYTHONVERSION']  = sys.version

      # -- configuration: command line

      oCmdLineParser = argparse.ArgumentParser()
      oCmdLineParser.add_argument('--testid', type=str, help='The ID of the test to be executed')
      oCmdLineParser.add_argument('--codedump', action='store_true', help='If True, creates pytest code and test lists; default: False')
      oCmdLineParser.add_argument('--configdump', action='store_true', help='If True, basic configuration values are dumped to console; default: False')
      oCmdLineParser.add_argument('--recreateinstance', action='store_true', help='If True, the JsonPreprocessor class object will be recreated in every iteration; default: False')
      oCmdLineParser.add_argument('--logfile', type=str, help='Path and name of log file (optional)')

      oCmdLineArgs = oCmdLineParser.parse_args()

      TESTID = None
      if oCmdLineArgs.testid != None:
         TESTID = str(oCmdLineArgs.testid).strip()
      self.__dictConfig['TESTID'] = TESTID

      bCodeDump = False
      if oCmdLineArgs.codedump != None:
         bCodeDump = oCmdLineArgs.codedump
      self.__dictConfig['CODEDUMP'] = bCodeDump
      # if True: script quits after config dump

      bConfigDump = False
      if oCmdLineArgs.configdump != None:
         bConfigDump = oCmdLineArgs.configdump
      self.__dictConfig['CONFIGDUMP'] = bConfigDump
      # if True: script quits after config dump

      bRecreateInstance = False
      if oCmdLineArgs.recreateinstance != None:
         bRecreateInstance = oCmdLineArgs.recreateinstance
      self.__dictConfig['RECREATEINSTANCE'] = bRecreateInstance

      # self test log file: default settings
      TESTLOGFILESFOLDER = f"{REFERENCEPATH}/testlogfiles"
      SELFTESTLOGFILE    = f"{TESTLOGFILESFOLDER}/JPP_SelfTest.log"
      if oCmdLineArgs.logfile != None:
         SELFTESTLOGFILE = oCmdLineArgs.logfile
         SELFTESTLOGFILE = CString.NormalizePath(SELFTESTLOGFILE, sReferencePathAbs=REFERENCEPATH)
         TESTLOGFILESFOLDER = os.path.dirname(SELFTESTLOGFILE)

      oFolder = CFolder(TESTLOGFILESFOLDER)
      bSuccess, sResult = oFolder.Create(bOverwrite=False, bRecursive=True)
      del oFolder
      if bSuccess is not True:
         raise Exception(CString.FormatResult(sMethod, bSuccess, sResult))
      self.__dictConfig['TESTLOGFILESFOLDER'] = TESTLOGFILESFOLDER
      self.__dictConfig['SELFTESTLOGFILE']    = SELFTESTLOGFILE

      # dump of basic configuration parameters to console
      self.DumpConfig()

   # eof def __init__(self, sCalledBy=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def DumpConfig(self):
      """Prints all configuration values to console."""
      # -- printing configuration to console
      print()
      # PrettyPrint(self.__dictConfig, sPrefix="Config")
      for key, value in self.__dictConfig.items():
         print(key.rjust(30, ' ') + " : " + str(value))
      print()
   # eof def DumpConfig(self):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def PrintConfigKeys(self):
      """Prints all configuration key names to console."""
      # -- printing configuration keys to console
      print()
      listKeys = self.__dictConfig.keys()
      sKeys = "[" + ", ".join(listKeys) + "]"
      print(sKeys)
      print()
   # eof def PrintConfigKeys(self):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def Get(self, sName=None):
      """Returns the configuration value belonging to a key name."""
      if ( (sName is None) or (sName not in self.__dictConfig) ):
         print()
         printerror(f"Configuration parameter '{sName}' not existing")
         # from here it's standard output:
         print()
         print("Use instead one of:")
         self.PrintConfigKeys()
         return None # returning 'None' in case of key is not existing !!!
      else:
         return self.__dictConfig[sName]
   # eof def Get(self, sName=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

# eof class CConfig():

# **************************************************************************************************************


