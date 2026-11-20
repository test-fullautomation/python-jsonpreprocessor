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
# File: dollar_syntax/dollar_keys.py
#
# Dollar keys (${...} : value): overwrite existing or implicitly create new data
# structures in the parameter store. A static dollar key which redefines a key of
# the current object moves this key to its position (see Interpreter.seed_object).
#
# DollarKeyMixin is a part of the Interpreter.
#
#################################################################################

from ..common import JsonpError, Busy, Lazy
from .parser import IntIndex, StrIndex
from .references import render


class DollarKeyMixin:
    """Assignments with dollar keys (part of Interpreter)."""

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

    def _exists(self, path, orig=None, value=None) -> bool:
        current = self.root
        for step in path:
            try:
                current = self.force(current[step])
            except (KeyError, IndexError, Busy):
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
                if isinstance(child, Lazy):
                    child = current[step] = self.force(child)
                current = child
            current[target[-1]] = value
        except Exception as error:
            raise JsonpError(f"Could not set parameter '{orig}' with value '{value}'! "
                             f"Reason: {str(error).replace(' or slices', '')}")
