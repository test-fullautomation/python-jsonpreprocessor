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
# File: jsonp_parser.py
#
# Parser of the JSONP document syntax (JSON + extensions). The result is an AST
# (see nodes.py). The structure follows the scanner of the Python standard library
# (json.decoder), so that JSON syntax errors keep the well known messages and
# positions.
#
# This module contains the JSON core syntax only. The syntax extensions are
# provided by mixin classes:
#
#   dollar_syntax/scanner.py        dollar operator expressions in values and keys (${...})
#   extensions/inline_code.py       Python inline code <<...>> as values
#   extensions/imports.py           "[import]" and "[import?]" keys
#   extensions/python_literals.py   Python literals True/False/None and byte values b'...'
#
#################################################################################

import json
import shlex
from json.decoder import scanstring, WHITESPACE
from typing import Optional

import regex

from .common import JsonpError, CKeyChecker, NUMBER_RE
from .dollar_syntax.scanner import DollarScannerMixin, normalize_line, normalize_indices
from .extensions.imports import ImportScannerMixin, IMPORT, IMPORT_OPT
from .extensions.inline_code import InlineScannerMixin, check_inline_in_dollar
from .extensions.python_literals import PythonLiteralScannerMixin
from .nodes import Source, Scalar, Str, Arr, Member, Obj

# --------------------------------------------------------------------------------
# Text preparation
# --------------------------------------------------------------------------------

def prepare_text(content: str) -> str:
    """
Line based preparation of the (comment free) JSONP text: removes empty lines and trailing
whitespace, checks quotation and normalizes index notation.
    """
    lines = []
    for line in content.splitlines():
        if line == '' or line.isspace():
            continue
        try:
            shlex.split(line)
        except Exception as error:
            raise JsonpError(f"{error} in line: '{line}'")
        line = line.rstrip()
        check_inline_in_dollar(line)
        lines.append(normalize_line(line) + "\n")
    return normalize_indices(''.join(lines))


def format_json_error(err: json.JSONDecodeError, file: Optional[str]) -> str:
    doc, pos = err.doc, err.pos
    before = min(50, pos)
    after = min(20, len(doc) - pos)
    nearby = f"... {doc[pos - before:pos + after]} ...".replace("\n", r"\n")
    message = f"{err}\nNearby: '{nearby}'"
    if file is not None:
        message = f"{message}\nIn file: '{file}'"
    return message


# --------------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------------

_WS = WHITESPACE.match
_WS_STR = ' \t\n\r'


