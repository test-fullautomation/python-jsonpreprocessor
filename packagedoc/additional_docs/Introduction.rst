.. Copyright 2020-2022 Robert Bosch GmbH

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

.. http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Json Preprocessor documentation
===============================

The JsonPreprocessor is a Python3 package which provides additional features for
JSON files.

These are:

* ability to (nested) import other JSON files. Users can create separate JSON files 
  and then import them to another JSON file.

* allow users using already defined parameters with ``${parameter}``-syntax in JSON files.

* overwrite already existing parameters with new values from later loaded json files.

* accept Python like ``True``, ``False`` and ``None``
  in JSON syntax. 

* provide the possibility to comment out parts of the JSON file content. This
  feature can be used to explain the meaning of parameters defined
  inside the JSON files.

The JsonPreprocessor returns as result a dictionary object of the deserialized 
preprocessed data.

