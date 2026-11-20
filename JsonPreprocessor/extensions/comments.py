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
# File: extensions/comments.py
#
# JSON syntax extension: C/C++ style comments (// ... and /* ... */). Comments are
# removed from the text before parsing; quoted strings are kept unchanged.
#
#################################################################################

import regex

_COMMENT_PATTERN = regex.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
                                 regex.DOTALL | regex.MULTILINE)


def _replacer(match):
    s = match.group(0)
    return "" if s.startswith('/') else s


def remove_comments(content: str) -> str:
    """Removes all C/C++ style comments from JSONP content."""
    return regex.sub(_COMMENT_PATTERN, _replacer, content)
