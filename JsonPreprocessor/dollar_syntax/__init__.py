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
# Package: dollar_syntax
#
# Everything belonging to the dollar operator syntax (${...}):
#
#   parser.py       expression language: recursive descent parser for ${...}
#                   (nested references, dotted names, indices)
#   scanner.py      dollar operator expressions in the JSONP document: unquoted values,
#                   keys, strings with references (mixin of JsonpParser)
#   references.py   resolution of references against the parameter store
#                   (mixin of Interpreter)
#   dollar_keys.py  assignments with dollar keys ${...} : value (mixin of Interpreter)
#
# Note: the package intentionally imports nothing to avoid import cycles.
#
#################################################################################
