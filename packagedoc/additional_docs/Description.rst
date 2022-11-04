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

Getting Started
---------------

The JsonPreprocessor package is a Python3 package which allows developers to handle additional 
features in json files such as:

* Adds the comments
* Imports other json files
* Overwrites existing or add new parameters
* Uses nested parameter
* Other features

These json files will be handled by JsonPreprocessor package which returns as result a dictionary 
object of the deserialized data.

How to install
--------------

Firstly, clone `python-jsonpreprocessor <https://github.com/test-fullautomation/python-jsonpreprocessor>`_ 
repository to your machine.

Then go to python-jsonpreprocessor, using the 2 common commands below to build or install this package:

.. code-block::

    setup.py build      will build the package underneath 'build/'
    setup.py install    will install the package

After the build processes is completed, the package is located in 'build/', and the generated package 
documentation is located in **build/lib/JsonPreprocessor**.

We can use ``--help`` to discover the options for ``build`` command, example:

.. code-block:: bat

     setup.py build      will build the package underneath 'build/'
     setup.py install    will install the package
   
   Global options:
     --verbose (-v)      run verbosely (default)
     --quiet (-q)        run quietly (turns verbosity off)
     --dry-run (-n)      don't actually do anything
     --help (-h)         show detailed help message
     --no-user-cfg       ignore pydistutils.cfg in your home directory
     --command-packages  list of packages that provide distutils commands
   
   Information display options (just display information, ignore any commands)
     --help-commands     list all available commands
     --name              print package name
     --version (-V)      print package version
     --fullname          print <package name>-<version>
     --author            print the author's name
     --author-email      print the author's email address
     --maintainer        print the maintainer's name
     --maintainer-email  print the maintainer's email address
     --contact           print the maintainer's name if known, else the author's
     --contact-email     print the maintainer's email address if known, else the
                         author's
     --url               print the URL for this package
     --license           print the license of the package
     --licence           alias for --license
     --description       print the package description
     --long-description  print the long package description
     --platforms         print the list of platforms
     --classifiers       print the list of classifiers
     --keywords          print the list of keywords
     --provides          print the list of packages/modules provided
     --requires          print the list of packages/modules required
     --obsoletes         print the list of packages/modules made obsolete
   
   usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
      or: setup.py --help [cmd1 cmd2 ...]
      or: setup.py --help-commands
      or: setup.py cmd --help   

Features
--------

Adding the comments
~~~~~~~~~~~~~~~~~~~

With a big or a complex project, it requires a lot of configuration parameters. So adding comments to 
json files is useful in case of more and more content is added, e.g. because of a json file has to 
hold a huge number of configuration parameters for different features. Comments can be used here to 
clarify the meaning of these parameters or the differences between them.

Every line starting with **"//"**, is commented out. Therefore a comment is valid for singles lines only.

Comment out a block of several lines with only one start and one end comment string, is currently not supported.

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
         "gGlobalIntParam" : 1,
         "gGlobalFloatParam" : 1.332,  // This parameter is used to configure for ....
         "gGlobalString"   : "This is a string",
         "gGlobalStructure": {
           "general": "general"
         }
       }
     },
     "preprocessor": {
       "definitions": {
         // FEATURE switches
         "gPreprolIntParam" : 1,
         "gPreproFloatParam" : 1.332,
   	  // The parameter for feature ABC
         "gPreproString"   : "This is a string",
         "gPreproStructure": {
                            "general": "general"
                           }
         }
     },
     "TargetName" : "gen3flex@dlt"
   }

Imports other json files
~~~~~~~~~~~~~~~~~~~~~~~~

This import feature enables developers to take over the content of other json files into the 
current json file. A json file that is imported into another json file, can contain imports also
(allows nested imports).

A possible usecase for nested imports is to handle similar configuration parameters of different 
variants of a feature or a component within a bunch of several smaller files, instead of putting 
all parameter into only one large json file.

**Example:**

Suppose we have the json file ``params_global.json`` with the content:

.. code-block::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
         //*****************************************************************************
         //
         //  This is to distinguish the different types of resets
         {
           "gGlobalIntParam" : 1,
         
           "gGlobalFloatParam" : 1.332, // This parameter is used to configure for ....
           
           "gGlobalString"   : "This is a string",
            
           "gGlobalStructure": {
             "general": "general"
           }
         }

And other json file ``preprocessor_definitions.json`` with content:

.. code-block::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
         //*****************************************************************************
         {
           "gPreprolIntParam" : 1,
           
           "gPreproFloatParam" : 1.332,
           // The parameter for feature ABC
           "gPreproString"   : "This is a string",
            
           "gPreproStructure": {
                                  "general": "general"
                               }
         }

Then we can import these 2 files above to the json file ``config.json`` with content:

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

The ``config.json`` file is handled by JsonPreprocessor package, then return the dictionary 
object for a program like below:

.. code-block::

         {
           "Project": "G3g",
           "WelcomeString": "Hello... ROBFW is running now!",
           "version": {
             "majorversion": "0",
             "minorversion": "1",
             "patchversion": "1"
           },
           "params": {
             "global": {
               "gGlobalIntParam" : 1,
               "gGlobalFloatParam" : 1.332,
               "gGlobalString"   : "This is a string",
               "gGlobalStructure": {
                 "general": "general"
                 }
             }
           },
           "preprocessor": {
             "definitions": {
               "gPreprolIntParam" : 1,
               "gPreproFloatParam" : 1.332,
               "gPreproString"   : "This is a string",
               "gPreproStructure": {
                                  "general": "general"
                                 }
             }
           },
           "TargetName" : "gen3flex@dlt"
         }

Overwrites existing or add new parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This JsonPreprocessor package also provides developers ability to overwrite or update as well as  
add new parameters. Developers can update parameters which are already declared and add new 
parameters or new element into existing parameters. The below example will show the way to do 
these features.

In case we have many different variants, and each variant requires a different value assigned 
to the parameter. This feature could help us update new value for existing parameters, it also 
supports to add new parameters to existing configuation object.

**Example:**

Suppose we have the json file ``params_global.json`` with the content:

.. code-block::

         {
           "gGlobalIntParam" : 1,
         
           "gGlobalFloatParam" : 1.332, // This parameter is used to configure for ....
           
           "gGlobalString"   : "This is a string",
            
           "gGlobalStructure": {
             "general": "general"
           }
         }

Then we import ``params_global.json`` to json file ``config.json`` with content:

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
           // Overwrite parameters
           "${params}['global']['gGlobalFloatParam']": 9.999,  
           "${version}['patchversion']": "2",
           "${params}['global']['gGlobalString']": "This is the new value for the already existing parameter.",
           // Add new parameters
           "${newParam}": {
         	  			"abc": 9,
         				"xyz": "new param"
           },
           "${params}['global']['gGlobalStructure']['newGlobalParam']": 123
         }

The ``config.json`` file is handled by JsonPreprocessor package, then return the dictionary object 
for a program like below:

.. code-block::

         {
           "Project": "G3g",
           "WelcomeString": "Hello... ROBFW is running now!",
           "version": {
             "majorversion": "0",
             "minorversion": "1",
             "patchversion": "2"
           },
           "params": {
             "global": {
               "gGlobalIntParam" : 1,
               "gGlobalFloatParam" : 9.999,
               "gGlobalString"   : "This is the new value for the already existing parameter.",
               "gGlobalStructure": {
                 "general": "general",
         		"newGlobalParam": 123
                 }
               }
           },
           "TargetName": "gen3flex@dlt",
           "newParam": {
         	  "abc": 9,
         	  "xyz": "new param"
           }
         }

Uses nested parameter
~~~~~~~~~~~~~~~~~~~~~

With JsonPreprocessor package, user can also use nested parameters as example below:

**Example:**

Suppose we have the json file ``config.json`` with the content:

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
           "${params}['global']['gGlobalFloatParam']": ${preprocessor}['definitions']['gPreproFloatParam']
         }

The ``config.json`` file is handled by JsonPreprocessor package, then return the dictionary object 
for a program like below:

.. code-block::

         {
           "Project": "G3g",
           "WelcomeString": "Hello... ROBFW is running now!",
           "version": {
             "majorversion": "0",
             "minorversion": "1",
             "patchversion": "1"
           },
           "params": {
             "global": {
               "gGlobalIntParam" : 1,
               "gGlobalFloatParam" : 9.664,
               "gGlobalString"   : "This is a string",
               "gGlobalStructure": {
                 "general": "general"
                 },
         	  "checkABC": true
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
           "TargetName" : "gen3flex@dlt"
         }

Other features
~~~~~~~~~~~~~~

To facilitate the json usage, the Python data types such as **``True``**, **``False``**, and 
**``None``** will be accepted as json syntax elements while using JsonPreprocessor package.

