.. Copyright 2020-2022 Robert Bosch Car Multimedia GmbH

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

JSONPREPROCESSOR DOCUMENTATION
==============================

Getting Started
---------------

The JsonPreprocessor is a python3 package which allows programmers to handle  
additional features in json files such as comments, imports, overrides, etc. 
The json files containing comments, imports,... will be handled by the JsonPreprocessor 
package which returs as result an dictionary object of the deserialized data.

How to install
~~~~~~~~~~~~~~

Firstly, clone **python-jsonpreprocessor** repository to your machine.

Then go to python-jsonpreprocessor, using the 2 common commands below to build or install this package:

.. code-block::

    setup.py build      will build the package underneath 'build/'
    setup.py install    will install the package

After the build processes is completed, the package is located in 'build/', and the generated 
documents are located in 'doc/_build/'.

Features
--------

Adding comments to json file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The JsonPreprocessor allows adding comments into a json file, a comment can be added 
anywhere after **"//"**. 

**Note:** This package is not supporting multiline comments. Only single line comments
are possible. 

**Example:**

.. code-block::

   //*****************************************************************************
   //  Author: ROBFW-AIO Team
   //
   //  This file defines all common global parameters and will be included to all
   //  test config files
   //*****************************************************************************
   {
     "Project": "G3g",
     "WelcomeString": "Hello... ROBFW is running now!",
     // Version control information.
     "version": {
       "majorversion": "0",
       "minorversion": "1",
       "patchversion": "1"
     },
     "TargetName" : "gen3flex@dlt"
   }

Import other json files:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The import feature allows users to merge the content of other json files into a json 
file, it also allows nested importing, means we can use import feature again in imported 
files.

**Example:**

.. code-block::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
         //*****************************************************************************
         {
           "Project": "G3g",
           "WelcomeString": "Hello... ROBFW is running now!",
           // Version control information.
           "version": {
             "majorversion": "0",
             "minorversion": "1",
             "patchversion": "1"
           },
           "params": {
             // Global parameters
             "global": {
         		"[import]": "<path_to_the_imported_file>/params_global.json"
               }
             },
           "preprocessor": {
             "definitions": {
               // FEATURE switches
                 "[import]": "<path_to_the_imported_file>/preprocessor_definitions.json"
               }
           },
           "TargetName" : "gen3flex@dlt"
         }

Override, update and add new parameters:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package also allows to override, update and adding new parameters. 
User can update parameters which are already declared and add new parameters or new 
elements into existing parameters. The below example will show the way to use these features.

**Example:**

.. code-block::

         {
           "Project": "G3g",
           "WelcomeString": "Hello... ROBFW is running now!",
           // Version control information.
           "version": {
             "majorversion": "0",
             "minorversion": "1",
             "patchversion": "1"
           },
           "params": {
             // Global parameters
             "global": {
         		"[import]": "<path_to_the_imported_file>/params_global.json"
               }
             },
           "TargetName" : "gen3flex@dlt",
           // Override parameters
           "${params}['global']['gGlobalFloatParam']": 9.999,  
           "${version}['patchversion']": "2",
           "${params}['global']['gGlobalString']": "This is new string after overrided",
           // Add new parameters
           "${newParam}": {
         	  			"abc": 9,
         				"xyz": "new param"
           },
           "${params}['global']['gGlobalStructure']['newGlobalParam']": 123
         }

Nested parameters:
~~~~~~~~~~~~~~~~~~

With the JsonPreprocessor package, a user can also use nested parameters:

**Example:**

.. code-block::

         {
           "Project": "G3g",
           "WelcomeString": "Hello... ROBFW is running now!",
           // Version control information.
           "version": {
             "majorversion": "0",
             "minorversion": "1",
             "patchversion": "1"
           },
           "params": {
             // Global parameters
             "global": {
               "gGlobalIntParam" : 1,
               "gGlobalFloatParam" : 1.332, // This parameter is used to configure for ....
               "gGlobalString"   : "This is a string",
               "gGlobalStructure": {
                 "general": "general"
                 }
             }
           },
           "preprocessor": {
             "definitions": {
               "gPreprolIntParam" : 1,
               "gPreproFloatParam" : 9.664,
         	  "ABC": "checkABC",
               "gPreproString"   : "This is a string",
               "gPreproStructure": {
                                  "general": "general"
                                 }
             }
           },
           "TargetName" : "gen3flex@dlt",
           // Nested parameter
           "${params}['global'][${preprocessor}['definitions']['ABC']]": true,
           "${params}['global']['gGlobalFloatParam']": "${preprocessor}['definitions']['gPreproFloatParam']"
         }

Feedback
--------

To give us a feedback, you can send an email to `Thomas Pollerspöck <Thomas.Pollerspoeck@de.bosch.com>` 

In case you want to report a bug or request any interesting feature, please don't 
hesitate to raise a ticket.

Maintainers
~~~~~~~~~~~

`Thomas Pollerspöck <Thomas.Pollerspoeck@de.bosch.com>`_

Contributors
~~~~~~~~~~~~

`Mai Dinh Nam Son <son.maidinhnam@vn.bosch.com>`_

`Tran Duy Ngoan <Ngoan.TranDuy@vn.bosch.com>`_

License
-------

json-preprocessor is open source software provided under the `Apache License
2.0`__. 

__ http://apache.org/licenses/LICENSE-2.0