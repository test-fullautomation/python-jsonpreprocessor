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
# File: dollar_syntax.py
#
# Parser for the dollar operator expression language. It is independent from the
# JSONP document syntax and works on plain strings:
#
#   template  := ( text | ref )*
#   ref       := '${' name '}' index*
#   name      := ( name_char | ref )+          -- nested references are allowed
#   index     := '[' ws* ( int | "'" template "'" | ref ) ws* ']'
#
# Dotted names (``${a.b.0}``) are kept as plain name text here; splitting them into
# path segments requires runtime knowledge and is done by the interpreter.
#
#################################################################################

from dataclasses import dataclass, field
from typing import List, Union

import regex

from .common import JsonpError


@dataclass
class IntIndex:
    value: int


@dataclass
class StrIndex:
    parts: list                     # template parts (str | Ref)


@dataclass
class RefIndex:
    ref: 'Ref'


@dataclass
class Ref:
    name: list                      # parts (str | Ref) building the parameter name
    indices: list = field(default_factory=list)
    src: str = field(default='', compare=False)    # source text of the reference including indices

    def nested_refs(self):
        """Yields all references which are nested inside this reference."""
        for part in self.name:
            if isinstance(part, Ref):
                yield part
                yield from part.nested_refs()
        for index in self.indices:
            if isinstance(index, RefIndex):
                yield index.ref
                yield from index.ref.nested_refs()
            elif isinstance(index, StrIndex):
                for part in index.parts:
                    if isinstance(part, Ref):
                        yield part
                        yield from part.nested_refs()

    @property
    def is_static(self) -> bool:
        return next(self.nested_refs(), None) is None


Template = List[Union[str, Ref]]

_EMPTY_INDEX = regex.compile(r'[!@#\$%\^&\*\(\)=\[\]|;\s\-\+\'",<>?/`~]*')
_SUB_ELEMENT = regex.compile(r'[\p{Nd}\s]*[\p{L}_]+[\p{Nd}\s]*')


def err_curly_missing(expr: str) -> JsonpError:
    return JsonpError(f"Invalid syntax! One or more than one closed curly bracket is missing in expression '{expr.strip()}'.")


def err_index_in_curly(expr: str) -> JsonpError:
    return JsonpError(f"Invalid syntax: Found index or sub-element inside curly brackets in the parameter '{expr}'")


def err_slicing(expr: str) -> JsonpError:
    return JsonpError(f"Slicing is not supported (expression: '{expr}').")


class DollarParser:
    """
Recursive descent parser for dollar operator expressions.

**Arguments:**

* ``text``: The text to be parsed.
* ``orig``: The expression shown in error messages (default: ``text``).
* ``strict``: Unquoted context (values without quotes, keys). Brackets which cannot be
  interpreted as index are an error instead of plain text.
* ``with_indices``: Parse ``[...]`` after a reference as index (``False`` for Python inline code).
    """

    def __init__(self, text: str, orig: str = None, strict: bool = False, with_indices: bool = True):
        self.s = text
        self.n = len(text)
        self.orig = text if orig is None else orig
        self.strict = strict
        self.with_indices = with_indices

    # -- entry points ------------------------------------------------------------

    def parse_template(self, i: int = 0, stop: str = None):
        """Parses text and references until ``stop`` character (or end). Returns (parts, end)."""
        parts = []
        buf = []
        while i < self.n:
            c = self.s[i]
            if stop is not None and c == stop:
                break
            if self.s.startswith('${', i):
                if buf:
                    parts.append(''.join(buf))
                    buf = []
                ref, i = self.parse_ref(i)
                parts.append(ref)
            else:
                buf.append(c)
                i += 1
        if buf:
            parts.append(''.join(buf))
        return parts, i

    def parse_ref(self, i: int):
        """Parses a reference starting at ``${``. Returns (Ref, end)."""
        start = i
        i += 2
        name = []
        buf = []
        while True:
            if i >= self.n or self.s[i] == '\n':
                raise err_curly_missing(self.orig)
            if self.s.startswith('${', i):
                if buf:
                    name.append(''.join(buf))
                    buf = []
                ref, i = self.parse_ref(i)
                name.append(ref)
                continue
            c = self.s[i]
            if c == '}':
                i += 1
                break
            if c == '[':
                raise err_index_in_curly(self.orig)
            buf.append(c)
            i += 1
        if buf:
            name.append(''.join(buf))
        indices = []
        while self.with_indices and i < self.n and self.s[i] == '[':
            index, j = self._parse_index(i, start)
            if index is None:
                break
            indices.append(index)
            i = j
        return Ref(name, indices, self.s[start:i]), i

    # -- helpers -----------------------------------------------------------------

    def _skip_ws(self, i: int) -> int:
        while i < self.n and self.s[i] in ' \t':
            i += 1
        return i

    def _closing_bracket(self, i: int) -> int:
        depth = 0
        for k in range(i, self.n):
            c = self.s[k]
            if c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    return k
            elif c == '\n':
                break
        return -1

    def _parse_index(self, i: int, start: int):
        """Parses an index at '[' of the reference at ``start``. Returns (index, end) or (None, i) if it is no index."""
        k = self._closing_bracket(i)
        content = self.s[i + 1:k] if k >= 0 else None
        if content is not None:
            if ':' in content or regex.fullmatch(r'\s*[\+]*\-+\+*\d+\s*', content):
                raise err_slicing(self.s[start:k + 1])
        j = self._skip_ws(i + 1)
        if j < self.n and self.s[j] == "'":
            parts, j2 = self.parse_template(j + 1, stop="'")
            if j2 < self.n and self.s[j2] == "'":
                j3 = self._skip_ws(j2 + 1)
                if j3 < self.n and self.s[j3] == ']':
                    return StrIndex(parts), j3 + 1
        elif self.s.startswith('${', j):
            ref, j2 = self.parse_ref(j)
            j3 = self._skip_ws(j2)
            if j3 < self.n and self.s[j3] == ']':
                return RefIndex(ref), j3 + 1
        else:
            m = regex.compile(r'\+?(\d+)[ \t]*\]').match(self.s, j)
            if m is not None and m.group(1).isascii():
                return IntIndex(int(m.group(1))), m.end()
        if content is not None:
            if _SUB_ELEMENT.fullmatch(content):
                elem = content
                raise JsonpError(f"Invalid syntax! Sub-element '{elem}' in {self.orig} need to be referenced "
                                 f"using ${{{elem}}} or enclosed in quotes ['{elem}'].")
            if self.strict and _EMPTY_INDEX.fullmatch(content):
                raise JsonpError(f"Expression '{self.orig}' cannot be evaluated. Reason: A pair of square "
                                 f"brackets is empty or contains not allowed characters.")
        return None, i


def parse_template(text: str, orig: str = None) -> Template:
    """Parses a (quoted) string value into text parts and references."""
    parts, _ = DollarParser(text, orig).parse_template()
    return parts


def has_refs(parts: Template) -> bool:
    return any(isinstance(p, Ref) for p in parts)
