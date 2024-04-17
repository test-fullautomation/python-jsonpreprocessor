# **************************************************************************************************************
#
#  Copyright 2020-2024 Robert Bosch GmbH
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
# component_test.py
#
# XC-HWP/ESW3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
VERSION      = "0.43.0"
VERSION_DATE = "17.04.2024"
#
# --------------------------------------------------------------------------------------------------------------
#TM***
# TOC:
# [ANALYZERETURNEDVALUES]
# [ANALYZEEXCEPTIONS]
# [TESTCONFIG]
# [CODEDUMP]
# [ADDITIONALSTEPS]
# [EXECUTION]
# --------------------------------------------------------------------------------------------------------------

import os, sys, shlex, subprocess, ctypes, time
import colorama as col
import pprint

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Utils.CUtils import *

from libs.CConfig import CConfig
from libs.CCodePatterns import CCodePatterns
from libs.CGenCode import CGenCode

from testconfig.TestConfig import *

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
# [ANALYZERETURNEDVALUES]

def AnalyzeReturnedValues(EXPECTEDRETURN=None, dictReturned=None):

   sMethod = "AnalyzeReturnedValues"

   listErrors = []

   if ( (EXPECTEDRETURN is None) and (dictReturned is None) ):
      # returned == expected => check passed (in case of len(listErrors) == 0)
      pass
   elif ( (EXPECTEDRETURN is not None) and (dictReturned is None) ):
      sResult  = "JsonPreprocessor returned None, but values are expected"
      listErrors.append(sResult)
   elif ( (EXPECTEDRETURN is None) and (dictReturned is not None) ):
      sResult  = "JsonPreprocessor returned values, but values are not expected"
      listErrors.append(sResult)
   else:
      # both EXPECTEDRETURN and dictReturned are not None => content needs to be compared

      listSplitLines = EXPECTEDRETURN.splitlines()
      listExpectedLines = []
      for sLine in listSplitLines:
         if sLine != "":
            listExpectedLines.append(sLine)
      # PrettyPrint(listExpectedLines)

      listReturnedLines = PrettyPrint(dictReturned, bToConsole=False)

      # check number of lines
      nNrOfLinesReturned = len(listReturnedLines)
      nNrOfLinesExpected = len(listExpectedLines)
      if nNrOfLinesReturned != nNrOfLinesExpected:
         bSuccess = False
         sResult  = f"JsonPreprocessor value counter mismatch! Expected: {nNrOfLinesExpected} values, but returned: {nNrOfLinesReturned} values"
         listErrors.append(sResult)
         print("JsonPreprocessor returned:")
         print()
         PrettyPrint(dictReturned, bToConsole=True)
         print()
         return listErrors, bSuccess, sResult

      # compare content line by line
      bDeviation = False
      for nIndex, sLineReturned in enumerate(listReturnedLines):
         sLineExpected = listExpectedLines[nIndex]
         if sLineReturned != sLineExpected:
            bDeviation = True
            sResult    = f"Found deviating return values\n(1) '{sLineExpected}'   > (expected)\n(2) '{sLineReturned}'   > (returned)"
            listErrors.append(sResult)
         # eof if sLineReturned != sLineExpected:
      # eof for nIndex, sLineReturned in enumerate(listReturnedLines):
   # eof else - elif - if ( (EXPECTEDRETURN is None) and (dictReturned is None) ):

   if len(listErrors) == 0:
      bSuccess = True
      if EXPECTEDRETURN is None:
         sResult  = "No values returned from JsonPreprocessor (like expected)."
      else:
         sResult  = "JsonPreprocessor returned expected values."
   else:
      bSuccess = False
      sResult  = "JsonPreprocessor did not return expected values."

   return listErrors, bSuccess, sResult

# eof def AnalyzeReturnedValues(EXPECTEDRETURN=None, dictReturned=None):

# --------------------------------------------------------------------------------------------------------------
# [ANALYZEEXCEPTIONS]

