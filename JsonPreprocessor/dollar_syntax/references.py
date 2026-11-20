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
# File: dollar_syntax/references.py
#
# Resolution of dollar operator expressions (references) against the parameter
# store: dotted names, nested references, indices and the substitution of
# references inside strings.
#
# ReferenceMixin is a part of the Interpreter.
#
#################################################################################

import regex

from ..common import JsonpError, PYTHON_TYPE_ERRORS, Busy
from ..nodes import Str, Obj, Member
from .parser import Ref, IntIndex, StrIndex, err_slicing

_MISSING = object()


class NotAvailable(JsonpError):
    """A referenced parameter does not exist."""


def render(root, steps) -> str:
    """Renders a parameter path in the notation ${root}[0]['key']."""
    text = f"${{{root}}}"
    for step in steps:
        text += f"[{step}]" if isinstance(step, int) and not isinstance(step, bool) else f"['{step}']"
    return text


def collect_dotted_keys(node, keys: set) -> set:
    """Collects literal key names containing a dot (objects nested in objects only)."""
    if isinstance(node, Obj):
        for member in node.members:
            if isinstance(member, Member):
                if isinstance(member.key, str) and '.' in member.key:
                    keys.add(member.key)
                collect_dotted_keys(member.value, keys)
    return keys


class ReferenceMixin:
    """Resolution of references (part of Interpreter)."""

    def eval_string(self, node: Str) -> str:
        orig = node.text
        result = []
        for part in node.parts:
            if isinstance(part, Ref):
                root, steps = self.path_of(part, orig)
                value = self.lookup(root, steps)
                if isinstance(value, (list, dict)):
                    raise JsonpError(f"The substitution of parameter '{render(root, steps)}' inside the string value "
                                     f"'{orig}' is not allowed! Composite data types like lists and dictionaries "
                                     f"cannot be substituted inside strings.")
                result.append(str(value))
            else:
                result.append(repr(part)[1:-1] if node.escape_text else part)
        return ''.join(result)

    def split_dotted(self, name: str) -> list:
        """Splits a dotted parameter name; key names containing dots are kept together."""
        parts = name.split('.')
        if len(parts) == 1:
            return parts
        segments = []
        i = 0
        while i < len(parts):
            for j in range(i + 2, len(parts) + 1):
                candidate = '.'.join(parts[i:j])
                if candidate in self.dotted_keys:
                    segments.append(candidate)
                    i = j
                    break
            else:
                segments.append(parts[i])
                i += 1
        return segments

    def _child(self, container, step):
        if container is _MISSING:
            return _MISSING
        try:
            return self.force(container[step])
        except Exception:
            return _MISSING

    def path_of(self, ref: Ref, orig: str, key_mode: bool = False):
        """Resolves a reference to its parameter path (root name, list of steps)."""
        segments = self.split_dotted(self._name_of(ref, orig))
        root = segments[0]
        steps = []
        current = self._child(self.root, root)
        for segment in segments[1:]:
            step = segment
            if regex.fullmatch(r'\d+', segment) and isinstance(current, (list, str)) and int(segment) < len(current):
                step = int(segment)
            steps.append(step)
            current = self._child(current, step)
        for index in ref.indices:
            if isinstance(index, IntIndex):
                step = index.value
                if key_mode and isinstance(current, dict):
                    step = str(step)
            elif isinstance(index, StrIndex):
                step = self._index_text(index, orig)
            else:
                step = self.value_of(index.ref, orig)
                if isinstance(step, int) and not isinstance(step, bool) and step < 0:
                    raise err_slicing(ref.src)
                if isinstance(step, (dict, list)) or not isinstance(step, (int, str)):
                    if current is _MISSING:
                        self._raise_unresolved_parent(root, steps, orig)
                    self._raise_invalid_index(current, index.ref, orig)
            steps.append(step)
            current = self._child(current, step)
        return root, steps

    def _name_of(self, ref: Ref, orig: str) -> str:
        name = ''
        for part in ref.name:
            if isinstance(part, Ref):
                value = self.value_of(part, orig)
                if isinstance(value, (dict, list)):
                    parent = name.strip().rstrip('.')
                    try:
                        parent_value = self.value_of(Ref([parent]), orig) if parent else _MISSING
                    except JsonpError as error:
                        raise JsonpError(f"{error} Could not resolve expression '{orig}'.")
                    self._raise_invalid_index(parent_value, part, orig)
                name += str(value)
            else:
                name += part
        return name.strip()

    def _index_text(self, index: StrIndex, orig: str) -> str:
        text = ''
        for part in index.parts:
            if isinstance(part, Ref):
                root, steps = self.path_of(part, orig)
                value = self.lookup(root, steps)
                if isinstance(value, (dict, list)):
                    raise JsonpError(f"The substitution of parameter '{render(root, steps)}' inside the expression "
                                     f"'{orig}' is not allowed! Composite data types like lists and dictionaries "
                                     f"cannot be substituted as strings.")
                text += str(value)
            else:
                text += part
        return text

    def _raise_unresolved_parent(self, root, steps, orig):
        try:
            self.lookup(root, steps)
        except JsonpError as error:
            raise JsonpError(f"{error} Could not resolve expression '{orig}'.")
        raise JsonpError(f"Invalid expression found: '{orig}'.")

    def _raise_invalid_index(self, container, ref: Ref, orig: str):
        if isinstance(container, list):
            raise JsonpError(f"Invalid list index in expression '{orig}'. The datatype of parameter '{ref.src}' has to be 'int'.")
        if isinstance(container, dict):
            raise JsonpError(f"Invalid dictionary key in expression '{orig}'. The datatype of parameter '{ref.src}' has to be 'str'.")
        raise JsonpError(f"Invalid expression found: '{orig}'.")

    def lookup(self, root, steps):
        rendered = render(root, steps)
        if root not in self.root:
            raise NotAvailable(f"The parameter '{rendered}' is not available!")
        try:
            value = self.force(self.root[root])
            for step in steps:
                try:
                    value = self.force(value[step])
                except Busy:
                    raise
                except Exception as error:
                    message = str(error)
                    if any(item in message for item in PYTHON_TYPE_ERRORS):
                        raise JsonpError(f"Could not resolve expression '{rendered}'. Reason: {message.replace(' or slices', '')}")
                    if isinstance(error, KeyError) and regex.search(r"\[\s*" + regex.escape(message) + r"\s*\]", rendered):
                        raise JsonpError(f"Could not resolve expression '{rendered}'. Reason: Key error {message}")
                    raise NotAvailable(f"The parameter '{rendered}' is not available!")
        except Busy:
            raise NotAvailable(f"The parameter '{rendered}' is not available!") from None
        return value

    def value_of(self, ref: Ref, orig: str, key_mode: bool = False):
        root, steps = self.path_of(ref, orig, key_mode)
        return self.lookup(root, steps)
