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

**This is the documentation for jsonpreprocessor repository**

Getting Started
---------------

The JsonPreprocessor is the python3 package which allows programmer to handle some 
additional features in json file such as comment, import, override, etc for configuring 
purpose. The json file containing comment, import,... will be handled by JsonPreprocessor 
package then returned the final dictionary object for python program.

How to install
~~~~~~~~~~~~~~

Firstly, clone **python-jsonpreprocessor** repository to your machine.

Then go to python-jsonpreprocessor, using the 2 common commands below to build or install this package:

.. code-block::

    setup.py build      will build the package underneath 'build/'
    setup.py install    will install the package

We can use --help to discover the options for 'build' command, ex:

.. code-block::

    python setup.py --help build
    ...
    Global options:
      --verbose (-v)  run verbosely (default)
      --quiet (-q)    run quietly (turns verbosity off)
      --dry-run (-n)  don't actually do anything
      --help (-h)     show detailed help message
      --no-user-cfg   ignore pydistutils.cfg in your home directory
    
    Options for 'build' command:
      --build-base (-b)  base directory for build library
      --build-purelib    build directory for platform-neutral distributions
      --build-platlib    build directory for platform-specific distributions
      --build-lib        build directory for all distribution (defaults to either
                         build-purelib or build-platlib
      --build-scripts    build directory for scripts
      --build-temp (-t)  temporary build directory
      --plat-name (-p)   platform name to build for, if supported (default: win-
                         amd64)
      --compiler (-c)    specify the compiler type
      --parallel (-j)    number of parallel build jobs
      --debug (-g)       compile extensions and libraries with debugging
                         information
      --force (-f)       forcibly build everything (ignore file timestamps)
      --executable (-e)  specify final destination interpreter path (build.py)
      --help-compiler    list available compilers
    
    usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
       or: setup.py --help [cmd1 cmd2 ...]
       or: setup.py --help-commands
       or: setup.py cmd --help

After the build processes are completed, the package is located in 'build/', and the documents are 
located in 'doc/_build/'.

Features
--------

Adding comments in json file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The JsonPreprocessor allows adding comments into json file, a comment could be added 
follow **"//"**.

**Note:** This package is not allow commented a block of json code, each comment must 
be added with **"//"**.

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

Imported the other json files:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This import feature allows user merges the content of other json files into the json 
file, it also allows the nested importing means we can use import feature in the imported 
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

Override, add new parameters:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package also provides user ability to override or update as well as add new parameters. 
User can update parameters which are already declared and add new parameters or new 
element into existing parameters. The below example will show the way to do these features.

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

With JsonPreprocessor package, user can also use nested parameters as example below:

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

To give us a feedback, you can send an email to `Thomas Pollerspöck <Thomas.Pollerspoeck@de.bosch.com>`_ 

In case you want to report a bug or request any interesting feature, please don't 
hesitate to raise a ticket.

About
-----

Maintainers
~~~~~~~~~~~

`Thomas Pollerspöck`_

Contributors
~~~~~~~~~~~~

`Mai Dinh Nam Son`_

`Tran Duy Ngoan`_

`Nguyen Huynh Tri Cuong`_

`Tran Hoang Nguyen`_

`Holger Queckenstedt`_

License
-------

json-preprocessor is open source software provided under the `Apache License
2.0`__. 

__ http://apache.org/licenses/LICENSE-2.0