def AnalyzeExceptions(EXPECTEDEXCEPTION=None, sException=None):

   sMethod = "AnalyzeExceptions"

   listErrors = []

   if ( (EXPECTEDEXCEPTION is None) and (sException is None) ):
      # returned == expected => check passed (in case of len(listErrors) == 0)
      pass
   elif ( (EXPECTEDEXCEPTION is not None) and (sException is None) ):
      sResult  = "JsonPreprocessor threw no exception, but an exception is expected"
      listErrors.append(sResult)
   elif ( (EXPECTEDEXCEPTION is None) and (sException is not None) ):
      sResult  = "JsonPreprocessor threw an exception, but an exception is not expected"
      listErrors.append(sResult)
   else:
      # both EXPECTEDEXCEPTION and sException are not None => content needs to be compared
      if EXPECTEDEXCEPTION not in sException:
         # we search for relevant parts only (a full match is not required)
         bSuccess = False
         sResult  = f"JsonPreprocessor exception mismatch! Expected exception:\n'{EXPECTEDEXCEPTION}',\nbut thrown:\n'{sException}'"
         listErrors.append(sResult)
   # eof else - elif - if ( (EXPECTEDEXCEPTION is None) and (sException is None) ):

   if len(listErrors) == 0:
      bSuccess = True
      if EXPECTEDEXCEPTION is None:
         sResult  = "No exception thrown from JsonPreprocessor (like expected)."
      else:
         sResult  = "JsonPreprocessor threw expected exception."
   else:
      bSuccess = False
      sResult  = "JsonPreprocessor did not throw expected exception."

   return listErrors, bSuccess, sResult

# eof def AnalyzeExceptions(EXPECTEDEXCEPTION=None, sException=None):


# --------------------------------------------------------------------------------------------------------------
# [TESTCONFIG]

# -- initialize and dump test configuration

oConfig = None
try:
   oConfig = CConfig(os.path.abspath(__file__))
except Exception as ex:
   print()
   printerror(CString.FormatResult("(main)", None, str(ex)))
   print()
   sys.exit(ERROR)

# update version and date of this app
oConfig.Set("VERSION", VERSION)
oConfig.Set("VERSION_DATE", VERSION_DATE)
THISSCRIPTNAME = oConfig.Get('THISSCRIPTNAME')
THISSCRIPTFULLNAME = f"{THISSCRIPTNAME} v. {VERSION} / {VERSION_DATE}"
oConfig.Set("THISSCRIPTFULLNAME", THISSCRIPTFULLNAME)

# add information about system under test
try:
   # not yet implemented officially
   oJsonPreprocessor = CJsonPreprocessor()
   sut_version = oJsonPreprocessor.getVersion()
   sut_version_date = oJsonPreprocessor.getVersionDate()
   del oJsonPreprocessor
   SUT_FULL_NAME = f"JsonPreprocessor v. {sut_version} / {sut_version_date}"
   oConfig.Set("SUT_FULL_NAME", SUT_FULL_NAME)
except:
   pass

# dump configuration values to screen
listConfigLines = oConfig.DumpConfig()

CONFIGDUMP = oConfig.Get('CONFIGDUMP')
if CONFIGDUMP is True:
   # if that's all, we have nothing more to do
   sys.exit(SUCCESS)


# --------------------------------------------------------------------------------------------------------------
# [PRELIMINARIES]
# --------------------------------------------------------------------------------------------------------------
#TM***

# -- access to configuration

THISSCRIPT         = oConfig.Get('THISSCRIPT')
THISSCRIPTNAME     = oConfig.Get('THISSCRIPTNAME')
TESTCONFIGPATH     = oConfig.Get('TESTCONFIGPATH')
OSNAME             = oConfig.Get('OSNAME')
PLATFORMSYSTEM     = oConfig.Get('PLATFORMSYSTEM')
PYTHON             = oConfig.Get('PYTHON')
PYTHONVERSION      = oConfig.Get('PYTHONVERSION')
TESTLOGFILESFOLDER = oConfig.Get('TESTLOGFILESFOLDER')
SELFTESTLOGFILE    = oConfig.Get('SELFTESTLOGFILE')
TESTID             = oConfig.Get('TESTID')
RECREATEINSTANCE   = oConfig.Get('RECREATEINSTANCE')

# -- start logging
oSelfTestLogFile = CFile(SELFTESTLOGFILE)
NOW = time.strftime('%d.%m.%Y - %H:%M:%S')
oSelfTestLogFile.Write(f"{THISSCRIPTNAME} started at: {NOW}\n")
oSelfTestLogFile.Write(listConfigLines) # from DumpConfig() called above
oSelfTestLogFile.Write()

# -- prepare TESTIDs

# ('listofdictUsecases' is imported directly from test/testconfig/TestConfig.py)

