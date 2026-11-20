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
# File: nodes.py
#
# AST nodes of the JSON core syntax. The nodes of the syntax extensions are defined
# in their modules:
#
#   dollar_syntax/scanner.py        Bare, DollarKey
#   extensions/inline_code.py       Inline
#   extensions/imports.py           Import
#   extensions/python_literals.py   Bytes
#
#################################################################################

from dataclasses import dataclass, field
from typing import Optional

from .dollar_syntax.parser import Template


@dataclass(frozen=True)
class Source:
    """A parsed JSONP source (file or content)."""
    path: Optional[str]         # normalized file path, None for content
    base_dir: Optional[str]     # reference directory for relative imports
    label: str                  # identification within the import chain


@dataclass(eq=False)
class Scalar:
    value: object


@dataclass(eq=False)
class Str:
    text: str
    parts: Optional[Template] = None    # set if the string contains references
    escape_text: bool = False


@dataclass(eq=False)
class Arr:
    items: list


@dataclass(eq=False)
class Member:
    key: object                 # str (literal key) or DollarKey
    value: object
    origin: str = None          # path of the imported file the member comes from (None: current file)


@dataclass(eq=False)
class Obj:
    members: list = field(default_factory=list)     # Member | Import


def is_pure_literal(node) -> bool:
    """True if the value of the node does not depend on anything."""
    if isinstance(node, Scalar):
        return True
    if isinstance(node, Str):
        return node.parts is None
    return False
