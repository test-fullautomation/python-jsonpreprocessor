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
# Package: extensions
#
# Extensions of the JSON syntax (except the dollar operator syntax, see
# dollar_syntax):
#
#   comments.py         C/C++ style comments
#   python_literals.py  Python literals True/False/None and byte values b'...'
#   inline_code.py      Python inline code <<...>>
#   imports.py          "[import]" and "[import?]" keys
#
# Each module contains the AST node, the scanner part (mixin of JsonpParser) and
# the evaluation part (mixin of Interpreter or evaluator) of its extension.
#
# Note: the package intentionally imports nothing to avoid import cycles.
#
#################################################################################
