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
# File: dollar_syntax/scanner.py
#
# Dollar operator expressions within the JSONP document:
#
#   - normalization of index notation in the text
#   - strings containing references ("... ${a} ...")
#   - unquoted dollar operator expressions as values (${a}[0])
#   - dollar keys (${a}['b'] : value)
#
# DollarScannerMixin is a part of the JsonpParser.
#
#################################################################################

import json
from dataclasses import dataclass

import regex

from ..common import JsonpError, CTextProcessor
from ..nodes import Str
from .parser import DollarParser, Ref, err_curly_missing


@dataclass(eq=False)
class Bare:
    ref: Ref
    src: str


@dataclass(eq=False)
class DollarKey:
    text: str
    ref: Ref


def normalize_line(line: str) -> str:
    """Normalizes list indices '[+N]' in lines containing dollar operator expressions."""
    if '${' in line:
        line = regex.sub(r"\[\s*\+\s*(\d+)\s*\]", "[\\1]", line)
    return line


def normalize_indices(text: str) -> str:
    """Normalizes Unicode digits in list indices and whitespace in key indices."""
    text = CTextProcessor.normalize_digits(text)
    text = regex.sub(r'\[\s+\'', '[\'', text)
    text = regex.sub(r'\'\s+\]', '\']', text)
    return text


class DollarScannerMixin:
    """Dollar operator expressions in values and keys (part of JsonpParser)."""

    def _dollar_string(self, text: str, for_import: bool):
        """String value containing references."""
        if for_import and text.count('${') > text.count('}'):
            if '}' in text:
                raise err_curly_missing(text)
            raise JsonpError(f"Invalid expression found: '{text}' - The brackets mismatch!!!")
        parts, _ = DollarParser(text).parse_template()
        return Str(text, parts, '\\' in text)

    def _raise_invalid_bare(self, expr: str):
        if expr.startswith('${') and expr.count('${') > expr.count('}'):
            raise err_curly_missing(expr)
        if not regex.match(r"^\${.+[}\]]+$", expr) or regex.search(r"\${[^\${]+}(\[[^\[]+\])*[^\[]*\${", expr):
            raise JsonpError(f"Invalid expression found: '{expr}' - The double quotes are missing!!!")
        if expr.count('{') != expr.count('}') or expr.count('[') != expr.count(']'):
            raise JsonpError(f"Invalid expression found: '{expr}' - The brackets mismatch!!!")
        raise JsonpError(f"Invalid expression found: '{expr}'.")

    def _scan_bare(self, i: int, ctx: str):
        """Unquoted dollar operator expression as value: exactly one reference."""
        s = self.s
        rest = self._rest_of_line(i)
        if not s.startswith('${', i):
            self._raise_invalid_bare(rest)
        ref, end = DollarParser(s, orig=rest, strict=True).parse_ref(i)
        j = end
        while j < self.n and s[j] in ' \t':
            j += 1
        nxt = s[j:j + 1]
        if nxt not in (',', '}', ']', '\n', ''):
            self._raise_invalid_bare(rest)
        if nxt == ',' and ctx == 'object':
            following = s[j + 1:self._eol(j)].strip()
            if following and following[0] not in '"$}<':
                self._raise_invalid_bare(rest)
        src = s[i:end]
        if '\\' in src:
            # unquoted text is decoded like a JSON string
            try:
                decoded = json.loads(f'"{src}"')
                ref, _ = DollarParser(decoded, orig=rest, strict=True).parse_ref(0)
            except json.JSONDecodeError:
                pass
        return Bare(ref, src), end

    @staticmethod
    def _check_dollar_in_key(text: str):
        """References are not allowed in quoted key names."""
        if '${' in text:
            raise JsonpError(f"A substitution in key names is not allowed! Please update the key name \"{text}\"")

    def _dollar_key(self, i: int):
        s = self.s
        orig = self._dollar_key_text(i)
        if not s.startswith('${', i):
            raise json.JSONDecodeError("Expecting property name enclosed in double quotes", s, i)
        ref, end = DollarParser(s, orig=orig, strict=True).parse_ref(i)
        return DollarKey(s[i:end], ref), end

    def _dollar_key_text(self, i: int) -> str:
        """Text of an unquoted key (up to the colon outside of brackets)."""
        s = self.s
        depth = 0
        quote = False
        j = i
        while j < self.n and s[j] != '\n':
            c = s[j]
            if c == "'":
                quote = not quote
            elif not quote:
                if c in '[{':
                    depth += 1
                elif c in ']}':
                    depth -= 1
                elif c == ':' and depth <= 0:
                    break
            j += 1
        return s[i:j].strip()
