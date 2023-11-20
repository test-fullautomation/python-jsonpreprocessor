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
# 13.09.2023
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

      # -- configuration: common environment

      THISSCRIPT = CString.NormalizePath(sCalledBy)
      self.__dictConfig['THISSCRIPT']     = THISSCRIPT
      self.__dictConfig['THISSCRIPTNAME'] = os.path.basename(THISSCRIPT)
      REFERENCEPATH = os.path.dirname(THISSCRIPT) # position of main() script is reference for all relative paths
      self.__dictConfig['REFERENCEPATH']  = REFERENCEPATH
      self.__dictConfig['TESTCONFIGPATH'] = f"{REFERENCEPATH}/testconfig" # reference for all relative paths inside TestConfig.py
      self.__dictConfig['OSNAME']         = os.name
      self.__dictConfig['PLATFORMSYSTEM'] = platform.system()
      PYTHON = CString.NormalizePath(sys.executable)
      self.__dictConfig['PYTHON']         = PYTHON
      self.__dictConfig['PYTHONPATH']     = os.path.dirname(PYTHON)
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

      CODEDUMP = False
      if oCmdLineArgs.codedump != None:
         CODEDUMP = oCmdLineArgs.codedump
      self.__dictConfig['CODEDUMP'] = CODEDUMP
      # if True: script quits after config dump

      CONFIGDUMP = False
      if oCmdLineArgs.configdump != None:
         CONFIGDUMP = oCmdLineArgs.configdump
      self.__dictConfig['CONFIGDUMP'] = CONFIGDUMP
      # if True: script quits after config dump

      RECREATEINSTANCE = False
      if oCmdLineArgs.recreateinstance != None:
         RECREATEINSTANCE = oCmdLineArgs.recreateinstance
      self.__dictConfig['RECREATEINSTANCE'] = RECREATEINSTANCE

      # -- log file and output folders
      sLogFileName = "JPP_SelfTest.log"
      if TESTID is not None:
         if ';' not in TESTID:
            # in case of a single TESTID is given in command line, we add this ID to the log file name
            # (support of pytest, where every test case is executed separately)
            sLogFileName = f"JPP_SelfTest_{TESTID}.log"

      SELFTESTLOGFILE = f"{REFERENCEPATH}/testlogfiles/{sLogFileName}"

      if oCmdLineArgs.logfile != None:
         # command line overwrites default log file location
         SELFTESTLOGFILE = CString.NormalizePath(oCmdLineArgs.logfile, sReferencePathAbs=REFERENCEPATH)

      TESTLOGFILESFOLDER = os.path.dirname(SELFTESTLOGFILE)
      # update default values in config
      self.__dictConfig['SELFTESTLOGFILE']    = SELFTESTLOGFILE
      self.__dictConfig['TESTLOGFILESFOLDER'] = TESTLOGFILESFOLDER

      # -- create output folder
      oFolder = CFolder(TESTLOGFILESFOLDER)
      bSuccess, sResult = oFolder.Create(bOverwrite=False, bRecursive=True)
      del oFolder
      if bSuccess is not True:
         raise Exception(CString.FormatResult(sMethod, bSuccess, sResult))

      # dump of basic configuration parameters to console
      # self.DumpConfig() # done in main script now!

   # eof def __init__(self, sCalledBy=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def DumpConfig(self):
      """Prints all configuration values to console."""
      listFormattedOutputLines = []
      # -- printing configuration to console
      print()
      # PrettyPrint(self.__dictConfig, sPrefix="Config")
      for key, value in self.__dictConfig.items():
         sLine = key.rjust(30, ' ') + " : " + str(value)
         print(sLine)
         listFormattedOutputLines.append(sLine)
      print()
      return listFormattedOutputLines
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

   def Set(self, sName=None, sValue=None):
      """Sets a new configuration parameter."""
      sName  = f"{sName}"
      sValue = f"{sValue}"
      self.__dictConfig[sName] = sValue
   # eof def Set(self, sName=None, sValue=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

# eof class CConfig():

# **************************************************************************************************************


