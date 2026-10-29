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
# File: interpreter.py
#
# Evaluates a JSONP AST into Python data.
#
# Evaluation model:
#   - The root object is the parameter store; references (${...}) are resolved
#     against it. Composite values are shared by reference.
#   - Every object is "seeded" before its members are executed: the keys are
#     created in their final order (a redefined key moves to the position of its
#     last definition) and values which do not depend on anything are available
#     immediately. Other values are represented by lazy placeholders which are
#     evaluated on demand. This allows references to parameters which are defined
#     later in the document.
#   - Members are then executed in document order; dollar keys (${...} : value)
#     overwrite existing or implicitly create new data structures.
#
#################################################################################

import ast

import regex

from .common import JsonpError, PYTHON_TYPE_ERRORS, type_name
from .dollar_syntax import Ref, IntIndex, StrIndex, err_slicing
from .inline_code import InlineCodeEvaluator
from .jsonp_parser import Scalar, Str, Bare, Inline, Bytes, Arr, Obj, Member, Import

_MISSING = object()
_SPECIAL_CHARACTERS = r"!#$%^&()=[]{}|;',?`~"


class NotAvailable(JsonpError):
    """A referenced parameter does not exist."""


class _Busy(Exception):
    """A lazy value is referenced during its own evaluation."""


class _Lazy:
    """Placeholder of a value which is evaluated on demand."""
    __slots__ = ('node', 'path', 'busy')

    def __init__(self, node, path):
        self.node = node
        self.path = path
        self.busy = False


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


