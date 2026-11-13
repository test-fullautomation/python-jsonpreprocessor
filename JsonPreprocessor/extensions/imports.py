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
# File: extensions/imports.py
#
# JSON syntax extension: "[import]" and "[import?]" keys (value: path or import
# object with the keys 'file', 'if', 'else' and 'optional').
#
#   - Import node and scanning of import members (ImportScannerMixin, part of the
#     JsonpParser)
#   - loading of JSONP sources and expansion of imports on AST level
#     (ImportResolver): the members of an imported file replace the import member
#     (members with the same name which are defined before are overwritten).
#     Imports with dynamic paths are expanded as soon as their path is known
#     (see CJsonPreprocessor.__process).
#   - execution of imports which could not be expanded before (ImportExecutionMixin,
#     part of the Interpreter)
#
#################################################################################

import os
import sys
from dataclasses import dataclass

import regex
from PythonExtensionsCollection.String.CString import CString

from ..common import JsonpError, CNameMangling, CTextProcessor, type_name
from ..dollar_syntax.references import NotAvailable
from ..dollar_syntax.scanner import DollarKey
from ..nodes import Source, Scalar, Str, Arr, Obj, Member
from .python_literals import Bytes

_RESERVED_TOKENS = [token.value for token in CNameMangling]
_SPECIAL_CHARACTERS = r"!#$%^&()=[]{}|;',?`~"
_IMPORT_KEY = regex.compile(r'^\s*\[\s*import\s*(\?)?\s*\]\s*$')
IMPORT = object()       # marker for "[import]" keys
IMPORT_OPT = object()   # marker for "[import?]" keys
_IMPORT_OPTIONS = ('file', 'if', 'else', 'optional')
SKIP = ''   # resolved path of an import which is not executed (condition false or optional file missing)


@dataclass(eq=False)
class Import:
    value: object               # Str (static or template), Bare or Inline
    source: Source
    pos: int
    condition: object = None    # value node of 'if' (None: unconditional)
    alternative: object = None  # value node of 'else' (None: nothing is imported if the condition is false)
    optional: bool = False      # a not existing file is ignored

    @property
    def is_static(self) -> bool:
        return self.condition is None and isinstance(self.value, Str) and self.value.parts is None


def normalize_file_path(path: str) -> str:
    """Normalizes a file path relative to the location of the executed script."""
    return CString.NormalizePath(path, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))


def check_reserved_tokens(content: str):
    for token in _RESERVED_TOKENS:
        if token in content:
            raise JsonpError(f"The JSONP content contains a reserved token '{token}'")


class ImportScannerMixin:
    """Import members (part of JsonpParser)."""

    @staticmethod
    def _import_marker(text: str):
        """IMPORT or IMPORT_OPT if the key name is an import key, otherwise None."""
        match = _IMPORT_KEY.match(text.lower())
        if match is None:
            return None
        return IMPORT if match[1] is None else IMPORT_OPT

    def _make_import(self, value, pos: int, optional: bool) -> Import:
        if isinstance(value, Obj):
            if optional:
                raise JsonpError("The [import?] key requires a value of type 'str'. "
                                 "Use the key 'optional' of an [import] object instead.")
            return self._make_import_object(value, pos)
        self._check_import_path(value, "The [import?] key" if optional else "The [import] key")
        return Import(value, self.source, pos, optional=optional)

    @staticmethod
    def _literal_type(node) -> str:
        """Type name of a literal value node."""
        sample = {Obj: {}, Arr: [], Bytes: b''}.get(type(node), getattr(node, 'value', getattr(node, 'text', None)))
        return type_name(sample)

    def _check_import_path(self, value, name: str):
        if isinstance(value, Scalar) and not isinstance(value.value, str) or isinstance(value, (Obj, Arr, Bytes)):
            raise JsonpError(f"{name} requires a value of type 'str', but the type is {self._literal_type(value)}")

    def _make_import_object(self, node: Obj, pos: int) -> Import:
        """Import object: {"file": <path>, "if": <condition>, "else": <path>, "optional": <bool>}"""
        options = {}
        for member in node.members:
            key = member.key if isinstance(member, Member) else '[import]'
            if not isinstance(key, str) or key not in _IMPORT_OPTIONS:
                key = key.text if isinstance(key, DollarKey) else key
                raise JsonpError(f"Invalid key '{key}' in [import] object. "
                                 f"Allowed keys are: {', '.join(repr(k) for k in _IMPORT_OPTIONS)}.")
            if key in options:
                raise JsonpError(f"Duplicate key '{key}' in [import] object.")
            options[key] = member.value
        if 'file' not in options:
            raise JsonpError("The [import] object requires the key 'file'.")
        if 'else' in options and 'if' not in options:
            raise JsonpError("The key 'else' of an [import] object requires the key 'if'.")
        self._check_import_path(options['file'], "The key 'file' of an [import] object")
        if 'else' in options:
            self._check_import_path(options['else'], "The key 'else' of an [import] object")
        condition = options.get('if')
        if isinstance(condition, (Obj, Arr, Bytes)) or isinstance(condition, Scalar) and not isinstance(condition.value, bool) \
                or isinstance(condition, Str) and condition.parts is None:
            raise JsonpError(f"The key 'if' of an [import] object requires a value of type 'bool', "
                             f"but the type is {self._literal_type(condition)}")
        optional = options.get('optional', Scalar(False))
        if not (isinstance(optional, Scalar) and isinstance(optional.value, bool)):
            raise JsonpError("The key 'optional' of an [import] object requires the literal value 'true' or 'false'.")
        return Import(options['file'], self.source, pos, condition, options.get('else'), optional.value)


