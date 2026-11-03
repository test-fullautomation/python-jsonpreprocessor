# JsonPreprocessor Self-Test (`python-jsonpreprocessor/test`)

> All paths in this document are relative to the component root directory
> `python-jsonpreprocessor` (e.g. `test/testconfig/TestConfig.py`).

---

## Section 1: High-Level Overview (for beginners / management)

### What is this about?

`JsonPreprocessor` is a Python library that extends plain JSON files with
additional capabilities (parameter substitution, file imports, inline Python
code, comments, etc.). To keep this library reliable, and to make sure that
no future change accidentally breaks any existing feature, there is an
**automated test suite** (a "self-test") located under `test/`.

### How does the basic principle work?

Think of the test suite as a long **checklist of examples**:

- Each example consists of a small sample JSON file (the input) and a clear
  expectation: "the result must look exactly like this" or "this must be
  rejected with exactly this error message".
- A test runner (**pytest**) automatically works through this checklist from
  top to bottom, loads every sample file with `JsonPreprocessor`, and
  compares the actual result against the expectation.
- At the end you get a simple number: "278 out of 278 tests passed" (as of
  the latest additions), or a precise listing of which examples failed and
  why.

### What is the checklist made of?

The checklist itself lives in **a single file**,
`test/testconfig/TestConfig.py`. This is a deliberate design choice: there is
only **one single source of truth** for all test cases, not scattered
copies. Each test case has a unique ID (`TESTID`, e.g. `JPP_0001`), a
description, an expectation, and a reference to a small sample JSON file
under `test/testfiles/`.

In addition to this main checklist, there is a second, smaller test module
(`test/jpp_test/test_api.py`) that doesn't check JSON files, but the
library's programming interface itself (e.g. "Can I also load JSON content
directly from a text string instead of from a file?").

### Where can I see the result?

For non-programmers, there is a ready-made **HTML overview**
(`test/JPP_TestUsecases.html`) that lists all test cases from the main
checklist as well as the additional API tests in a readable form - with
description, expectation, and a link to the respective sample file. This
file is automatically generated from the checklist by a small helper script
(`test/gen_html_overview.py`), so it never needs to be maintained by hand.

### Why does this matter?

- **Safety for changes:** every code change to `JsonPreprocessor` can
  immediately be checked against all ~280 examples.
- **Documentation through examples:** the checklist also shows what the
  library can do (and what it must explicitly reject).
- **Traceability:** a failed check shows exactly which example is affected,
  what was expected, and what actually happened.

---

## Section 2: Detailed Information (for application developers and testers)

### Directory structure

```
test/
├── testconfig/
│   ├── TestConfig.py         # single source of truth for all use cases (listofdictUsecases)
│   └── missing_tests.md      # gap analysis: implementation vs. test coverage
├── testfiles/
│   └── jpp-test_config_*.jsonp, import/..., ...
├── jpp_test/
│   ├── conftest.py           # pytest fixtures, path constants
│   ├── comparators.py        # comparison logic (return values / exceptions)
│   ├── test_usecases.py      # data-driven tests sourced from TestConfig.py
│   └── test_api.py           # standalone tests of the public API
├── gen_html_overview.py      # generates JPP_TestUsecases.html
└── JPP_TestUsecases.html     # generated, human readable overview
```

### 2.1 `test/testconfig/TestConfig.py` - the use case database

Contains the list `listofdictUsecases`. Each entry is a `dict` with the
following keys:

| Key | Required | Meaning |
|---|---|---|
| `TESTID` | yes | Unique ID, e.g. `JPP_0275`. Numbering convention per `SECTION`: `GOODCASE` starts at `x00`, `BADCASE` starts at `x50`. |
| `DESCRIPTION` | yes | Short description of the test case. |
| `EXPECTATION` | yes | What is expected, in plain text (also shown in the failure report). |
| `SECTION` / `SUBSECTION` | yes | Thematic grouping (e.g. `FILE_IMPORTS` / `BADCASE`). |
| `JSONFILE` | yes | Relative path to the sample file under `test/testfiles/`. |
| `EXPECTEDEXCEPTION` | yes (or `None`) | Expected (partial) text of an exception. `None` means: no exception must be raised. |
| `EXPECTEDRETURN` | yes (or `None`) | Expected pretty-printed representation of the return value. `None` means: no return value is expected (e.g. because an error is expected instead). |
| `HINT`, `COMMENT` | optional | Additional free-text notes. |
| `USERAWPATH` | optional | If `True`: `JSONFILE` is resolved relative to `test/` instead of relative to `testconfig/` (see `conftest.py`). |

