.. Copyright 2020-2023 Robert Bosch GmbH

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

.. http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Test Use Cases
==============

* **Test JPP_0001**

  [DATA_TYPES / GOODCASE]

   **JSON file with parameters of different data types (basic and composite)**

   Expected: All values are returned untouched, with their correct data types

----

* **Test JPP_0002**

  [DATA_TYPES / GOODCASE]

   **JSON file containing parameters with dollar operator syntax at right hand side of colon, basic data types**

   Expected: All parameters referenced by dollar operator are resolved correctly, with their correct data types

----

* **Test JPP_0100**

  [DATA_INTEGRITY / GOODCASE]

   **JSON file is empty (single pair of brackets only)**

   Expected: JsonPreprocessor returns empty dictionary

----

* **Test JPP_0101**

  [DATA_INTEGRITY / GOODCASE]

   **JSON file with string containing several separator characters and blanks; no parameters**

   Expected: String is returned unchanged

----

* **Test JPP_0102**

  [DATA_INTEGRITY / GOODCASE]

   **JSON file with string containing more special characters, masked special characters and escape sequences**

   Expected: String is returned unchanged (but with masked special characters and escape sequences resolved)

----

* **Test JPP_0200**

  [PARAMETER_SUBSTITUTION / GOODCASE]

   **JSON file with nested parameter / string parameter substitution in parameter value**

   Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string

----

* **Test JPP_0201**

  [PARAMETER_SUBSTITUTION / GOODCASE]

   **JSON file with nested parameter / string parameter substitution in parameter name**

   Expected: JsonPreprocessor creates a new string with all dollar operator expressions resolved as string

----

* **Test JPP_0250**

  [PARAMETER_SUBSTITUTION / BADCASE]

   **JSON file with nested parameter / string parameter substitution in parameter value / innermost parameter not existing**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0255**

  [PARAMETER_SUBSTITUTION / BADCASE]

   **JSON file with nested parameter / index parameter substitution in parameter value / dotdict notation / index parameter not existing**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0259**

  [PARAMETER_SUBSTITUTION / BADCASE]

   **JSON file with nested parameter / key parameter substitution in parameter value / dotdict notation / milestone number not existing**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0361**

  [VALUE_DETECTION / BADCASE]

   **JSON file with expression containing more closing elements '}' than opening elements '${' (invalid syntax 1)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

   *Hint: Checklist rule 3 / pattern 1*

----

* **Test JPP_0900**

  [COMMON_SYNTAX_VIOLATIONS / GOODCASE]

   **JSON file with syntax error, that is commented out**

   Expected: JsonPreprocessor returns remaining content of JSON file (valid parameters)

----

* **Test JPP_0950**

  [COMMON_SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (1)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0951**

  [COMMON_SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (2)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0952**

  [COMMON_SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (3)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0953**

  [COMMON_SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (4): file is completely empty**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0954**

  [COMMON_SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (5): file is empty (multiple pairs of brackets only)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

Generated: 08.08.2023 - 15:09:12