class ImportExecutionMixin:
    """Imports which are resolved at runtime (part of Interpreter)."""

    def exec_import(self, imp: Import, target: dict, path: list):
        """Handles an import which could not be expanded before (dynamic path or condition)."""
        try:
            file = self.import_path(imp, path)
        except JsonpError:
            if self.lenient:
                return
            raise
        if self.lenient:
            self.resolved[self.resolver.key(imp)] = file
            return
        if file == SKIP:
            return
        imported = self.resolver.import_file(file, [imp.source.label], self.resolved)
        for member in imported.members:
            if isinstance(member, Member) and isinstance(member.key, str):
                target.pop(member.key, None)
        self.seed_object(imported, target, path)
        self.exec_object(imported, target, path)

    def import_path(self, imp: Import, path: list) -> str:
        """Path of the file to import; SKIP if nothing is imported."""
        node = imp.value
        if imp.condition is not None:
            try:
                condition = self.eval_node(imp.condition, path)
            except NotAvailable as error:
                raise JsonpError(f"Could not evaluate the condition of the [import] object. {error}")
            if not isinstance(condition, bool):
                raise JsonpError(f"The key 'if' of an [import] object requires a value of type 'bool', "
                                 f"but the type is {type_name(condition)}")
            if not condition:
                if imp.alternative is None:
                    return SKIP
                node = imp.alternative
        try:
            value = self.eval_node(node, path)
        except NotAvailable:
            text = node.text if isinstance(node, Str) else node.src
            params = regex.findall(rf'(\${{[^{regex.escape(_SPECIAL_CHARACTERS)}]+}}(\[.*\])*)', text)
            params = ''.join(f"{item[0]} " for item in params)
            raise JsonpError(f"Could not load the import file '{text}'. The parameter '{params}' is not available!")
        if not isinstance(value, str):
            raise JsonpError(f"The [import] key requires a value of type 'str', but the type is {type_name(value)}")
        file = self.resolver.dynamic_path(value, imp.source.base_dir)
        if imp.optional and not os.path.isfile(file):
            return SKIP
        return file


class ImportResolver:
    """Loads and parses JSONP sources and expands imports."""

    def __init__(self, python_syntax: bool, key_pattern: str):
        self.python_syntax = python_syntax
        self.key_pattern = key_pattern
        self._cache = {}

    # -- loading -----------------------------------------------------------------

    def parse(self, content: str, source: Source):
        """Parses comment free JSONP content."""
        from ..jsonp_parser import parse_jsonp     # local import: jsonp_parser depends on this module
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
                    elif path == SKIP or member.optional and not os.path.isfile(path):
                        continue
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
