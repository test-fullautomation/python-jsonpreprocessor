# **************************************************************************************************************
#
#  Copyright 2020-2026 Robert Bosch GmbH
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
# comparators.py
#
# Comparison helpers used by test_usecases.py to check the values/exceptions
# returned by CJsonPreprocessor against the expectations defined per use case
# in test/testconfig/TestConfig.py.
#
# This is a 1:1 port of the comparison logic that used to live in
# test/component_test.py (AnalyzeReturnedValues / AnalyzeExceptions), with
# the printing/logfile side effects removed (pytest already captures stdout
# and provides its own, much richer failure reporting) - only the actual
# comparison semantics are preserved.
#
# --------------------------------------------------------------------------------------------------------------

from PythonExtensionsCollection.Utils.CUtils import PrettyPrint


def analyze_returned_values(EXPECTEDRETURN, dictReturned):
    """
Compares the dict returned by CJsonPreprocessor.jsonLoad() against the expected
pretty-printed representation defined in TestConfig.py's 'EXPECTEDRETURN'.

Returns a list of human readable error strings (empty list == match / success).
    """
    listErrors = []

    if EXPECTEDRETURN is None and dictReturned is None:
        return listErrors
    if EXPECTEDRETURN is not None and dictReturned is None:
        listErrors.append("JsonPreprocessor returned None, but values are expected")
        return listErrors
    if EXPECTEDRETURN is None and dictReturned is not None:
        listErrors.append("JsonPreprocessor returned values, but values are not expected")
        return listErrors

    # both EXPECTEDRETURN and dictReturned are not None => content needs to be compared
    listExpectedLines = [sLine for sLine in EXPECTEDRETURN.splitlines() if sLine != ""]
    listReturnedLines = PrettyPrint(dictReturned, bToConsole=False)

    nNrOfLinesReturned = len(listReturnedLines)
    nNrOfLinesExpected = len(listExpectedLines)
    if nNrOfLinesReturned != nNrOfLinesExpected:
        listErrors.append(
            f"JsonPreprocessor value counter mismatch! Expected: {nNrOfLinesExpected} values, "
            f"but returned: {nNrOfLinesReturned} values\n"
            f"JsonPreprocessor returned:\n" + "\n".join(listReturnedLines)
        )
        return listErrors

    for nIndex, sLineReturned in enumerate(listReturnedLines):
        sLineExpected = listExpectedLines[nIndex]
        if sLineReturned != sLineExpected:
            listErrors.append(
                f"Found deviating return values\n(1) '{sLineExpected}'   > (expected)\n"
                f"(2) '{sLineReturned}'   > (returned)"
            )

    return listErrors


def analyze_exceptions(EXPECTEDEXCEPTION, sException):
    """
Compares the exception message raised by CJsonPreprocessor.jsonLoad() (if any)
against the expected (partial) message defined in TestConfig.py's 'EXPECTEDEXCEPTION'.

Returns a list of human readable error strings (empty list == match / success).
    """
    listErrors = []

    if EXPECTEDEXCEPTION is None and sException is None:
        return listErrors
    if EXPECTEDEXCEPTION is not None and sException is None:
        listErrors.append("JsonPreprocessor threw no exception, but an exception is expected")
        return listErrors
    if EXPECTEDEXCEPTION is None and sException is not None:
        listErrors.append("JsonPreprocessor threw an exception, but an exception is not expected")
        return listErrors

    # both EXPECTEDEXCEPTION and sException are not None => content needs to be compared
    # (we search for relevant parts only, a full match is not required)
    if EXPECTEDEXCEPTION not in sException:
        listErrors.append(
            f"JsonPreprocessor exception mismatch! Expected exception:\n'{EXPECTEDEXCEPTION}',\n"
            f"but thrown:\n'{sException}'"
        )

    return listErrors
