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
# File: inline_code.py
#
# Evaluation of Python inline code (<<...>>). Dollar operator expressions inside
# the code are translated into Python accesses to the parameter store
# (self.jp_globals[...]); index expressions behind them are plain Python code.
#
#################################################################################

from collections.abc import Mapping

import regex

from .common import JsonpError
from .dollar_syntax import DollarParser, Ref, err_slicing

_JSON_TYPES = (str, int, float, bool, type(None), list, dict)


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
