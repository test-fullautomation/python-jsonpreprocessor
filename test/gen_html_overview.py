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
# gen_html_overview.py
#
# Standalone replacement for the HTML part of the former '--codedump' feature
# (test/libs/CGenCode.py, now deleted together with the rest of the old
# component_test.py / codedump machinery). Generates 'test/JPP_TestUsecases.html',
# a human readable overview of all use cases currently defined in
# 'test/testconfig/TestConfig.py' (the single source of truth also used by
# 'test/jpp_test/test_usecases.py').
#
# Usage:
#   python test/gen_html_overview.py
#
# --------------------------------------------------------------------------------------------------------------

import ast
import os
import sys
import time

sTestDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(sTestDir, "testconfig"))

from PythonExtensionsCollection.String.CString import CString
from TestConfig import listofdictUsecases

TESTCONFIGPATH = os.path.join(sTestDir, "testconfig")
HTMLFILE = os.path.join(sTestDir, "JPP_TestUsecases.html")
API_TESTFILE = os.path.join(sTestDir, "jpp_test", "test_api.py")

GITHUB_JSONFILE_BASE = "https://github.com/test-fullautomation/python-jsonpreprocessor/blob/develop/test/testfiles"
GITHUB_API_TESTFILE_LINK = "https://github.com/test-fullautomation/python-jsonpreprocessor/blob/develop/test/jpp_test/test_api.py"

HTML_HEAD = """<html><head>
<meta http-equiv="content-type" content="text/html; charset=windows-1252">
   <meta name="JsonPreprocessor" content="JsonPreprocessor">
   <title>JsonPreprocessor Test Overview</title>
</head>
<body vlink="#000000" text="#000000" link="#000000" bgcolor="#FFFFFF" alink="#000000">
<hr width="100%" color="#FF8C00" align="center">
<div align="center">
<font size="6" face="Arial" color="#595959">
<b>
JsonPreprocessor<br>Test Cases
</b></font>
</div>
<hr width="100%" color="#FF8C00" align="center">

<div>&nbsp;</div>

<div align="center">

<table frame="box" rules="all" valign="middle" width="1100" cellspacing="0" cellpadding="6" border="1" align="center">
<colgroup>
   <col width="4%" span="1">
   <col width="8%" span="1">
   <col width="16%" span="1">
   <col width="9%" span="1">
   <col width="63%" span="1">
</colgroup>
<tbody>
"""

HTML_ROW_PATTERN = """<td colspan="1" valign="center" bgcolor="#F5F5F5" align="right">
<font size="2" face="Arial" color="#FF0000">
<b>
####CNTUSECASES####
</b></font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#595959">
<b>
<a target="_blank" href="####JSONFILELINK####">####TESTID####</a>
</b></font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#4169E1">
####SECTION####
</font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#####TEXTCOLOR####">
####SUBSECTION####
</font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="left">
<font size="2" face="Arial" color="#595959"><i>
<b>####DESCRIPTION####</b><br>
Expected: ####EXPECTATION####
####COMMENT####
####HINT####
</i></font></td>

"""

HTML_SECTION_PATTERN = """<tr valign="middle" align="left">
<td colspan="5" valign="center" bgcolor="#FFE4B5" align="center">
<font size="3" face="Arial" color="#595959">
<b>####SECTIONTITLE####</b>
</font></td>
</tr>
"""

HTML_API_ROW_PATTERN = """<td colspan="1" valign="center" bgcolor="#F5F5F5" align="right">
<font size="2" face="Arial" color="#FF0000">
<b>
####CNTUSECASES####
</b></font></td>

<td colspan="2" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#595959">
<b>
<a target="_blank" href="####TESTFILELINK####">####TESTNAME####</a>
</b></font></td>

<td colspan="2" valign="center" bgcolor="#F5F5F5" align="left">
<font size="2" face="Arial" color="#595959"><i>
####DESCRIPTION####
</i></font></td>

"""

HTML_TAIL_PATTERN = """
</tbody></table></div>
<div>&nbsp;</div>
<hr width="100%" color="#FF8C00" align="center">
<div align="center"><font size="2" color="#27408B">####GENERATED####</font></div>
<div>&nbsp;</div>
</body></html>
"""


