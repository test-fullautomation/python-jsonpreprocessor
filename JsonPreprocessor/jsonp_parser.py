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
# (see the node classes below). The structure follows the scanner of the Python
# standard library (json.decoder), so that JSON syntax errors keep the well known
# messages and positions. JSONP extensions handled here:
#
#   - Python literals True/False/None (syntax 'python')
#   - "[import]" keys
#   - unquoted dollar operator expressions as values and keys (${...})
#   - Python inline code <<...>> as values
#   - byte values b'...'
#
# The dollar operator expressions themselves are parsed by dollar_syntax.
#
#################################################################################

import json
import shlex
from dataclasses import dataclass, field
from json.decoder import scanstring, WHITESPACE
from typing import Optional

import regex

from .common import (JsonpError, CKeyChecker, CTextProcessor, PY_INLINE_PATTERN, NUMBER_RE, type_name)
from .dollar_syntax import DollarParser, Ref, Template, err_curly_missing

# --------------------------------------------------------------------------------
# AST
# --------------------------------------------------------------------------------

@dataclass(frozen=True)
class Source:
    """A parsed JSONP source (file or content)."""
    path: Optional[str]         # normalized file path, None for content
    base_dir: Optional[str]     # reference directory for relative imports
    label: str                  # identification within the import chain


@dataclass(eq=False)
class Scalar:
    value: object


@dataclass(eq=False)
class Str:
    text: str
    parts: Optional[Template] = None    # set if the string contains references
    escape_text: bool = False


@dataclass(eq=False)
class Bare:
    ref: Ref
    src: str


@dataclass(eq=False)
class Inline:
    code: str
    src: str
    in_list: bool = False


@dataclass(eq=False)
class Bytes:
    src: str


@dataclass(eq=False)
class Arr:
    items: list


@dataclass(eq=False)
class DollarKey:
    text: str
    ref: Ref


@dataclass(eq=False)
class Member:
    key: object                 # str (literal key) or DollarKey
    value: object
    origin: str = None          # path of the imported file the member comes from (None: current file)


@dataclass(eq=False)
class Import:
    value: object               # Str (static or template), Bare or Inline
    source: Source
    pos: int

    @property
    def is_static(self) -> bool:
        return isinstance(self.value, Str) and self.value.parts is None


@dataclass(eq=False)
class Obj:
    members: list = field(default_factory=list)     # Member | Import


def is_pure_literal(node) -> bool:
    """True if the value of the node does not depend on anything."""
    if isinstance(node, Scalar):
        return True
    if isinstance(node, Str):
        return node.parts is None
    return False


# --------------------------------------------------------------------------------
# Text preparation
# --------------------------------------------------------------------------------

_INLINE_IN_DOLLAR = regex.compile(rf'\${{\s*{PY_INLINE_PATTERN}\s*}}')


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
        if '<<' in line or '>>' in line:
            match = _INLINE_IN_DOLLAR.search(line)
            if match is not None:
                raise JsonpError(f"Python inline code must not be used within dollar operator expression! "
                                 f"Please check the expression '{match[0]}'")
        if '${' in line:
            line = regex.sub(r"\[\s*\+\s*(\d+)\s*\]", "[\\1]", line)
        lines.append(line + "\n")
    text = CTextProcessor.normalize_digits(''.join(lines))
    text = regex.sub(r'\[\s+\'', '[\'', text)
    text = regex.sub(r'\'\s+\]', '\']', text)
    return text


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
_IMPORT_KEY = regex.compile(r'^\s*\[\s*import\s*\]\s*$')
_IMPORT = object()      # marker for "[import]" keys


def _is_ascii(text: str) -> bool:
    return text.isascii()


