# Copyright 2020 Robert Bosch GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# *******************************************************************************
#
# Tests for the public API of CJsonPreprocessor that is not exercised by the
# file-based use case suite in test_usecases.py: jsonLoads/json_loads,
# jsonDump/json_dump, the current_cfg / key_pattern / syntax constructor
# parameters and the key_pattern validation, plus getVersion/getVersionDate.
# See test/testconfig/missing_tests.md, section 1, for the gap analysis
# this module closes.

import os

import pytest

from JsonPreprocessor import CJsonPreprocessor, CSyntaxType

TESTFILES_DIR = os.path.join(os.path.dirname(__file__), "..", "testfiles")


def test_json_loads_and_jsonLoads_are_equivalent():
    """Loads JSONP content from a string (not a file) via both 'json_loads()' and
    'jsonLoads()', including import resolution via 'reference_dir'."""
    content = """
{
    "[import]" : "./import/dotdict_format_common.jsonp",
    "local_param" : ${gPreprol.IntParam}
}
"""
    jpp = CJsonPreprocessor()
    result_snake = jpp.json_loads(content, reference_dir=TESTFILES_DIR)
    result_camel = jpp.jsonLoads(content, TESTFILES_DIR)

    assert dict(result_snake) == dict(result_camel)
    assert result_snake["local_param"] == 1


def test_json_loads_requires_string_content():
    """'json_loads()' rejects non-string input with a clear error."""
    jpp = CJsonPreprocessor()
    with pytest.raises(Exception, match="Expected a string"):
        jpp.json_loads(123)


def test_json_loads_rejects_missing_reference_dir():
    """'json_loads()' rejects a non-existing 'reference_dir'."""
    jpp = CJsonPreprocessor()
    with pytest.raises(Exception, match="is not existing"):
        jpp.json_loads('{"a": 1}', reference_dir=r"C:\does\not\exist")


def test_json_dump_writes_normalized_file(tmp_path):
    """'json_dump()' writes a dict to a JSON file and returns the normalized path."""
    jpp = CJsonPreprocessor()
    out_file = tmp_path / "dumped.json"

    returned_path = jpp.json_dump({"a": 1, "b": "text"}, str(out_file))

    assert os.path.isfile(returned_path)
    with open(returned_path, encoding="utf-8") as f:
        content = f.read()
    assert '"a": 1' in content
    assert '"b": "text"' in content


def test_current_cfg_preseeds_parameter_store():
    """Constructor parameter 'current_cfg' preseeds the parameter store."""
    jpp = CJsonPreprocessor(current_cfg={"existing_param": "preset_value"})

    result = jpp.json_loads('{\n    "derived" : ${existing_param}\n}\n')

    assert result["existing_param"] == "preset_value"
    assert result["derived"] == "preset_value"


def test_key_pattern_accepts_matching_key():
    """Constructor parameter 'key_pattern' accepts a key name matching a custom regex."""
    jpp = CJsonPreprocessor(key_pattern=r'^[a-z_]+$')

    result = jpp.json_loads('{\n    "valid_key" : 1\n}\n')

    assert result["valid_key"] == 1


def test_key_pattern_rejects_non_matching_key():
    """Constructor parameter 'key_pattern' rejects a key name violating a custom regex."""
    jpp = CJsonPreprocessor(key_pattern=r'^[a-z_]+$')

    with pytest.raises(Exception, match="invalid"):
        jpp.json_loads('{\n    "InvalidKey" : 1\n}\n')


@pytest.mark.parametrize(
    "bad_pattern, expected_message_part",
    [
        (123, "must be 'str'"),
        ("", "allows key names that are empty"),
        (".*", "allows key names that are empty"),
        ("   ", "allows a key name that contains only whitespace"),
    ],
)
def test_constructor_rejects_invalid_key_patterns(bad_pattern, expected_message_part):
    """Constructor validates 'key_pattern' itself: rejects non-str, '', '.*' and whitespace-only patterns."""
    with pytest.raises(Exception, match=expected_message_part):
        CJsonPreprocessor(key_pattern=bad_pattern)


def test_syntax_json_parses_json_literals():
    """Constructor parameter 'syntax=CSyntaxType.json' accepts JSON literals 'true'/'null'."""
    jpp = CJsonPreprocessor(syntax=CSyntaxType.json)

    result = jpp.json_loads('{\n    "a" : true,\n    "b" : null\n}\n')

    assert result["a"] is True
    assert result["b"] is None


def test_syntax_json_rejects_python_keywords():
    """Constructor parameter 'syntax=CSyntaxType.json' rejects the Python keyword 'True'."""
    jpp = CJsonPreprocessor(syntax=CSyntaxType.json)

    with pytest.raises(Exception):
        jpp.json_loads('{\n    "a" : True\n}\n')


def test_get_version_and_version_date():
    """'getVersion()' and 'getVersionDate()' return non-empty values."""
    jpp = CJsonPreprocessor()

    assert jpp.getVersion()
    assert jpp.getVersionDate()