class JsonpParser(DollarScannerMixin, InlineScannerMixin, ImportScannerMixin, PythonLiteralScannerMixin):
    """Parses prepared JSONP text into an AST."""

    def __init__(self, text: str, source: Source, python_syntax: bool, key_pattern: str):
        self.s = text
        self.n = len(text)
        self.source = source
        self.python_syntax = python_syntax
        self.key_checker = CKeyChecker(key_pattern)

    def parse(self):
        try:
            s = self.s
            idx = _WS(s, 0).end()
            try:
                node, end = self.scan_value(idx, 'top')
            except StopIteration as err:
                raise json.JSONDecodeError("Expecting value", s, err.value) from None
            end = _WS(s, end).end()
            if end != len(s):
                raise json.JSONDecodeError("Extra data", s, end)
            return node
        except json.JSONDecodeError as err:
            raise JsonpError(format_json_error(err, self.source.path)) from None

    # -- helpers -----------------------------------------------------------------

    def _eol(self, i: int) -> int:
        end = self.s.find('\n', i)
        return self.n if end < 0 else end

    def _key_region(self, i: int) -> str:
        """Text of the current line from ``i`` up to the last colon."""
        line = self.s[i:self._eol(i)]
        return line[:line.rfind(':')] if ':' in line else line

    # -- values ------------------------------------------------------------------

    def scan_value(self, i: int, ctx: str, for_import: bool = False):
        s = self.s
        try:
            c = s[i]
        except IndexError:
            raise StopIteration(i) from None
        if c == '"':
            text, end = scanstring(s, i + 1, True)
            return self._make_string(text, s[i:end], for_import), end
        if c == '{':
            return self.parse_object(i + 1)
        if c == '[':
            return self.parse_array(i + 1)
        if c == 'n' and s.startswith('null', i):
            return Scalar(None), i + 4
        if c == 't' and s.startswith('true', i):
            return Scalar(True), i + 4
        if c == 'f' and s.startswith('false', i):
            return Scalar(False), i + 5
        if self.python_syntax:
            result = self._scan_python_constant(i)
            if result is not None:
                return result
        m = NUMBER_RE.match(s, i)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                return Scalar(float(integer + (frac or '') + (exp or ''))), m.end()
            return Scalar(int(integer)), m.end()
        if c == 'N' and s.startswith('NaN', i):
            return Scalar(float('nan')), i + 3
        if c == 'I' and s.startswith('Infinity', i):
            return Scalar(float('inf')), i + 8
        if c == '-' and s.startswith('-Infinity', i):
            return Scalar(float('-inf')), i + 9
        if c == '$':
            return self._scan_bare(i, ctx)
        if c in '<>':
            return self._scan_inline(i, ctx)
        if c == 'b':
            result = self._scan_bytes(i)
            if result is not None:
                return result
        rest = self._rest_of_line(i)
        if '${' in rest:
            self._raise_invalid_bare(rest)
        raise StopIteration(i)

    def _rest_of_line(self, i: int) -> str:
        rest = self.s[i:self._eol(i)].rstrip()
        if rest.endswith(','):
            rest = rest[:-1].rstrip()
        return rest

    def _make_string(self, text: str, raw: str, for_import: bool):
        self._check_inline_in_string(text, raw)
        if '${' not in text:
            return Str(text)
        return self._dollar_string(text, for_import)

    # -- containers (structure as in json.decoder) -------------------------------

    def parse_array(self, end: int):
        s = self.s
        values = []
        nextchar = s[end:end + 1]
        if nextchar in _WS_STR:
            end = _WS(s, end + 1).end()
            nextchar = s[end:end + 1]
        if nextchar == ']':
            return Arr(values), end + 1
        while True:
            try:
                value, end = self.scan_value(end, 'array')
            except StopIteration as err:
                raise json.JSONDecodeError("Expecting value", s, err.value) from None
            values.append(value)
            nextchar = s[end:end + 1]
            if nextchar in _WS_STR:
                end = _WS(s, end + 1).end()
                nextchar = s[end:end + 1]
            end += 1
            if nextchar == ']':
                break
            elif nextchar != ',':
                raise json.JSONDecodeError("Expecting ',' delimiter", s, end - 1)
            comma_idx = end - 1
            try:
                if s[end] in _WS_STR:
                    end += 1
                    if s[end] in _WS_STR:
                        end = _WS(s, end + 1).end()
                nextchar = s[end:end + 1]
            except IndexError:
                pass
            if nextchar == ']':
                raise json.JSONDecodeError("Illegal trailing comma before end of array", s, comma_idx)
        return Arr(values), end

    def parse_object(self, end: int):
        s = self.s
        members = []
        nextchar = s[end:end + 1]
        if nextchar != '"':
            if nextchar in _WS_STR:
                end = _WS(s, end).end()
                nextchar = s[end:end + 1]
            if nextchar == '}':
                return Obj(members), end + 1
        while True:
            key_pos = end
            key, end = self._scan_key(end)
            if s[end:end + 1] != ':':
                end = _WS(s, end).end()
                if s[end:end + 1] != ':':
                    self._check_inline_before_colon(end)
                    raise json.JSONDecodeError("Expecting ':' delimiter", s, end)
            end += 1
            try:
                if s[end] in _WS_STR:
                    end += 1
                    if s[end] in _WS_STR:
                        end = _WS(s, end + 1).end()
            except IndexError:
                pass
            is_import = key is IMPORT or key is IMPORT_OPT
            try:
                value, end = self.scan_value(end, 'object', for_import=is_import)
            except StopIteration as err:
                raise json.JSONDecodeError("Expecting value", s, err.value) from None
            if is_import:
                members.append(self._make_import(value, key_pos, key is IMPORT_OPT))
            else:
                members.append(Member(key, value))
            try:
                nextchar = s[end]
                if nextchar in _WS_STR:
                    end = _WS(s, end + 1).end()
                    nextchar = s[end]
            except IndexError:
                nextchar = ''
            end += 1
            if nextchar == '}':
                break
            elif nextchar != ',':
                raise json.JSONDecodeError("Expecting ',' delimiter", s, end - 1)
            comma_idx = end - 1
            end = _WS(s, end).end()
            if s[end:end + 1] == '}':
                raise json.JSONDecodeError("Illegal trailing comma before end of object", s, comma_idx)
        return Obj(members), end

    # -- keys --------------------------------------------------------------------

    def _scan_key(self, i: int):
        s = self.s
        c = s[i:i + 1]
        if c == '"':
            text, end = scanstring(s, i + 1, True)
            return self._literal_key(text, s[i:end]), end
        if c == '$':
            self._check_inline_in_dollar_key(i)
            return self._dollar_key(i)
        if c == '<':
            self._check_inline_key(i)
        if c == 'b':
            self._check_bytes_key(i)
        raise json.JSONDecodeError("Expecting property name enclosed in double quotes", s, i)

    def _literal_key(self, text: str, raw: str):
        self._check_inline_in_key(text)
        self._check_dollar_in_key(text)
        if regex.match(r'^\s+[^\s]+.+$|^.+[^\s]+\s+$', text):
            text = text.strip()
        marker = self._import_marker(text)
        if marker is not None:
            return marker
        if r'\"' not in raw and text.isascii() and not self.key_checker.key_name_checker(text):
            raise JsonpError(self.key_checker.error_msg)
        return text


def parse_jsonp(text: str, source: Source, python_syntax: bool, key_pattern: str):
    """Parses comment free JSONP content into an AST."""
    return JsonpParser(prepare_text(text), source, python_syntax, key_pattern).parse()