class JsonpParser:
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

    def _raise_inline_key(self, expr: str):
        raise JsonpError(f"Python inline code is not allowed at the left hand side of the colon. "
                         f"Please check expression '{expr}'.")

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
            if c == 'N' and s.startswith('None', i):
                return Scalar(None), i + 4
            if c == 'T' and s.startswith('True', i):
                return Scalar(True), i + 4
            if c == 'F' and s.startswith('False', i):
                return Scalar(False), i + 5
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
            m = regex.compile(r"b'[^']+'").match(s, i)
            if m is not None:
                return Bytes(m[0]), m.end()
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
        if regex.search(PY_INLINE_PATTERN, text):
            raise JsonpError(f"Python inline code must not be embedded part of a string! Please check the expression {raw}")
        if '${' not in text:
            return Str(text)
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

    def _scan_inline(self, i: int, ctx: str):
        """Python inline code <<...>> as value."""
        s = self.s
        j = i
        depth = 0
        quote = None
        while j < self.n:
            c = s[j]
            if c == '\n':
                break
            if quote is not None:
                if c == '\\':
                    j += 2
                    continue
                if c == quote:
                    quote = None
            elif c in '"\'':
                quote = c
            elif c in '([{':
                depth += 1
            elif c in ')]}':
                if depth == 0:
                    break
                depth -= 1
            elif c == ',' and depth == 0:
                break
            j += 1
        region = s[i:j].rstrip()
        if regex.match(r'^\s*<<\s*>>\s*$', region):
            raise JsonpError(f"The Python builtIn must not be empty. Please check '{region}'")
        if not regex.search(PY_INLINE_PATTERN, region):
            message = f"Invalid syntax: Check the Python inline code '{region}'. "
            if region.count('<<') > region.count('>>'):
                message += "Missing closed bracket!"
            elif region.count('<<') < region.count('>>'):
                message += "Missing opened bracket!"
            else:
                message += "The correct syntax is '<<Python_inline_code>>'!"
            raise JsonpError(message)
        if region.startswith('<<') and region.endswith('>>'):
            code = regex.search(r'<<\s*(.*)>>', region)[1]
            return Inline(code, region, ctx == 'array'), i + len(region)
        raise StopIteration(i)

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
                    match = regex.search(PY_INLINE_PATTERN, self._key_region(end))
                    if match is not None:
                        self._raise_inline_key(match[0])
                    raise json.JSONDecodeError("Expecting ':' delimiter", s, end)
            end += 1
            try:
                if s[end] in _WS_STR:
                    end += 1
                    if s[end] in _WS_STR:
                        end = _WS(s, end + 1).end()
            except IndexError:
                pass
            try:
                value, end = self.scan_value(end, 'object', for_import=key is _IMPORT)
            except StopIteration as err:
                raise json.JSONDecodeError("Expecting value", s, err.value) from None
            if key is _IMPORT:
                members.append(self._make_import(value, key_pos))
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
            return self._dollar_key(i)
        if c == '<':
            region = self._key_region(i).strip()
            if regex.fullmatch(r'<<.*>>', region):
                self._raise_inline_key(region)
        if c == 'b':
            m = regex.compile(r"b'[^']+'").match(s, i)
            if m is not None:
                raise JsonpError(f"Type error in key {m[0]}. Key names must be strings; byte values are not supported.")
        raise json.JSONDecodeError("Expecting property name enclosed in double quotes", s, i)

    def _literal_key(self, text: str, raw: str):
        if regex.search(rf'["\s]*{PY_INLINE_PATTERN}["\s]*', text):
            self._raise_inline_key(text)
        if '${' in text:
            raise JsonpError(f"A substitution in key names is not allowed! Please update the key name \"{text}\"")
        if regex.match(r'^\s+[^\s]+.+$|^.+[^\s]+\s+$', text):
            text = text.strip()
        if _IMPORT_KEY.match(text.lower()):
            return _IMPORT
        if r'\"' not in raw and _is_ascii(text) and not self.key_checker.key_name_checker(text):
            raise JsonpError(self.key_checker.error_msg)
        return text

    def _dollar_key(self, i: int):
        s = self.s
        region = self._key_region(i)
        match = regex.search(PY_INLINE_PATTERN, region)
        if match is not None:
            code = match[0]
            expr = region.strip().replace(code, '"' + code.replace('"', '') + '"') + "'  "
            self._raise_inline_key(expr)
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

    # -- imports -----------------------------------------------------------------

    def _make_import(self, value, pos: int) -> Import:
        if isinstance(value, Scalar) and not isinstance(value.value, str) or isinstance(value, (Obj, Arr, Bytes)):
            sample = {Obj: {}, Arr: []}.get(type(value), getattr(value, 'value', b''))
            raise JsonpError(f"The [import] key requires a value of type 'str', but the type is {type_name(sample)}")
        return Import(value, self.source, pos)


def parse_jsonp(text: str, source: Source, python_syntax: bool, key_pattern: str):
    """Parses comment free JSONP content into an AST."""
    return JsonpParser(prepare_text(text), source, python_syntax, key_pattern).parse()
