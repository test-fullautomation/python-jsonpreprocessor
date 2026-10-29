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
#################################################################################
#
# File: common.py
#
# Shared building blocks of the JsonPreprocessor:
#   - public helper classes (kept for backward compatibility of the module API)
#   - the internal exception type and shared constants/patterns
#
#################################################################################

import json
import unicodedata
from enum import Enum

import regex


class JsonpError(Exception):
    """Internal error type. Converted to a plain ``Exception`` at the API boundary."""


class CSyntaxType():
    python = "python"
    json = "json"


class CNameMangling(Enum):
    """
Token strings reserved by former implementations. JSONP content must not contain them.
    """
    AVOIDDATATYPE    = "JPavoidDataType_"
    COLONS           = "__handleColonsInLine__"
    NESTEDPARAM      = "__handleNestedParamInLine__"
    DUPLICATEDKEY_00 = "__handleDuplicatedKey__00"
    DUPLICATEDKEY_01 = "__handleDuplicatedKey__"
    STRINGCONVERT    = "__ConvertParameterToString__"
    LISTINDEX        = "__IndexOfList__"
    SLICEINDEX       = "__SlicingIndex__"
    STRINGVALUE      = "__StringValueMake-up__"
    HANDLEIMPORTED   = "__CheckImportedHandling__"
    DYNAMICIMPORTED  = "__DynamicImportedHandling__"
    PYTHONBUILTIN    = "__PythonBuiltInFunction__"
    PYBUILTINSTR     = "__StrInPythonInlineCode__"
    BYTEVALUE        = "__HandleByteValue__"


# Python inline code: <<...>> (no nested '<<' and no '>>' inside)
PY_INLINE_PATTERN = r'<<\s*(?:(?!<<\s*|>>).)*>>'

# Number literal (same as the former CPythonJSONDecoder; note: '\d' matches Unicode digits)
NUMBER_RE = regex.compile(r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
                          (regex.VERBOSE | regex.MULTILINE | regex.DOTALL))

# Fragments of Python exception messages which indicate an invalid access path
PYTHON_TYPE_ERRORS = ("object is not subscriptable",
                      "string indices must be integers",
                      "list indices must be integers",
                      "index out of range")


def type_name(value) -> str:
    """Returns the type of a value in the format "'int'"."""
    return regex.search(r"('.+')>\s*$", str(type(value)))[1]