class Interpreter:
    """
Evaluates an (import expanded) AST.

**Arguments:**

* ``resolver``: ImportResolver used for imports which are resolved at runtime.
* ``current_cfg``: Parameters which are available in addition to the document.
* ``lenient``: Pre-evaluation mode to determine paths of dynamic imports. The paths are
  collected in ``resolved``; imports which cannot be resolved yet are skipped.
    """

    def __init__(self, resolver, current_cfg: dict, lenient: bool = False, resolved: dict = None):
        self.resolver = resolver
        self.current_cfg = current_cfg
        self.lenient = lenient
        self.resolved = {} if resolved is None else resolved
        self.root = {}
        self.dotted_keys = set()
        self.inline = InlineCodeEvaluator(self)
        self._owners = {}

    def run(self, tree):
        self.dotted_keys = collect_dotted_keys(tree, set())
        if not isinstance(tree, Obj):
            return self.eval_node(tree, [])
        self.root.update(self.current_cfg)
        self.seed_object(tree, self.root, [])
        self.exec_object(tree, self.root, [])
        return self.root

    # -- lazy values -------------------------------------------------------------

    def force(self, value):
        if isinstance(value, _Lazy):
            if value.busy:
                raise _Busy()
            value.busy = True
            try:
                return self.eval_node(value.node, value.path)
            finally:
                value.busy = False
        return value

    # -- seeding -----------------------------------------------------------------

    def seed(self, node, path):
        if isinstance(node, Scalar):
            return node.value
        if isinstance(node, Str) and node.parts is None:
            return node.text
        if isinstance(node, Obj):
            value = {}
            self.seed_object(node, value, path)
            return value
        if isinstance(node, Arr):
            return [self.seed(item, path + [i]) for i, item in enumerate(node.items)]
        return _Lazy(node, path)

    def seed_object(self, node: Obj, target: dict, path: list):
        order = []
        count = {}
        definition = {}
        for member in node.members:
            if isinstance(member, Import):
                continue
            if isinstance(member.key, str):
                key = member.key
                definition[key] = member
            else:
                key = self._redefined_key(member.key, path, order)
                # a dollar key of an imported file does not reorder keys defined outside
                # of this file (imported files are processed separately and merged afterwards)
                if key is None or (member.origin is not None and definition[key].origin != member.origin):
                    continue
            if key in order:
                order.remove(key)
            order.append(key)
            count[key] = count.get(key, 0) + 1
        owners = {}
        for key in order:
            member = definition[key]
            if count[key] == 1:
                value = self.seed(member.value, path + [key])
                owners[key] = (member, value)
            else:
                value = _Lazy(member.value, path + [key])
            target[key] = value
        self._owners[id(target)] = (target, owners)

    def _redefined_key(self, key, path, order):
        """Name of an existing key of the current object which is redefined by a static dollar key."""
        ref = key.ref
        if not ref.is_static:
            return None
        steps = self.split_dotted(''.join(ref.name).strip())
        for index in ref.indices:
            if isinstance(index, IntIndex):
                steps.append(str(index.value))
            elif isinstance(index, StrIndex):
                steps.append(''.join(index.parts))
        if len(steps) != len(path) + 1 or any(str(a) != str(b) for a, b in zip(steps, path)):
            return None
        return steps[-1] if steps[-1] in order else None

    # -- execution ---------------------------------------------------------------

    def exec_object(self, node: Obj, target: dict, path: list):
        entry = self._owners.pop(id(target), None)
        owners = entry[1] if entry is not None and entry[0] is target else {}
        for member in node.members:
            if isinstance(member, Import):
                self.exec_import(member, target, path)
            elif isinstance(member.key, str):
                key = member.key
                owner = owners.get(key)
                if owner is not None and owner[0] is member and target.get(key) is owner[1] \
                        and not isinstance(owner[1], _Lazy):
                    self.complete(member.value, owner[1], path + [key])
                else:
                    target[key] = self.eval_node(member.value, path + [key])
            else:
                value = self.eval_node(member.value, path + [member.key.text])
                self.assign(member.key, value, path)

    def complete(self, node, seeded, path):
        """Completes a seeded value."""
        if isinstance(node, Obj):
            self.exec_object(node, seeded, path)
        elif isinstance(node, Arr):
            for i, item in enumerate(node.items):
                current = seeded[i]
                if isinstance(current, _Lazy):
                    seeded[i] = self.eval_node(item, path + [i])
                elif isinstance(item, (Obj, Arr)):
                    self.complete(item, current, path + [i])

    def eval_node(self, node, path):
        if isinstance(node, Scalar):
            return node.value
        if isinstance(node, Str):
            return node.text if node.parts is None else self.eval_string(node)
        if isinstance(node, Bare):
            return self.value_of(node.ref, node.src)
        if isinstance(node, Inline):
            if node.in_list:
                raise JsonpError(f"Python inline code must not be a part of a list! Please check the expression '{node.src}'")
            return self.inline.evaluate(node.code, node.src)
        if isinstance(node, Bytes):
            return ast.literal_eval(node.src)
        value = self.seed(node, path)
        self.complete(node, value, path)
        return value

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

    # -- references --------------------------------------------------------------

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
                except _Busy:
                    raise
                except Exception as error:
                    message = str(error)
                    if any(item in message for item in PYTHON_TYPE_ERRORS):
                        raise JsonpError(f"Could not resolve expression '{rendered}'. Reason: {message.replace(' or slices', '')}")
                    if isinstance(error, KeyError) and regex.search(r"\[\s*" + regex.escape(message) + r"\s*\]", rendered):
                        raise JsonpError(f"Could not resolve expression '{rendered}'. Reason: Key error {message}")
                    raise NotAvailable(f"The parameter '{rendered}' is not available!")
        except _Busy:
            raise NotAvailable(f"The parameter '{rendered}' is not available!") from None
        return value

    def value_of(self, ref: Ref, orig: str, key_mode: bool = False):
        root, steps = self.path_of(ref, orig, key_mode)
        return self.lookup(root, steps)

    # -- dollar keys -------------------------------------------------------------

    def _exists(self, path, orig=None, value=None) -> bool:
        current = self.root
        for step in path:
            try:
                current = self.force(current[step])
            except (KeyError, IndexError, _Busy):
                return False
            except TypeError as error:
                if orig is None:
                    return False
                raise JsonpError(f"Could not set parameter '{orig}' with value '{value}'! "
                                 f"Reason: {str(error).replace(' or slices', '')}")
        return True

    def assign(self, key, value, path: list):
        orig = key.text
        root, steps = self.path_of(key.ref, orig, key_mode=True)
        target = [root] + steps
        dynamic = orig.count('${') > 1
        if path:
            if len(target) <= len(path) or any(str(a) != str(b) for a, b in zip(target, path)):
                candidate = list(path) + target
                if self._exists(candidate):
                    absolute_1 = render(candidate[0], candidate[1:])
                    absolute_2 = '${' + '.'.join(str(step) for step in candidate) + '}'
                    raise JsonpError(f"Missing scope for parameter '${{{target[-1]}}}'. To change the value of this "
                                     f"parameter, an absolute path must be used: '{absolute_1}' or '{absolute_2}'.")
                self._raise_not_existing_key(orig)
            if not self._exists(target, orig, value):
                if dynamic:
                    self._raise_dynamic_key(orig)
                if len(target) == len(path) + 1:
                    self._raise_not_existing_key(orig)
        else:
            if dynamic and not self._exists(target, orig, value):
                self._raise_dynamic_key(orig)
            if not steps and root not in self.root:
                raise JsonpError(f"Could not resolve expression '${{{root}}}'. The based parameter '{root}' is not "
                                 f"defined yet! Use the '<name> : <value>' syntax to create a new based parameter.")
        self._set(target, value, orig)

    @staticmethod
    def _raise_not_existing_key(orig):
        raise JsonpError(f"A key with name '{orig}' does not exist at this position. "
                         f"Use the '<name> : <value>' syntax to create a new key.")

    @staticmethod
    def _raise_dynamic_key(orig):
        raise JsonpError(f"Identified dynamic name of key '{orig}' that does not exist. "
                         f"But new keys can only be created based on hard code names.")

    def _set(self, target, value, orig):
        current = self.root
        try:
            for step in target[:-1]:
                if isinstance(current, dict) and step not in current:
                    current[step] = {}
                child = current[step]
                if isinstance(child, _Lazy):
                    child = current[step] = self.force(child)
                current = child
            current[target[-1]] = value
        except Exception as error:
            raise JsonpError(f"Could not set parameter '{orig}' with value '{value}'! "
                             f"Reason: {str(error).replace(' or slices', '')}")

    # -- imports -----------------------------------------------------------------

    def exec_import(self, imp: Import, target: dict, path: list):
        """Handles an import which could not be expanded before (dynamic path)."""
        try:
            value = self.eval_node(imp.value, path)
            if not isinstance(value, str):
                raise JsonpError(f"The [import] key requires a value of type 'str', but the type is {type_name(value)}")
            file = self.resolver.dynamic_path(value, imp.source.base_dir)
        except JsonpError as error:
            if self.lenient:
                return
            if isinstance(error, NotAvailable):
                text = imp.value.text if isinstance(imp.value, Str) else imp.value.src
                params = regex.findall(rf'(\${{[^{regex.escape(_SPECIAL_CHARACTERS)}]+}}(\[.*\])*)', text)
                params = ''.join(f"{item[0]} " for item in params)
                raise JsonpError(f"Could not load the import file '{text}'. The parameter '{params}' is not available!")
            raise
        if self.lenient:
            self.resolved[self.resolver.key(imp)] = file
            return
        imported = self.resolver.import_file(file, [imp.source.label], self.resolved)
        for member in imported.members:
            if isinstance(member, Member) and isinstance(member.key, str):
                target.pop(member.key, None)
        self.seed_object(imported, target, path)
        self.exec_object(imported, target, path)
