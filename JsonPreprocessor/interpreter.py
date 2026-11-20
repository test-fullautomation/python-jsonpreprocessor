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
# This module contains the evaluation of the JSON core syntax. The syntax
# extensions are provided by mixin classes and evaluators:
#
#   dollar_syntax/references.py     resolution of references ${...}
#   dollar_syntax/dollar_keys.py    assignments with dollar keys
#   extensions/imports.py           imports which are resolved at runtime
#   extensions/inline_code.py       evaluation of Python inline code <<...>>
#   extensions/python_literals.py   evaluation of byte values
#
#################################################################################

from .common import Busy, Lazy
from .dollar_syntax.dollar_keys import DollarKeyMixin
from .dollar_syntax.references import ReferenceMixin, collect_dotted_keys
from .dollar_syntax.scanner import Bare
from .extensions.imports import ImportExecutionMixin, Import
from .extensions.inline_code import InlineCodeEvaluator, Inline
from .extensions.python_literals import Bytes, evaluate_bytes
from .nodes import Scalar, Str, Arr, Obj


class Interpreter(ReferenceMixin, DollarKeyMixin, ImportExecutionMixin):
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
        if isinstance(value, Lazy):
            if value.busy:
                raise Busy()
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
        return Lazy(node, path)

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
                value = Lazy(member.value, path + [key])
            target[key] = value
        self._owners[id(target)] = (target, owners)

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
                        and not isinstance(owner[1], Lazy):
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
                if isinstance(current, Lazy):
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
            return self.inline.evaluate_node(node)
        if isinstance(node, Bytes):
            return evaluate_bytes(node)
        value = self.seed(node, path)
        self.complete(node, value, path)
        return value

