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

How to install
--------------

**JsonPreprocessor** can be installed in two different ways.

1. Installation via PyPi (recommended for users)

   .. code::

      pip install JsonPreprocessor

   `JsonPreprocessor in PyPi <https://pypi.org/project/JsonPreprocessor/>`_

2. Installation via GitHub (recommended for developers)

   Clone the **python-jsonpreprocessor** repository to your machine.

   .. code::

      git clone https://github.com/test-fullautomation/python-jsonpreprocessor.git

   `JsonPreprocessor in GitHub <https://github.com/test-fullautomation/python-jsonpreprocessor>`_

   Use the following command to install **JsonPreprocessor**:

   .. code::

      cd python-jsonpreprocessor
      setup.py install

JsonPreprocessor Features
-------------------------

Basic JSON format
~~~~~~~~~~~~~~~~~

Users can use JsonPreprocessor to handle any JSON file with its format as per JSON specification.

**Example**:

.. code::

   {
     "Project": "name_of_prject",
     "version": {
       "major": "0",
       "minor": "1",
       "patch": "1"
     },
     "params": {
       "global": {
         "param_1" : "value_1",
         "param_2" : value_2,
         "structure_param": {
           "general": "general"
         }
       }
     },
     "device" : "device_name"
   }

Adding comments
~~~~~~~~~~~~~~~~~~~

Often large projects require large JSON files. Comments can be used here to clarify the meaning of 
parameters or the differences between them.

Every line starting with **"//"**, is commented out. Therefore a comment is valid for singles lines only.

Comment out a block of several lines with only one start and one end comment string, is currently not supported.

**Example:**

.. code::

   //*****************************************************************************
   //  Author: Author_of_the_file
   //
   //  This file defines some paramters and will be included to other
   //  JSON files.
   //*****************************************************************************
   {
     "Project": "name_of_prject",
     // <adding comment>
     "version": {
       "majorversion": "0",
       "minorversion": "1",
       "patchversion": "1"
     },
     "params": {
       // <adding comment>
       "global": {
         "param_1" : "value_1",
         "param_2" : value_2,  // <adding comment>
         "structure_param": {
           "general": "general"
         }
       }
     },
     "device" : "device_name"
   }

Import other JSON files
~~~~~~~~~~~~~~~~~~~~~~~~

The import feature enables users to take over the content of another JSON file(s) into the 
current JSON file. A JSON file that is imported into another JSON file, can contain imports also
(nested imports).

A possible usecase for nested imports is to handle configuration parameters in a hierarchical way.
Parameters which belong together are defined in a separate JSON file and at the end inported to
a JSON file which brings parameters together.

This allows you to build up JSON files which are hierarchichally loaded, starting with
a default value which you overwrite with a later loaded JSON file.

**Example:**

Suppose we have the JSON file ``params_global.json`` with the content:

.. code::

         //*****************************************************************************
         //  Author: Author_of_the_file
         //
         //  This file defines all common global parameters and will be included to all
         //  configuration files
         //*****************************************************************************
         //
         //  This is to distinguish the different types of resets
         {
           "import_param_1" : "value_1",
         
           "import_param_2" : "value_2",
            
           "import_structure_1": {   // <adding comment>
             "general": "general"
           }
         }

And another JSON file ``preprocessor_definitions.json`` with the following content:

.. code::

         //*****************************************************************************
         //  Author: Author_of_the_file
         //
         //  This file defines all common global parameters and will be included to all
         //  configuration files
         //*****************************************************************************
         {
           "import_param_3" : "value_3",
           
           "import_param_4" : "value_4",

           // <adding comment>
            
           "import_structure_2": {
              "general": "general"
            }
         }

Now we can import the two files above into the JSON file ``config.json`` with the **``[import]``** statement:

.. code::

         //*****************************************************************************
         //  Author: Author_of_the_file
         //
         //  This file defines all common global parameters and will be included to all
         //  configuration files
         //*****************************************************************************
         {
           "Project": "name_of_project",
           "version": {
             "major": "0",
             "minor": "1",
             "patch": "1"
           },
           "params": {
             "global": {
                 "[import]": "<relative_path_to_the_imported_file>/params_global.json"
              }
            },
           "preprocessor": {
             "definitions": {
                 "[import]": "<relative_path_to_the_imported_file>/preprocessor_definitions.json"
               }
           },
           "device" : "device_name"
         }

After all imports are resolved by the JsonPreprocessor, this is the resulting data structure:

