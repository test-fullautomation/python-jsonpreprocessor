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
# File: extensions/python_literals.py
#
# JSON syntax extension: Python literals
#
#   - True/False/None as values (syntax 'python' only)
#   - byte values b'...'
#
# PythonLiteralScannerMixin is a part of the JsonpParser.
#
#################################################################################

import ast
from dataclasses import dataclass

import regex

from ..common import JsonpError
from ..nodes import Scalar

_BYTES = regex.compile(r"b'[^']+'")
_PYTHON_CONSTANTS = (('None', None), ('True', True), ('False', False))


@dataclass(eq=False)
class Bytes:
    src: str


def evaluate_bytes(node: Bytes) -> bytes:
    return ast.literal_eval(node.src)


class PythonLiteralScannerMixin:
    """Python literals in values and keys (part of JsonpParser)."""

    def _scan_python_constant(self, i: int):
        """True/False/None at position ``i``. Returns (node, end) or None."""
        for name, value in _PYTHON_CONSTANTS:
            if self.s.startswith(name, i):
                return Scalar(value), i + len(name)
        return None

    def _scan_bytes(self, i: int):
        """Byte value at position ``i``. Returns (node, end) or None."""
        m = _BYTES.match(self.s, i)
        if m is None:
            return None
        return Bytes(m[0]), m.end()

    def _check_bytes_key(self, i: int):
        m = _BYTES.match(self.s, i)
        if m is not None:
            raise JsonpError(f"Type error in key {m[0]}. Key names must be strings; byte values are not supported.")