TESTID = oConfig.Get('TESTID')

if TESTID is not None:
   listTESTIDs = TESTID.split(';')
   listofdictUsecasesSubset = []
   for sTESTID in listTESTIDs:
      sTESTID = sTESTID.strip()
      for dictUsecase in listofdictUsecases:
         if sTESTID == dictUsecase['TESTID']:
            listofdictUsecasesSubset.append(dictUsecase)
   # eof for sTESTID in listTESTIDs:
   if len(listofdictUsecasesSubset) == 0:
      bSuccess = False
      sResult  = f"Test ID '{TESTID}' not defined"
      sResult  = CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)
      print()
      printerror(sResult)
      print()
      printerror(sResult)
      oSelfTestLogFile.Write(sResult, 1)
      del oSelfTestLogFile
      sys.exit(ERROR)
   del listofdictUsecases
   listofdictUsecases = listofdictUsecasesSubset
# eof if TESTID is not None:

# --------------------------------------------------------------------------------------------------------------

# -- check for duplicate test IDs
# Test IDs are used to identify and select test cases. They have to be unique.

listIDs = []
listDuplicates = []
for dictUsecase in listofdictUsecases:
   TESTID = dictUsecase['TESTID']
   if TESTID in listIDs:
      listDuplicates.append(TESTID)
   else:
      listIDs.append(TESTID)
# eof for dictUsecase in listofdictUsecases:
if len(listDuplicates) > 0:
   sDuplicates = "[" + ", ".join(listDuplicates) + "]"
   bSuccess = False
   sResult  = f"Duplicate test IDs found in test configuration: {sDuplicates}\nTest IDs are used to identify and select test cases. They have to be unique"
   sResult  = CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)
   print()
   printerror(sResult)
   print()
   oSelfTestLogFile.Write(sResult, 1)
   del oSelfTestLogFile
   sys.exit(ERROR)


# --------------------------------------------------------------------------------------------------------------
# [CODEDUMP]
# special function (with premature end of execution = no test execution)
# --------------------------------------------------------------------------------------------------------------
#TM***

CODEDUMP = oConfig.Get('CODEDUMP')
if CODEDUMP is True:
   oCodeGenerator = None
   try:
      oCodeGenerator = CGenCode(oConfig)
   except Exception as ex:
      bSuccess = None
      sResult  = str(ex)
      sResult  = CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)
      print()
      printerror(sResult)
      print()
      oSelfTestLogFile.Write(sResult, 1)
      del oSelfTestLogFile
      sys.exit(ERROR)

   bSuccess, sResult = oCodeGenerator.GenCode()
   if bSuccess is not True:
      sResult = CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)
      print()
      printerror(sResult)
      print()
      oSelfTestLogFile.Write(sResult, 1)
      del oSelfTestLogFile
      sys.exit(ERROR)

   print(COLBG + f"{sResult}\n")

   # after code dump nothing more to do here
   sys.exit(SUCCESS)


# --------------------------------------------------------------------------------------------------------------
# [EXECUTION]
# --------------------------------------------------------------------------------------------------------------
#TM***

print("Executing test cases")
print()

nNrOfUsecases = len(listofdictUsecases)

# -- initialize test conter
nCntUsecases        = 0
nCntPassedUsecases  = 0
nCntFailedUsecases  = 0
nCntUnknownUsecases = 0

# --------------------------------------------------------------------------------------------------------------
# !!! the object under test !!!
oJsonPreprocessor = None
if RECREATEINSTANCE is not True:
   oJsonPreprocessor = CJsonPreprocessor()
#
# The default behavior is: The object under test is created only once for all test cases!
# Every test case uses the same JsonPreprocessor class object. This is also like a stress test,
# to see how stable the JsonPreprocessor is.
#
# An alternative way is to create a JsonPreprocessor class object for every test case separately
# (= create at the beginning, destroy at the end of a test case).
# Every test case uses an own JsonPreprocessor class object
#
# This depends on the switch RECREATEINSTANCE (command line)
#
# --------------------------------------------------------------------------------------------------------------

listTestsNotPassed = []