def _html_row(nCntUsecases: int, dictUsecase: dict) -> str:
    TESTID      = dictUsecase["TESTID"]
    DESCRIPTION = dictUsecase["DESCRIPTION"]
    EXPECTATION = dictUsecase["EXPECTATION"]
    SECTION     = dictUsecase["SECTION"]
    SUBSECTION  = dictUsecase["SUBSECTION"]
    COMMENT     = dictUsecase.get("COMMENT")
    HINT        = dictUsecase.get("HINT")

    JSONFILE     = CString.NormalizePath(dictUsecase["JSONFILE"], sReferencePathAbs=TESTCONFIGPATH)
    JSONFILEname = os.path.basename(JSONFILE)
    JSONFILElink = f"{GITHUB_JSONFILE_BASE}/{JSONFILEname}"

    TEXTCOLOR = "008000" if SUBSECTION == "GOODCASE" else "FF0000"

    sOut = HTML_ROW_PATTERN
    sOut = sOut.replace("####CNTUSECASES####", str(nCntUsecases))
    sOut = sOut.replace("####TESTID####", TESTID)
    sOut = sOut.replace("####JSONFILELINK####", JSONFILElink)
    sOut = sOut.replace("####SECTION####", SECTION)
    sOut = sOut.replace("####SUBSECTION####", SUBSECTION)
    sOut = sOut.replace("####TEXTCOLOR####", TEXTCOLOR)
    sOut = sOut.replace("####DESCRIPTION####", DESCRIPTION)
    sOut = sOut.replace("####EXPECTATION####", EXPECTATION)
    sOut = sOut.replace("####COMMENT####", "" if COMMENT is None else f"<br>\n{COMMENT}")
    sOut = sOut.replace("####HINT####", "" if HINT is None else f"<br>\n{HINT}")
    return sOut


def _get_api_tests() -> list:
    """
Extracts all top level 'test_*' functions from 'test/jpp_test/test_api.py'
via the 'ast' module (no import/execution needed) together with their
docstring, so this overview never drifts out of sync with the actual test
module.
    """
    with open(API_TESTFILE, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=API_TESTFILE)

    listofTests = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            sDocstring = ast.get_docstring(node) or node.name.replace("_", " ")
            listofTests.append((node.name, sDocstring))
    return listofTests


def _html_api_row(nCntUsecases: int, sTestName: str, sDescription: str) -> str:
    sOut = HTML_API_ROW_PATTERN
    sOut = sOut.replace("####CNTUSECASES####", str(nCntUsecases))
    sOut = sOut.replace("####TESTFILELINK####", GITHUB_API_TESTFILE_LINK)
    sOut = sOut.replace("####TESTNAME####", sTestName)
    sOut = sOut.replace("####DESCRIPTION####", sDescription)
    return sOut


def gen_html_overview() -> None:
    """
Generates 'test/JPP_TestUsecases.html' from the use cases defined in
'test/testconfig/TestConfig.py' plus the API level tests in
'test/jpp_test/test_api.py' - a drop-in replacement for the HTML part of
the former '--codedump' feature.
    """
    listofAPITests = _get_api_tests()

    with open(HTMLFILE, "w", encoding="windows-1252", errors="xmlcharrefreplace") as fh:
        fh.write(HTML_HEAD)
        for nCntUsecases, dictUsecase in enumerate(listofdictUsecases, start=1):
            fh.write("<tr valign=\"middle\" align=\"left\">")
            fh.write(_html_row(nCntUsecases, dictUsecase))
            fh.write("</tr>\n")

        fh.write(HTML_SECTION_PATTERN.replace("####SECTIONTITLE####", "API Level Tests (test/jpp_test/test_api.py)"))
        for nCntUsecases, (sTestName, sDescription) in enumerate(listofAPITests, start=1):
            fh.write("<tr valign=\"middle\" align=\"left\">")
            fh.write(_html_api_row(nCntUsecases, sTestName, sDescription))
            fh.write("</tr>\n")

        sGenerated = "Generated: " + time.strftime("%d.%m.%Y - %H:%M:%S")
        fh.write(HTML_TAIL_PATTERN.replace("####GENERATED####", sGenerated))

    print(f"{len(listofdictUsecases)} use case(s) + {len(listofAPITests)} API test(s) written to '{HTMLFILE}'")


if __name__ == "__main__":
    gen_html_overview()
