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
# test_usecases.py
#
# Single, data-driven pytest module replacing the former two-layer setup:
#
#   1. test/component_test.py            (standalone test runner, executed
#                                          once per use case via subprocess)
#   2. test/component_test_codedump.bat   (generated 30 static pytest files
#                                          under test/pytest/pytestfiles/,
#                                          each of which just called back
#                                          into component_test.py again via
#                                          CExecute/subprocess)
#
# Both layers are obsolete now: every use case defined in
# 'test/testconfig/TestConfig.py' (listofdictUsecases - left untouched, still
# the single source of truth for all ~280 use cases) is executed directly,
# in-process, as its own parametrized pytest test. No code generation, no
# subprocess indirection.
#
# --------------------------------------------------------------------------------------------------------------

import pytest

from PythonExtensionsCollection.String.CString import CString

from TestConfig import listofdictUsecases

from .comparators import analyze_returned_values, analyze_exceptions
from .conftest import TESTBASEPATH, TESTCONFIGPATH


def _make_test_id(dictUsecase: dict) -> str:
    return f"{dictUsecase['TESTID']}-{dictUsecase['SECTION']}-{dictUsecase['SUBSECTION']}"


@pytest.mark.parametrize(
    "dictUsecase",
    listofdictUsecases,
    ids=[_make_test_id(dictUsecase) for dictUsecase in listofdictUsecases],
)
def test_jsonpreprocessor_usecase(jpp, dictUsecase):
    """
Executes a single use case from TestConfig.py: loads 'JSONFILE' via the shared
CJsonPreprocessor instance ('jpp' fixture) and checks the returned values /
raised exception against 'EXPECTEDRETURN' / 'EXPECTEDEXCEPTION'.
    """
    JSONFILE          = dictUsecase["JSONFILE"]
    EXPECTEDEXCEPTION = dictUsecase["EXPECTEDEXCEPTION"]
    EXPECTEDRETURN    = dictUsecase["EXPECTEDRETURN"]
    USERAWPATH        = dictUsecase.get("USERAWPATH", False)

    if USERAWPATH is not True:
        # Default: 'JSONFILE' is normalized relative to the position of
        # TestConfig.py (TESTCONFIGPATH) - same convention as before.
        JSONFILE = CString.NormalizePath(JSONFILE, sReferencePathAbs=TESTCONFIGPATH)
    else:
        # USERAWPATH cases (e.g. JPP_1200) use a path relative to 'test/'
        # (see TESTBASEPATH doc in conftest.py) instead of the process cwd.
        JSONFILE = CString.NormalizePath(JSONFILE, sReferencePathAbs=TESTBASEPATH)

    if EXPECTEDEXCEPTION is None and EXPECTEDRETURN is None:
        pytest.skip("Expected values are not defined for this use case (UNKNOWN in the former component_test.py).")

    dictReturned = None
    sException = None
    try:
        dictReturned = jpp.jsonLoad(JSONFILE)
    except Exception as reason:
        sException = f"'{reason}'"

    listErrors = []
    listErrors.extend(analyze_returned_values(EXPECTEDRETURN, dictReturned))
    listErrors.extend(analyze_exceptions(EXPECTEDEXCEPTION, sException))

    assert not listErrors, (
        f"[DESCRIPTION]: {dictUsecase['DESCRIPTION']}\n"
        f"[EXPECTATION]: {dictUsecase['EXPECTATION']}\n\n" + "\n".join(listErrors)
    )
