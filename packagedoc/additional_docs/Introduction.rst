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

**This is the documentation for Python JsonPreprocessor**

Json is a format used to represent data and becomes the universal standard of data 
exchange. Today many software projects are using configuration file in Json format. 
For a big or a complex project there is a need to have some enhanced format in Json 
file such as adding the comments, importing other Json files, etc.

Based on that needs, we develop JsonPreprocessor package: 

* Gives the possibility to comment out parts of the content. This feature can be used to 
  explain the meaning of the parameters defined inside the configuration files.

* Has ability to import other Json files. This feature can be applied for complex project,
  users can create separated Json files then importing them to other Json file.

* Allows users using the defined parameter in Json file. 

* Accepts **``True``**, **``False``**, and **``None``** in Json syntax

.. image:: ./pictures/python3-jsonpreprocessor.png