for dictUsecase in listofdictUsecases:

   # debug
   # PrettyPrint(dictUsecase, sPrefix="dictUsecase")
   # print()

   nCntUsecases = nCntUsecases + 1

   # get required parameters
   TESTID            = dictUsecase['TESTID']
   DESCRIPTION       = dictUsecase['DESCRIPTION']
   EXPECTATION       = dictUsecase['EXPECTATION']
   SECTION           = dictUsecase['SECTION']
   SUBSECTION        = dictUsecase['SUBSECTION']
   JSONFILE          = dictUsecase['JSONFILE']
   EXPECTEDEXCEPTION = dictUsecase['EXPECTEDEXCEPTION']
   EXPECTEDRETURN    = dictUsecase['EXPECTEDRETURN']

   # get optional parameters
   HINT = None
   if "HINT" in dictUsecase:
      HINT = dictUsecase['HINT']
   COMMENT = None
   if "COMMENT" in dictUsecase:
      COMMENT = dictUsecase['COMMENT']
   USERAWPATH = False
   if "USERAWPATH" in dictUsecase:
      USERAWPATH = dictUsecase['USERAWPATH']

   if USERAWPATH is not True:
      # Default is that the path 'JSONFILE' is normalized before the JsonPreprocessor is called.
      # The reference for relative paths is the position of the file TestConfig.py (TESTCONFIGPATH).
      # In case of USERAWPATH is True, the path 'JSONFILE' is not normalized.
      # And the path is relative to the position of the executing script (this script).
      JSONFILE = CString.NormalizePath(JSONFILE, sReferencePathAbs=TESTCONFIGPATH)

   # get derived parameters
   TESTFULLNAME    = f"{TESTID}-({SECTION})-[{SUBSECTION}]"
   TESTLOGFILE_TXT = f"{TESTLOGFILESFOLDER}/{TESTFULLNAME}.log"

   sOut = f"====== [START OF TEST] : '{TESTFULLNAME}' / ({nCntUsecases}/{nNrOfUsecases})"
   print(COLBY + sOut)
   print()
   oSelfTestLogFile.Write(sOut, 1)
   sOut = f"   [JSONFILE] : '{JSONFILE}'"
   print(COLBY + sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"[DESCRIPTION] : {DESCRIPTION}"
   print(COLBY + sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"[EXPECTATION] : {EXPECTATION}"
   print(COLBY + sOut)
   oSelfTestLogFile.Write(sOut)
   if COMMENT is not None:
      sOut = f"    [COMMENT] : {COMMENT}"
      print(COLBY + sOut)
      oSelfTestLogFile.Write(sOut)
   if HINT is not None:
      sOut = f"       [HINT] : {HINT}"
      print(COLBY + sOut)
      oSelfTestLogFile.Write(sOut)
   print()
   oSelfTestLogFile.Write()

   # --------------------------------------------------------------------------------------------------------------

   # Checking the JsonPreprocessor depends on the following two return parameters: 'dictReturned' and 'sException'.
   # They have to match to what is defined in test configuration by 'EXPECTEDRETURN' and 'EXPECTEDEXCEPTION'.

   # If both 'EXPECTEDEXCEPTION' and 'EXPECTEDRETURN' are None, the check of values returned from JsonPreprocessor
   # is skipped and the test case result is UNKNOWN.

   # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
   # -- test case execution
   if RECREATEINSTANCE is True:
      # !!! the object under test !!!
      oJsonPreprocessor = CJsonPreprocessor()
   dictReturned = None
   sException   = None
   try:
      dictReturned = oJsonPreprocessor.jsonLoad(JSONFILE)
   except Exception as reason:
      sException = f"'{reason}'"
      printerror(sException, "JsonPreprocessor threw exception")
      oSelfTestLogFile.Write("JsonPreprocessor threw exception:", 1)
      oSelfTestLogFile.Write(sException)
      oSelfTestLogFile.Write()
   if RECREATEINSTANCE is True:
      # !!! the object under test !!!
      del oJsonPreprocessor
   # //////////////////////////////////////////////////////////////////////////////////////////////////////////////

   listReturnedLines = PrettyPrint(dictReturned, bToConsole=False)
   oSelfTestLogFile.Write("JsonPreprocessor returned:", 1)
   oSelfTestLogFile.Write(listReturnedLines)

   # additional debug:
   # print("JsonPreprocessor returned:")
   # pprint.pprint(dictReturned)
   # PrettyPrint(dictReturned, bToConsole=True)

   if ( (EXPECTEDEXCEPTION is None) and (EXPECTEDRETURN is None) ):
      nCntUnknownUsecases = nCntUnknownUsecases + 1
      sOut = f"    Test '{TESTFULLNAME}' UNKNOWN (because expected values are not defined)"
      print(COLBB + sOut)
      print()
      oSelfTestLogFile.Write()
      oSelfTestLogFile.Write(sOut)
      oSelfTestLogFile.Write()
      listTestsNotPassed.append(TESTFULLNAME)
      print("JsonPreprocessor returned:")
      print()
      PrettyPrint(dictReturned, bToConsole=True)
      print()
      continue # for dictUsecase in listofdictUsecases:

   listErrors = []

   listErrorsReturnedValues, bSuccess, sResult = AnalyzeReturnedValues(EXPECTEDRETURN, dictReturned)
   listErrors.extend(listErrorsReturnedValues)
   if bSuccess is True:
      # intermediate result
      print(sResult)
      print()
      oSelfTestLogFile.Write()
      oSelfTestLogFile.Write(sResult)
      oSelfTestLogFile.Write()

   listErrorsExceptions, bSuccess, sResult = AnalyzeExceptions(EXPECTEDEXCEPTION, sException)
   listErrors.extend(listErrorsExceptions)
   if bSuccess is True:
      # intermediate result
      print(sResult)
      print()
      oSelfTestLogFile.Write(sResult)
      oSelfTestLogFile.Write()

   # -- final result
   if len(listErrors) == 0:
      nCntPassedUsecases = nCntPassedUsecases + 1
      sOut = f"    Test '{TESTFULLNAME}' PASSED"
      print(COLBG + sOut)
      print()
      oSelfTestLogFile.Write(sOut)
      oSelfTestLogFile.Write()
   else:
      nCntFailedUsecases = nCntFailedUsecases + 1
      sErrors = "\n".join(listErrors)
      printerror(sErrors)
      oSelfTestLogFile.Write(sErrors, 1)
      printerror(f"Test '{TESTFULLNAME}' FAILED\n\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}")
      oSelfTestLogFile.Write("\n" + f"    Test '{TESTFULLNAME}' FAILED", 1)
      listTestsNotPassed.append(TESTFULLNAME)

# eof for dictUsecase in listofdictUsecases:

try:
   # !!! the object under test !!!
   del oJsonPreprocessor
except:
   pass

# --------------------------------------------------------------------------------------------------------------

# paranoia check
if ( (nCntPassedUsecases + nCntFailedUsecases + nCntUnknownUsecases != nCntUsecases) or (nNrOfUsecases != nCntUsecases) ):
   print()
   sOut = CString.FormatResult(THISSCRIPTNAME, bSuccess=None, sResult="Internal counter mismatch")
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"Defined  : {nNrOfUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"Executed : {nCntUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"PASSED   : {nCntPassedUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"FAILED   : {nCntFailedUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"UNKNOWN  : {nCntUnknownUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   print()
   del oSelfTestLogFile
   sys.exit(ERROR)

# --------------------------------------------------------------------------------------------------------------

# -- component test result (over all test cases)

if len(listTestsNotPassed) > 0:
   # print()
   sOut = "Tests that are not PASSED:"
   oSelfTestLogFile.Write(sOut + "\n")
   print(COLBY + sOut)
   print()
   for sTest in listTestsNotPassed:
      sOut = f"- {sTest}"
      oSelfTestLogFile.Write(sOut)
      print(sOut)
   oSelfTestLogFile.Write()
   print()

nReturn = ERROR

if nCntUsecases == 0:
   sOut = "Nothing executed - but why?" # should not happen
   oSelfTestLogFile.Write(sOut, 1)
   printerror(fsOut)
   nReturn = ERROR
elif ( (nCntFailedUsecases == 0) and (nCntUnknownUsecases == 0) ):
   sOut = f"Component test PASSED"
   oSelfTestLogFile.Write(sOut, 1)
   print(COLBG + sOut)
   print()
   nReturn = SUCCESS
else:
   sOut = f"Component test FAILED"
   oSelfTestLogFile.Write(sOut, 1)
   printerror(sOut)
   nReturn = ERROR

sOut = f"Defined : {nNrOfUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)
sOut = f"PASSED  : {nCntPassedUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)
sOut = f"FAILED  : {nCntFailedUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)
sOut = f"UNKNOWN : {nCntUnknownUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)

print()

del oSelfTestLogFile

sys.exit(nReturn)

# --------------------------------------------------------------------------------------------------------------

