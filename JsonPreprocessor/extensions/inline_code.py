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
# File: extensions/inline_code.py
#
# JSON syntax extension: Python inline code (<<...>>) as values.
#
#   - Inline node and scanning of inline code (InlineScannerMixin, part of the
#     JsonpParser), including the checks for inline code at not allowed positions
#   - evaluation (InlineCodeEvaluator, used by the Interpreter): dollar operator
#     expressions inside the code are translated into Python accesses to the
#     parameter store (self.jp_globals[...]); index expressions behind them are
#     plain Python code.
#
#################################################################################

from collections.abc import Mapping
from dataclasses import dataclass

import regex

from ..common import JsonpError, PY_INLINE_PATTERN
from ..dollar_syntax.parser import DollarParser, Ref, err_slicing

_JSON_TYPES = (str, int, float, bool, type(None), list, dict)
_INLINE_IN_DOLLAR = regex.compile(rf'\${{\s*{PY_INLINE_PATTERN}\s*}}')


@dataclass(eq=False)
class Inline:
    code: str
    src: str
    in_list: bool = False


def check_inline_in_dollar(line: str):
    """Python inline code must not be used within dollar operator expressions."""
    if '<<' in line or '>>' in line:
        match = _INLINE_IN_DOLLAR.search(line)
        if match is not None:
            raise JsonpError(f"Python inline code must not be used within dollar operator expression! "
                             f"Please check the expression '{match[0]}'")


class InlineScannerMixin:
    """Python inline code in values and checks for not allowed positions (part of JsonpParser)."""

    def _raise_inline_key(self, expr: str):
        raise JsonpError(f"Python inline code is not allowed at the left hand side of the colon. "
                         f"Please check expression '{expr}'.")

    @staticmethod
    def _check_inline_in_string(text: str, raw: str):
        if regex.search(PY_INLINE_PATTERN, text):
            raise JsonpError(f"Python inline code must not be embedded part of a string! Please check the expression {raw}")

    def _check_inline_in_key(self, text: str):
        """Quoted key name."""
        if regex.search(rf'["\s]*{PY_INLINE_PATTERN}["\s]*', text):
            self._raise_inline_key(text)

    def _check_inline_key(self, i: int):
        """Unquoted key starting with '<' at position ``i``."""
        region = self._key_region(i).strip()
        if regex.fullmatch(r'<<.*>>', region):
            self._raise_inline_key(region)

    def _check_inline_in_dollar_key(self, i: int):
        """Dollar key starting at position ``i``."""
        region = self._key_region(i)
        match = regex.search(PY_INLINE_PATTERN, region)
        if match is not None:
            code = match[0]
            expr = region.strip().replace(code, '"' + code.replace('"', '') + '"') + "'  "
            self._raise_inline_key(expr)

    def _check_inline_before_colon(self, i: int):
        """Key region in front of a missing colon at position ``i``."""
        match = regex.search(PY_INLINE_PATTERN, self._key_region(i))
        if match is not None:
            self._raise_inline_key(match[0])

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


class _Globals(Mapping):
    """Read access to the parameter store for Python inline code."""

    def __init__(self, interpreter):
        self._interpreter = interpreter

    def __getitem__(self, key):
        return self._interpreter.force(self._interpreter.root[key])

    def __iter__(self):
        return iter(self._interpreter.root)

    def __len__(self):
        return len(self._interpreter.root)


class _Context:
    """Provides ``self.jp_globals`` inside the Python inline code."""

    def __init__(self, interpreter):
        self.jp_globals = _Globals(interpreter)


def _python_access(root, steps) -> str:
    return "self.jp_globals" + ''.join(f"[{step!r}]" for step in [root] + list(steps))


class InlineCodeEvaluator:

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def to_python(self, code: str, orig: str) -> str:
        parts, _ = DollarParser(code, orig=orig, with_indices=False).parse_template()
        python = []
        for part in parts:
            if isinstance(part, Ref):
                root, steps = self.interpreter.path_of(part, orig)
                self.interpreter.lookup(root, steps)
                python.append(_python_access(root, steps))
            else:
                python.append(part)
        python = ''.join(python)
        if any(isinstance(part, Ref) for part in parts) and regex.search(r"\[\s*\+*\-+\+*\d+\s*\]", python):
            raise err_slicing(orig)
        return python

    def evaluate_node(self, node: Inline):
        if node.in_list:
            raise JsonpError(f"Python inline code must not be a part of a list! Please check the expression '{node.src}'")
        return self.evaluate(node.code, node.src)

    def evaluate(self, code: str, orig: str):
        python = self.to_python(code, orig)
        scope = {'self': _Context(self.interpreter)}
        try:
            result = {}
            exec(f"eval_value = {python}", scope, result)
            value = result['eval_value']
            # a string result may be Python code again
            if isinstance(value, str) and not regex.match(r'^[0-9\.\-+\s]+$', value) and 'self.jp_globals' not in value:
                try:
                    result = {}
                    exec(f"eval_value = {value}", scope, result)
                    value = result['eval_value']
                except Exception:
                    pass
            if not isinstance(value, _JSON_TYPES):
                raise JsonpError(f"The Python builtIn '{orig}' return the value with the datatype '{type(value)}' "
                                 f"is not suitable for JSON.")
        except Exception as error:
            raise JsonpError(f"Could not evaluate the Python builtIn {orig}. Reason: {error}")
        return value
