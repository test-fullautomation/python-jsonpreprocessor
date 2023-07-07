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

How to install
--------------

**JsonPreprocessor** can be installed in two different ways.

1. Installation via PyPi (recommended for users)

   .. code::

      pip install JsonPreprocessor

   `JsonPreprocessor in PyPi <https://pypi.org/project/JsonPreprocessor/>`_

2. Installation via GitHub (recommended for developers)

   Clone the **JsonPreprocessor** repository to your machine.

   .. code::

      git clone https://github.com/test-fullautomation/python-jsonpreprocessor.git

   `JsonPreprocessor in GitHub <https://github.com/test-fullautomation/python-jsonpreprocessor>`_

   Use the following command to install **JsonPreprocessor**:

   .. code::

      setup.py install

Features
--------

Basic Json format
~~~~~~~~~~~~~~~~~

Users can use JsonPreprocessor to handle the json file with its original format.

**Example:**

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

Adding the comments
~~~~~~~~~~~~~~~~~~~

Often large projects require a lot of configuration parameters. So adding comments to json files is
useful in case of more and more content is added, e.g. because of a json file has to hold a huge number
of configuration parameters for different features. Comments can be used here to clarify the meaning of
these parameters or the differences between them.

Every line starting with **"//"**, is commented out. Therefore a comment is valid for singles lines only.

Comment out a block of several lines with only one start and one end comment string, is currently not supported.

**Example:**

.. code::

   //*****************************************************************************
   //  Author: ROBFW-AIO Team
   //
   //  This file defines all common global parameters and will be included to all
   //  test config files
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

Imports other json files
~~~~~~~~~~~~~~~~~~~~~~~~

This import feature enables developers to take over the content of other json files into the
current json file. A json file that is imported into another json file, can contain imports also
(allows nested imports).

A possible usecase for nested imports is to handle configuration parameters of different variants
of a feature or a component within a bunch of several smaller files, instead of putting all parameter
into only one large json file.

**Example:**

Suppose we have the json file ``params_global.json`` with the content:

.. code::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
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

And other json file ``preprocessor_definitions.json`` with content:

.. code::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
         //*****************************************************************************
         {
           "import_param_3" : "value_3",

           "import_param_4" : "value_4",

           // <adding comment>

           "import_structure_2": {
              "general": "general"
            }
         }

Then we can import these 2 files above to the json file ``config.json`` with the [import] statement:

.. code::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
         //*****************************************************************************
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
           "preprocessor": {
             "definitions": {
                 "[import]": "<path_to_the_imported_file>/preprocessor_definitions.json"
               }
           },
           "device" : "device_name"
         }

After all imports are resolved by the JsonPreprocessor, this is the resulting of data structure:

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

This JsonPreprocessor package also provides developers ability to add new as well as overwrite
existing parameters. Developers can update parameters which are already declared and add new
parameters or new element into existing parameters. The below example will show the way to do
these features.

In case we have many different variants, and each variant requires a different value assigned
to the parameter, users can use this feature to add new parameters and update new values for
existing parameters of existing configuation object.

**Example:**

Suppose we have the json file ``params_global.json`` with the content:

.. code::

         //*****************************************************************************
         //  Author: ROBFW-AIO Team
         //
         //  This file defines all common global parameters and will be included to all
         //  test config files
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

Then we import ``params_global.json`` to json file ``config.json`` with content:

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

Using defined parameters
~~~~~~~~~~~~~~~~~~~~~~~~

With JsonPreprocessor package, users can also use the defined parameters in Json file. The value of
the defined parameter could be called with syntax ``${<parameter_name>}``

**Example:**

Suppose we have the json file ``config.json`` with the content:

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

After all imports are resolved by the JsonPreprocessor, this is the resulting of data structure:

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

Accepted ``True``, ``False``, and ``None``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some keywords are different between Json and Python syntax:

* Json syntax: **``true``**, **``false``**, **``null``**

* Python syntax: **``True``**, **``False``**, **``None``**

To facilitate the usage of configuration files in Json format, both ways of syntax are accepted.