If both `EXPECTEDEXCEPTION` and `EXPECTEDRETURN` are `None`, the
corresponding test case is skipped in `test_usecases.py` (`pytest.skip`,
status "UNKNOWN") - a remnant of the former test concept, deliberately kept
to allow marking temporarily deactivated cases.

### 2.2 `test/jpp_test/conftest.py` - fixtures and path conventions

- Adds `test/testconfig` to `sys.path` so that `TestConfig.py` can be
  imported.
- Defines `TESTCONFIGPATH` (reference path for regular `JSONFILE` entries)
  and `TESTBASEPATH` (reference path for `USERAWPATH: True` cases).
- Provides the `jpp` fixture: a **single, session-wide shared**
  `CJsonPreprocessor` instance. This is deliberate (identical to the former
  test concept): all ~264 use cases run against the same instance, which
  also acts as a simple stress test (no hidden side effects between
  consecutive calls).

### 2.3 `test/jpp_test/comparators.py` - comparison logic

Two functions, ported 1:1 from the former `component_test.py`:

- `analyze_returned_values(EXPECTEDRETURN, dictReturned)`: compares the
  pretty-printed lines of the actual return value line by line against the
  expected text.
- `analyze_exceptions(EXPECTEDEXCEPTION, sException)`: checks via
  **substring containment** (`EXPECTEDEXCEPTION in sException`), not an exact
  match. This allows `TestConfig.py` to specify only the relevant, stable
  part of an error message, without having to update every test case
  whenever the wording of an error message changes slightly.

Both functions return a list of error strings (empty list = success), which
is then evaluated in `test_usecases.py` via `assert not listErrors`.

### 2.4 `test/jpp_test/test_usecases.py` - the data-driven test run

- Parametrizes **one** test function
  (`test_jsonpreprocessor_usecase`) with every entry in
  `listofdictUsecases`. Each use case appears in the pytest output as its
  own test case with the ID `<TESTID>-<SECTION>-<SUBSECTION>`
  (e.g. `JPP_1167-FILE_IMPORTS-BADCASE`).
- Flow per test case:
  1. Normalize the `JSONFILE` path (depending on `USERAWPATH`).
  2. Call `jpp.jsonLoad(JSONFILE)`.
  3. Capture the return value or the raised exception.
  4. Check both against `EXPECTEDRETURN` / `EXPECTEDEXCEPTION` via
     `comparators.py`.
  5. On mismatch: `assert` with `DESCRIPTION`, `EXPECTATION`, and the
     concrete error texts in the report - directly copy-pastable into a bug
     report.

This module fully replaces the former two-layer solution
(`component_test.py` + generated `pytest/pytestfiles/*` files with subprocess
indirection), without touching the data source (`TestConfig.py`) itself.

### 2.5 `test/jpp_test/test_api.py` - public API tests

While `test_usecases.py` exclusively exercises the file-path-based call
`jpp.jsonLoad(JSONFILE)`, `test_api.py` covers the parts of the public
interface that don't fit into this file-based scheme - e.g. alternative
constructor parameters or alternative entry points. These are plain,
standalone pytest functions (no shared data model like `TestConfig.py`),
covering among others:

- `json_loads()` / `jsonLoads()` - loading JSONP content directly from a
  string (including the `reference_dir` parameter for import resolution).