class CPythonJSONDecoder(json.JSONDecoder):
    """
Extends the JSON syntax by the Python keywords ``True``, ``False`` and ``None``.

**Arguments:**

* ``json.JSONDecoder``

  / *Type*: object /

  Decoder object provided by ``json.loads``
    """

    NUMBER_RE = NUMBER_RE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_once = self.custom_scan_once

    def _custom_scan_once(self, string :str, idx: int) -> any:
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx) from None

        if nextchar == '"':
            return self.parse_string(string, idx + 1, self.strict)
        elif nextchar == '{':
            return self.parse_object((string, idx + 1), self.strict,
                self._custom_scan_once, self.object_hook, self.object_pairs_hook, self.memo)
        elif nextchar == '[':
            return self.parse_array((string, idx + 1), self._custom_scan_once)
        elif nextchar == 'n' and string[idx:idx + 4] == 'null':
            return None, idx + 4
        elif nextchar == 't' and string[idx:idx + 4] == 'true':
            return True, idx + 4
        elif nextchar == 'f' and string[idx:idx + 5] == 'false':
            return False, idx + 5
        elif nextchar == 'N' and string[idx:idx + 4] == 'None':
            return None, idx + 4
        elif nextchar == 'T' and string[idx:idx + 4] == 'True':
            return True, idx + 4
        elif nextchar == 'F' and string[idx:idx + 5] == 'False':
            return False, idx + 5

        m = CPythonJSONDecoder.NUMBER_RE.match(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = self.parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = self.parse_int(integer)
            return res, m.end()
        elif nextchar == 'N' and string[idx:idx + 3] == 'NaN':
            return self.parse_constant('NaN'), idx + 3
        elif nextchar == 'I' and string[idx:idx + 8] == 'Infinity':
            return self.parse_constant('Infinity'), idx + 8
        elif nextchar == '-' and string[idx:idx + 9] == '-Infinity':
            return self.parse_constant('-Infinity'), idx + 9
        else:
            raise StopIteration(idx)

    def custom_scan_once(self, string : str, idx : int) -> any:
        try:
            return self._custom_scan_once(string, idx)
        finally:
            self.memo.clear()


class CKeyChecker():
    """
CkeyChecker checks key names format based on a rule defined by user.
    """
    def __init__(self, key_pattern):
        self.key_pattern = key_pattern
        self.error_msg   = ''

    def key_name_checker(self, key_name: str):
        if key_name=='' or regex.match(r'^\s+$', key_name):
            self.error_msg = "Empty key name detected. Please enter a valid name."
            return False
        if regex.match(self.key_pattern, key_name):
            return True
        else:
            self.error_msg = f"Error: Key name '{key_name}' is invalid. Expected format: '{self.key_pattern}'"
            return False


class CTreeNode():
    """
The CTreeNode class is a custom tree data structure that allows to create and manage hierarchical data.
    """

    def __init__(self, value, parent=None):
        self.value    = value
        self.parent   = parent
        self.children = {}    # Dictionary to store children

    def add_child(self, value):
        """
Add a child node to the current node.

**Arguments:**

* ``value``

  / *Condition*: required / *Type*: str /

  The value for the new child node.

**Returns:**

  The new or existing child node.
        """
        if value in self.children:
            return self.children[value]
        child_node = CTreeNode(value, parent=self)
        self.children[value] = child_node
        return child_node

    def get_path_to_root(self):
        """
Retrieve the path from this node to the root.
        """
        path = []
        current = self
        while current:
            path.append(current.value)
            current = current.parent
        return path[::-1]


class CTextProcessor():
    @staticmethod
    def load_and_remove_comments(jsonP : str, is_file = True) -> str:
        """
Loads a given json file or json content and filters all C/C++ style comments.

**Arguments:**

* ``jsonP``

  / *Condition*: required / *Type*: str /

  Path of file to be processed or a JSONP content.

* ``is_file``

  / *Condition*: required / *Type*: bool /

  Indicates the jsonP is a path of file or a JSONP content, default value is True.

**Returns:**

* ``sContentCleaned``

  / *Type*: str /

  String version of JSON file after removing all comments.
        """
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return ""
            else:
                return s

        if is_file:
            with open(jsonP, mode='r', encoding='utf-8') as file:
                content = file.read()
        else:
            content = jsonP

        pattern = regex.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', regex.DOTALL | regex.MULTILINE)
        content_cleaned=regex.sub(pattern, replacer, content)
        return content_cleaned

    @staticmethod
    def multiple_replace(input : str, replacements : dict) -> str:
        """
    Replaces multiple parts in a string.

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``output``

  / *Type*: str /

        """
        pattern = regex.compile('|'.join(regex.escape(key) for key in replacements.keys()))
        output = pattern.sub(lambda x: replacements[x.group()], input)
        return output

    @staticmethod
    def normalize_digits(input : str) -> str:
        """
Convert/Replace all Unicode digits inside square brackets like [<digits>] to [<ASCII digits>].

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

  The string which need to find and convert Unicode digits to ASCII digits.

**Returns:**

* ``result``

  / *Type*: str /

  The string contains only ASCII digits within brackets.

**Raises:**

 * ``TypeError``: If input is not a string.
        """
        if not isinstance(input, str):
            error_msg = f'Invalid input type: {type(input)}. Expected str.'
            raise Exception(error_msg)

        pattern = r'\[\s*(\p{Nd}+)\s*\]'

        def replacer(match):
            digits = match.group(1)
            try:
                ascii_digits = ''.join(str(unicodedata.decimal(item)) for item in digits)
                return f'[{ascii_digits}]'
            except ValueError:
                # retain original match if conversion fails without further message
                return match.group(0)

        try:
            result = regex.sub(pattern, replacer, input)
        except regex.error as e:
            error_msg = f'Could not replace Unicode digits with their ASCII equivalents. Regex error occurred: {e}'
            raise Exception(error_msg)
        return result
