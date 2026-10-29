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
# File: imports.py
#
# Loading of JSONP sources and expansion of "[import]" keys on AST level:
# the members of an imported file replace the import member (members with the same
# name which are defined before are overwritten). Imports with dynamic paths are
# expanded as soon as their path is known (see CJsonPreprocessor.json_loads).
#
#################################################################################

import os
import sys

import regex
from PythonExtensionsCollection.String.CString import CString

from .common import JsonpError, CNameMangling, CTextProcessor
from .jsonp_parser import Source, Obj, Arr, Member, Import, DollarKey, parse_jsonp

_RESERVED_TOKENS = [token.value for token in CNameMangling]


def normalize_file_path(path: str) -> str:
    """Normalizes a file path relative to the location of the executed script."""
    return CString.NormalizePath(path, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))


def check_reserved_tokens(content: str):
    for token in _RESERVED_TOKENS:
        if token in content:
            raise JsonpError(f"The JSONP content contains a reserved token '{token}'")


class ImportResolver:
    """Loads and parses JSONP sources and expands imports."""

    def __init__(self, python_syntax: bool, key_pattern: str):
        self.python_syntax = python_syntax
        self.key_pattern = key_pattern
        self._cache = {}

    # -- loading -----------------------------------------------------------------

    def parse(self, content: str, source: Source):
        """Parses comment free JSONP content."""
        check_reserved_tokens(content)
        return parse_jsonp(content, source, self.python_syntax, self.key_pattern)

    def load_file(self, path: str):
        """Loads and parses the JSONP file with the (normalized) path."""
        if path not in self._cache:
            if not os.path.isfile(path):
                raise JsonpError(f"File '{path}' is not existing!")
            try:
                content = CTextProcessor.load_and_remove_comments(path)
            except Exception as reason:
                raise JsonpError(f"Could not read json file '{path}' due to: '{reason}'!")
            self._cache[path] = self.parse(content, Source(path, os.path.dirname(path), path))
        return self._cache[path]

    # -- paths -------------------------------------------------------------------

    @staticmethod
    def static_path(imp: Import) -> str:
        return normalize_file_path(CString.NormalizePath(imp.value.text, sReferencePathAbs=imp.source.base_dir))

    @staticmethod
    def dynamic_path(value: str, base_dir: str) -> str:
        if not regex.match(r'^[/|\\].+$', value):
            value = CString.NormalizePath(value, sReferencePathAbs=base_dir)
        return normalize_file_path(value)

    @staticmethod
    def key(imp: Import):
        return (imp.source.label, imp.pos)

    # -- expansion ---------------------------------------------------------------

    def expand(self, node, chain: list, resolved: dict):
        """
Returns a copy of the AST in which all imports with known path are replaced by the
members of the imported files. ``chain`` is the list of files from the root to the
current file, ``resolved`` maps dynamic imports to their paths.
        """
        if isinstance(node, Obj):
            members = []
            for member in node.members:
                if isinstance(member, Import):
                    path = self.static_path(member) if member.is_static else resolved.get(self.key(member))
                    if path is None:
                        members.append(member)
                    else:
                        imported = [m if isinstance(m, Import) or m.origin is not None else Member(m.key, m.value, path)
                                    for m in self.import_file(path, chain, resolved).members]
                        # like in a dict update, an imported dollar key replaces an equal
                        # dollar key defined before (the earlier assignment is dropped)
                        refs = [m.key.ref for m in imported if isinstance(m, Member) and isinstance(m.key, DollarKey)]
                        if refs:
                            members = [m for m in members
                                       if not (isinstance(m, Member) and isinstance(m.key, DollarKey) and m.key.ref in refs)]
                        members.extend(imported)
                else:
                    members.append(Member(member.key, self.expand(member.value, chain, resolved), member.origin))
            return Obj(members)
        if isinstance(node, Arr):
            return Arr([self.expand(item, chain, resolved) for item in node.items])
        return node

    def import_file(self, path: str, chain: list, resolved: dict) -> Obj:
        if path in chain:
            previous_1 = chain[0]
            for item in chain:
                if item == path:
                    break
                previous_1 = item
            previous_2 = chain[-1]
            if path in (previous_1, previous_2):
                raise JsonpError(f"Cyclic import detection: The file '{path}' imports itself.")
            raise JsonpError(f"Cyclic import detection: The file '{path}' is imported by '{previous_1}' "
                             f"and by file '{previous_2}'.")
        tree = self.load_file(path)
        if not isinstance(tree, Obj):
            raise JsonpError(f"The imported file '{path}' must contain a JSON object.")
        return self.expand(tree, chain + [path], resolved)


def has_unresolved_imports(node) -> bool:
    if isinstance(node, Obj):
        return any(isinstance(m, Import) or has_unresolved_imports(m.value) for m in node.members)
    if isinstance(node, Arr):
        return any(has_unresolved_imports(item) for item in node.items)
    return False
