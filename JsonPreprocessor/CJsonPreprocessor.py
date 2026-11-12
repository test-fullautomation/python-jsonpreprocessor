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
# File: CJsonPreprocessor.py
#
# Public API of the JsonPreprocessor.
#
# The processing is split into the following layers:
#
#   common.py         shared definitions (syntax types, reserved tokens, key checker,
#                     comment removal, error type)
#   jsonp_parser.py   JSONP syntax: tokenizer/parser producing an AST (objects, arrays,
#                     literals, strings, [import] members, Python inline code, keys)
#   dollar_syntax.py  dollar operator syntax: recursive descent parser for ${...}
#                     expressions (nested references, dotted names, indices)
#   imports.py        loading of files and expansion of [import] members
#   inline_code.py    evaluation of Python inline code <<...>>
#   interpreter.py    evaluation of the AST (parameter store, references, dollar keys)
#
#################################################################################

import copy
import json
import os
import sys

import regex
from PythonExtensionsCollection.String.CString import CString
from pydotdict import DotDict

from JsonPreprocessor.version import VERSION, VERSION_DATE
from .common import (JsonpError, CSyntaxType, CNameMangling, CPythonJSONDecoder, CKeyChecker,  # noqa: F401
                     CTreeNode, CTextProcessor)
from .imports import ImportResolver, normalize_file_path, check_reserved_tokens, has_unresolved_imports
from .interpreter import Interpreter
from .jsonp_parser import Source


class CJsonPreprocessor():
    """
CJsonPreprocessor extends the JSON syntax by the following features:

* Allow c/c++-style comments within JSON files
* Allow to import JSON files into JSON files
* Allow to define and use parameters within JSON files
* Allow Python keywords ``True``, ``False`` and ``None``
    """

    def getVersion(self):
        """
Returns the version of JsonPreprocessor as string.
        """
        return VERSION

    def getVersionDate(self):
        """
Returns the version date of JsonPreprocessor as string.
        """
        return VERSION_DATE

    def __init__(self, syntax: CSyntaxType = CSyntaxType.python , current_cfg : dict = {}, key_pattern = r'.+') -> None:
        """
Constructor

**Arguments:**

* ``syntax`` (*CSyntaxType*) optional

  / *Condition*: optional / *Type*: CSyntaxType / *Default*: python /

  If set to ``python``, then Python data types are allowed as part of JSON file.

* ``current_cfg`` (*dict*) optional

  / *Condition*: optional / *Type*: dict / *Default*: {} /

  Used to update parameters from jsonp file to current JSON object.
        """
        if not isinstance(key_pattern, str):
            key_pattern_type = regex.search(r"('.+')>\s*$", str(type(key_pattern)))[1]
            raise Exception(f"The key pattern must be 'str' but received {key_pattern_type}!")
        elif key_pattern=='' or key_pattern=='.*':
            raise Exception(f"The key pattern '{key_pattern}' allows key names that are empty or contains only whitespace!")
        elif regex.match(r'^\s+$', key_pattern):
            raise Exception(f"The key pattern '{key_pattern}' just allows a key name that contains only whitespace!")
        self.key_pattern = key_pattern
        self.syntax      = syntax
        self.current_cfg = current_cfg

    def jsonLoad(self, json_file : str):
        """
This is a wrapper for the json_load() function.
        """
        return self.json_load(json_file)

    def json_load(self, json_file : str):
        """
This method is the entry point of JsonPreprocessor.

``json_load`` loads the JSON file, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``json_file``

  / *Condition*: required / *Type*: str /

  Path and name of main JSON file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

* ``json_obj``

  / *Type*: dict /

  Preprocessed JSON file(s) as Python dictionary
        """
        json_file = normalize_file_path(json_file)
        try:
            resolver = self.__create_resolver()
            tree = resolver.load_file(json_file)
            return self.__process(resolver, tree, json_file)
        except JsonpError as error:
            raise Exception(str(error)) from None

    def jsonLoads(self, jsonp_content : str, reference_dir : str = None):
        """
This is a wrapper for the json_loads() function.
        """
        return self.json_loads(jsonp_content, reference_dir)

    def json_loads(self, jsonp_content : str, reference_dir : str = None):
        """
``json_loads`` loads the JSONP content, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``jsonp_content``

  / *Condition*: required / *Type*: str /

  The JSONP content.

* ``reference_dir``

  / *Condition*: optional / *Type*: str / *Default*: None /

  A reference path for loading imported files.

**Returns:**

* ``json_obj``

  / *Type*: dict /

  Preprocessed JSON content as Python dictionary
        """
        if not isinstance(jsonp_content, str):
            raise Exception(f'Expected a string, but got a value of type {type(jsonp_content)}')
        base_dir = None
        if reference_dir is not None:
            base_dir = normalize_file_path(reference_dir)
            if not os.path.exists(base_dir):
                raise Exception(f"Reference directory '{reference_dir}' is not existing!")
        try:
            content = CTextProcessor.load_and_remove_comments(jsonp_content, is_file=False)
        except Exception as reason:
            raise Exception(f"Could not read JSONP content due to: '{reason}'!")
        try:
            check_reserved_tokens(content)
            resolver = self.__create_resolver()
            label = f"Root:{base_dir}"
            tree = resolver.parse(content, Source(None, base_dir, label))
            return self.__process(resolver, tree, label)
        except JsonpError as error:
            raise Exception(str(error)) from None

    def __create_resolver(self) -> ImportResolver:
        if self.syntax not in (CSyntaxType.python, CSyntaxType.json):
            raise JsonpError(f"Provided syntax '{self.syntax}' is not supported.")
        return ImportResolver(self.syntax == CSyntaxType.python, self.key_pattern)

    def __process(self, resolver: ImportResolver, tree, label: str):
        """
Expands the imports and evaluates the document. The paths of dynamic imports depend on
parameters, therefore they are determined by preliminary (lenient) evaluations until
all of them are known.
        """
        chain = [label]
        resolved = {}
        expanded = resolver.expand(tree, chain, resolved)
        while has_unresolved_imports(expanded):
            known = dict(resolved)
            try:
                Interpreter(resolver, copy.deepcopy(self.current_cfg), lenient=True, resolved=resolved).run(expanded)
            except Exception:
                pass
            if resolved == known:
                break
            expanded = resolver.expand(tree, chain, resolved)
        result = Interpreter(resolver, self.current_cfg, resolved=resolved).run(expanded)
        return DotDict(result) if isinstance(result, dict) else result

    def jsonDump(self, json_obj : dict, out_file : str) -> str:
        """
This is a wrapper for the json_dump() function.
        """
        return self.json_dump(json_obj, out_file)

    def json_dump(self, json_obj : dict, out_file : str) -> str:
        """
This method writes the content of a Python dictionary to a file in JSON format and returns a normalized path to this JSON file.

**Arguments:**

* ``json_obj``

  / *Condition*: required / *Type*: dict /

* ``out_file`` (*string*)

  / *Condition*: required / *Type*: str /

  Path and name of the JSON output file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

* ``out_file`` (*string*)

  / *Type*: str /

  Normalized path and name of the JSON output file.
        """
        out_file = CString.NormalizePath(out_file, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        json_obj = json.dumps(json_obj, ensure_ascii=False, indent=4)
        try:
            with open(out_file, "w", encoding='utf-8') as f:
                f.write(json_obj)
        except Exception as error:
            error_msg = f"Could not write a JSON file '{out_file}'! Reason: {error}"
            raise Exception(error_msg)

        return out_file