.. code::

         {
           "Project": "name_of_project",
           "version": {
             "major": "0",
             "minor": "1",
             "patch": "1"
           },
           "params": {
             "global": {
               "import_param_1" : "value_1",
               "import_param_2" : "value_2",
               "import_structure_1": {
                 "general": "general"
                 }
             }
           },
           "preprocessor": {
             "definitions": {
               "import_param_3" : "value_3",
               "import_param_4" : "value_4",
               "import_structure_2": {
                  "general": "general"
                }
             }
           },
           "device" : "device_name"
         }

Add new or overwrites existing parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JsonPreprocessor provides users the powerful possibility to add new as well as overwrite  
existing parameters. Developers can update parameters which are already declared and add new 
parameters or new elements into existing parameters. 

**Example:**

Suppose we have the JSON file ``params_global.json`` with the content:

.. code::

         //*****************************************************************************
         //  Author: Author_of_the_file
         //
         //  This file defines all common global parameters and will be included to all
         //  configuration files
         //*****************************************************************************
         //
         //  This is to distinguish the different types of resets
         {
           "import_param_1" : "value_1",
         
           "import_param_2" : "value_2",
            
           "import_structure_1": {   // <adding comment>
             "general": "general"
           }
         }

Then we import ``params_global.json`` to JSON file ``config.json`` with content:

.. code::

         {
           "Project": "name_of_prject",
           "version": {
             "major": "0",
             "minor": "1",
             "patch": "1"
           },
           "params": {
             "global": {
                 "[import]": "<path_to_the_imported_file>/params_global.json"
               }
             },
           "device" : "device_name",
           // Overwrite parameters
           "${params}['global']['import_param_1']": "new_value_1",  
           "${version}['patch']": "2",
           // Add new parameters
           "new_param": {
               "abc": 9,
               "xyz": "new param"
           },
           "${params}['global']['import_structure_1']['new_structure_param']": "new_structure_value"
         }

After all imports are resolved by the JsonPreprocessor, this is the resulting of data structure:

.. code::

         {
           "Project": "name_of_prject",
           "version": {
             "major": "0",
             "minor": "1",
             "patch": "2"
           },
           "params": {
             "global": {
               "import_param_1" : "new_value_1",
               "import_param_2" : "value_2",
               "import_structure_1": {
                 "general": "general",
                     "new_structure_param": "new_structure_value"
                }
              }
           },
           "device" : "device_name",
           "new_param": {
           "abc": 9,
           "xyz": "new param"
           }
         }

Using already defined parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JsonPreprocessor allows you to use the already defined parameters.  You can
refer to any already defined parameter by means of ``${<parameter_name>}``-syntax.

**Example:**

Suppose we have the JSON file ``config.json`` with the content:

.. code::json

         {
           "Project": "name_of_prject",
           "version": {
             "major": "0",
             "minor": "1",
             "patch": "1"
           },
           "params": {
             "global": {
               "import_param_1" : "value_1",
               "import_param_2" : "value_2",
               "import_structure_1": {
                 "general": "general"
                }
             }
           },
           "preprocessor": {
             "definitions": {
               "import_param_3" : "value_3",
               "import_param_4" : "value_4",
               "ABC": "param_ABC",
               "import_structure_1": {
                  "general": "general"
                }
             }
           },
           "device" : "device_name",
           // Using the defined parameters
           "${params}['global'][${preprocessor}['definitions']['ABC']]": True,
           "${params}['global']['import_param_1']": ${preprocessor}['definitions']['import_param_4']
         }

After all imports are resolved by  JsonPreprocessor, this is the resulting data structure:

.. code::

         {
           "Project": "name_of_prject",
           "version": {
             "major": "0",
             "minor": "1",
             "patch": "1"
           },
           "params": {
             "global": {
               "import_param_1" : "value_4",
               "import_param_2" : "value_2",
               "import_structure_1": {
                 "general": "general"
                 },
               "param_ABC": True
             }
           },
           "preprocessor": {
             "definitions": {
               "import_param_3" : "value_3",
               "import_param_4" : "value_4",
               "ABC": "param_ABC",
               "import_structure_1": {
                  "general": "general"
                }
             }
           },
           "TargetName" : "device_name"
         }

Python-like ``True``, ``False``, and ``None``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some keywords are different between JSON and Python syntax:

* JSON syntax: **``true``**, **``false``**, **``null``**

* Python syntax: **``True``**, **``False``**, **``None``**

JsonPreprocessor enables both ways of syntax.

