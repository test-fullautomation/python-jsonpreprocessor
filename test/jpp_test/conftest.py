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
# conftest.py
#
# Makes 'test/testconfig' (containing TestConfig.py, the single source of
# truth for all use cases - unchanged, still reused as-is) importable, and
# provides the shared CJsonPreprocessor instance fixture.
#
# --------------------------------------------------------------------------------------------------------------

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "testconfig"))

from JsonPreprocessor.CJsonPreprocessor import CJsonPreprocessor

# Reference path for normalizing the (relative, Windows-style) 'JSONFILE' paths
# defined in TestConfig.py - same reference as component_test.py used to apply
# (the position of TestConfig.py itself, i.e. test/testconfig).
TESTCONFIGPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testconfig"))

# Reference path for the few use cases marked 'USERAWPATH': True (raw/non-
# normalized path, e.g. JPP_1200). In the former component_test.py these were
# resolved relative to the current working directory, which happened to work
# only because component_test.py was always launched with cwd='test/' (every
# .bat launcher cd's there first). That made the test's pass/fail silently
# depend on the caller's cwd. Resolving explicitly against 'test/' instead
# keeps the same original intent ("relative to where component_test.py used
# to live") without depending on the invocation cwd.
TESTBASEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="session")
def jpp():
    """
The object under test, created once and shared across all use cases (default
behavior of the former component_test.py: also serves as a stress test, since
every use case reuses the very same CJsonPreprocessor instance).
    """
    return CJsonPreprocessor()