- `json_dump()` / `jsonDump()` - writing a `dict` back to a JSON file.
- Constructor parameter `current_cfg` (pre-seeding the parameter store).
- Constructor parameter `key_pattern` (custom regex for valid key names),
  including validation of the pattern itself (parametrized test for invalid
  patterns: non-string, empty, `.*`, whitespace-only).
- `syntax=CSyntaxType.json` (strict JSON syntax without the Python keywords
  `True`/`False`/`None`).
- `getVersion()` / `getVersionDate()`.

Every test function carries a short docstring - this is automatically picked
up by `gen_html_overview.py` and used as the description in the HTML
overview (see 2.7).

### 2.6 `test/testconfig/missing_tests.md` - gap analysis

Documents a systematic comparison of the implementation
(`JsonPreprocessor/*.py`) against test coverage, organized into:

1. Untested public API methods (now marked `[ERLEDIGT]`/done, see
   `test_api.py`).
2. Existing error-path code branches without a corresponding test case (now
   marked `[ERLEDIGT]`/done, see the associated `TESTID`s per row).
3. Lower-priority edge cases (currently still open).

This file serves as the working basis for future test extensions and should
be kept up to date whenever new gaps are identified.

### 2.7 `test/gen_html_overview.py` - generated overview

A standalone script (`python test/gen_html_overview.py`) that generates
`test/JPP_TestUsecases.html`:

- **Section 1 of the HTML file:** one row per entry in
  `listofdictUsecases` (TestConfig.py), with TESTID, section/subsection
  (color-coded: green = GOODCASE, red = BADCASE), description, expectation,
  and a link to the sample file on GitHub.
- **Section 2 of the HTML file:** one row per `test_*` function in
  `test/jpp_test/test_api.py`. The list of these functions is **not**
  maintained manually, but extracted at generation time directly from the
  source code of `test_api.py` via the `ast` module (function name +
  docstring) - the overview can therefore never go stale with respect to the
  test code.
- At the end, the script prints a short summary to the console, e.g.
  `264 use case(s) + 11 API test(s) written to '...'`. Note: a parametrized
  API test (`test_constructor_rejects_invalid_key_patterns`) counts as
  **one** row in this overview, but appears as **four** individual test
  cases in the `pytest` run (one per parameter combination) - so "number of
  rows in the overview" is not necessarily identical to "number of tests
  executed by pytest".

### 2.8 Running the tests

```powershell
cd python-jsonpreprocessor
$env:PYTHONPATH = "<path-to-repo>\python-jsonpreprocessor"
python -m pytest test/jpp_test                       # full suite
python -m pytest test/jpp_test/test_api.py -v         # API tests only
python -m pytest test/jpp_test -k "JPP_1167"          # single use case
python test/gen_html_overview.py                      # regenerate the overview
```

The API tests are plain, standalone pytest functions (no shared data model
like `TestConfig.py`). No extra configuration step is needed:
`test/jpp_test/pytest.ini` makes pytest automatically discover every
`test_*.py` file under `test/jpp_test` - so `test_api.py` is always included
whenever `test/jpp_test` (or the parent `test/`) is given as the test
target. More fine-grained invocation variants:

```powershell
# a single API test
python -m pytest test/jpp_test/test_api.py::test_json_loads_and_jsonLoads_are_equivalent -v

# a single parameter case of the parametrized test
python -m pytest "test/jpp_test/test_api.py::test_constructor_rejects_invalid_key_patterns[.*-allows key names that are empty]" -v
```

### 2.9 Conventions for new test cases

- Always add new use cases to `TestConfig.py`, never create a copy of the
  data source.
- Follow the TESTID numbering convention (`GOODCASE` starting at `x00`,
  `BADCASE` starting at `x50` within the respective `SECTION`).
- Keep `EXPECTEDEXCEPTION` as short as possible, but unambiguous (substring
  match - see 2.3), so test cases stay robust against small wording changes
  in the error message.
- Place new sample files under `test/testfiles/`, following the same naming
  scheme (`jpp-test_config_<TESTID-digits>.jsonp`).
- After every extension: re-run `python test/gen_html_overview.py` so the
  HTML overview stays current.
