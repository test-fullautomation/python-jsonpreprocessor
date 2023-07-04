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

* **Test JPP_0003**

  [DATA_TYPES / GOODCASE]

   **JSON file containing parameters with dollar operator syntax at right hand side of colon, composite data type: list**

   Expected: All parameters referenced by dollar operator are resolved correctly, with their correct data types

----

* **Test JPP_0004**

  [DATA_TYPES / GOODCASE]

   **JSON file containing parameters with dollar operator syntax at right hand side of colon, composite data type: dict**

   Expected: All parameters referenced by dollar operator are resolved correctly, with their correct data types

----

* **Test JPP_0005**

  [DATA_TYPES / GOODCASE]

   **JSON file with string values containing dollar operators**

   Expected: All parameters referenced by dollar operator are resolved correctly, outcome is a string containing the values of all referenced parameters

----

* **Test JPP_0100**

  [DATA_INTGRITY / GOODCASE]

   **JSON file is empty (single pair of brackets only)**

   Expected: JsonPreprocessor returns empty dictionary

----

* **Test JPP_0101**

  [DATA_INTGRITY / GOODCASE]

   **JSON file with string containing several separator characters and blanks; no parameters**

   Expected: String is returned unchanged

----

* **Test JPP_0102**

  [DATA_INTGRITY / GOODCASE]

   **JSON file with string containing more special characters, masked special characters and escape sequences**

   Expected: String is returned unchanged (but with masked special characters and escape sequences resolved)

----

* **Test JPP_0200**

  [PARAMETER_SUBSTITUTION / GOODCASE]

   **JSON file with composite string on right hand side of colon: parameters and hard coded string parts**

   Expected: JsonPreprocessor returns a string with parameter values resolved as string

----

* **Test JPP_0201**

  [PARAMETER_SUBSTITUTION / GOODCASE]

   **JSON file with composite string on left hand side of colon: parameters and hard coded string parts**

   Expected: JsonPreprocessor creates a parameter with parameter values resolved as string

----

* **Test JPP_0250**

  [PARAMETER_SUBSTITUTION / BADCASE]

   **JSON file with composite string on right hand side of colon: parameters and hard coded string parts; quotes around expression are missing**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0251**

  [PARAMETER_SUBSTITUTION / BADCASE]

   **JSON file with composite string on left hand side of colon: parameters and hard coded string parts; quotes around expression are missing**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0900**

  [SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (1)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0901**

  [SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (2)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0902**

  [SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (3)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0903**

  [SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (4): file is completely empty**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

* **Test JPP_0904**

  [SYNTAX_VIOLATIONS / BADCASE]

   **JSON file with syntax error (5): file is empty (multiple pairs of brackets only)**

   Expected: No values are returned, and JsonPreprocessor throws an exception

----

Generated: 04.07.2023 - 16:17:36

