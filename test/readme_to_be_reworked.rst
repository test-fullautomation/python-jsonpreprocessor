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

Component test of JsonPreprocessor
==================================

XC-CT/ECA3-Queckenstedt

17.07.2023

----

Table of content
----------------

`Execution`_

`Test case results`_

`Naming conventions`_

`Web application support`_

`Test case documentation`_

`List of test cases`_

----

Execution
---------

The component test is executed by the main test script ``component_test.py``.

This script executes a bunch of test cases that are configured in

.. code::

   testconfig/TestConfig.py

The JSON files used for testing, are placed in folder

.. code::

   testfiles

The log file of the test execution can be found here (default)

.. code::

   testlogfiles/JPP_SelfTest.log

It is possible to redirect the output with

.. code::

   component_test.py --logfile="<path and name of logfile>"

The path to the log file is created recursively. 

Per default all test cases defined in ``TestConfig.py``, are executed. Alternatively a single test case can
be choosed for execution by providing the test id (``TESTID``) in command line in the following way:

.. code::

   component_test.py --testid="<TESTID>"

The ``TESTID`` is part of the test case configuration in ``TestConfig.py``.

It is also possible to provide a semicolon separated list of TESTIDs:

.. code::

   component_test.py --testid="<TESTID1; TESTID2; TESTID3; ...>"

The execution of all test cases runs in a loop. The **JsonPreprocessor** class object is created (and deleted) outside this loop (default!).

Outcome: *All tests work with the same class object.*

With the (optional) command line switch ``--recreateinstance`` the **JsonPreprocessor** class object is created (and deleted) inside the loop.

Outcome: *All tests work with their own class object.*

Another possibility is available to execute the component test (under ``pytest`` conditions). This is
described in one of the next parts of this readme.

TOC_

----

Test case results
-----------------

The result of a single test case depends on the following topics:

* The values returned from **JsonPreprocessor** (like defined with ``EXPECTEDRETURN`` in ``TestConfig.py``)
* A thrown exception (like defined with ``EXPECTEDEXCEPTION`` in ``TestConfig.py``)

If both ``EXPECTEDRETURN`` and ``EXPECTEDEXCEPTION`` is defined with ``None``, the result of the test case will be ``UNKNOWN``.
But nevertheless the test case will be executed!

It is expected, that either values are returned from **JsonPreprocessor** or an exception is thrown.

If both is like expected, the result of the test case is ``PASSED``. In case of deviations between expected and returned content
the result of the test case is ``FAILED``.

The return value of ``component_test.py`` is 0 in case of all test cases are ``PASSED``, otherwise 1 (the return value
currently does not distinguish between FAILED and UNKNOWN). Only the result of a single test case can be ``UNKNOWN``.
The final result of the entire component test can only be either ``PASSED`` or ``FAILED``.

TOC_

----

Naming conventions
------------------

The configuration of a test case includes (beneath others) a ``TESTID``, a ``SECTION`` and a ``SUBSECTION`` (see
``TestConfig.py``).

The ``TESTID`` is a unique identifier for a test case and consists of a component specific prefix (to make
these id's much more unique also over all tested components) and a number. ``SECTION`` and ``SUBSECTION`` are
labels that are used to give a test case a more meaningful name. ``SECTION`` contains the name of the tested
feature; ``SUBSECTION`` is used to indicate a ``GOODCASE`` or a ``BADCASE`` test.

``TESTID``, ``SECTION`` and ``SUBSECTION`` are used together to define the names of test cases.

Example: The test case name of a ``GOODCASE`` test of the parameter substitution with ``TESTID`` ``JPP_0201`` is:

.. code::

   JPP_0201-(PARAMETER_SUBSTITUTION)-[GOODCASE]

With:

* ``JPP_0201`` is the ``TESTID``
* ``PARAMETER_SUBSTITUTION`` is the ``SECTION`` (*to ease the readability the* ``SECTION`` *is encapsulated in round brackets*)
* ``GOODCASE`` is the ``SUBSECTION`` (*to ease the readability the* ``SUBSECTION`` *is encapsulated in edged brackets*)

To ensure an unique look&feel of all names, the content of ``SECTION`` and ``SUBSECTION`` should be written in
capital letters only (with the underline as separator character).

TOC_

----


Web application support
-----------------------

Test results can be shown on a database supported web page. The software that is required to enable this, can be found here:

`https://github.com/test-fullautomation/testresultwebapp <https://github.com/test-fullautomation/testresultwebapp>`_

`https://github.com/test-fullautomation/python-pytestlog2db <https://github.com/test-fullautomation/python-pytestlog2db>`_ (``pytestlog2db.py``)

The ``testresultwebapp`` provides the web page (a so called dashboard displaying the results), ``pytestlog2db.py`` writes test results
created from Python ``pytest`` module into the database. Input is a certain result log file in XML format (like generated by ``pytest``).
Therefore we need the possibility to execute all test cases also under ``pytest`` conditions. This has no impact on the test execution, it's only required
to get this XML file in a format, that is required for ``pytestlog2db.py``.

This is realized in the following way:

With the command line option

.. code::

   --codedump

``component_test.py`` creates for every combination of ``SECTION`` and ``SUBSECTION`` a ``pytest`` file containing all test cases belonging to this
combination. Every test case inside these ``pytest`` files does nothing else than calling ``component_test.py`` with the ``TESTID`` of this test case.
Therefore the same code is executed, but because of the Python ``pytest`` module is involved now, we have an XML result log file in
``pytest`` format available. And this XML file can be computed by ``pytestlog2db.py``.

All automatically generated ``pytest`` code files can be found here:

.. code::

   pytest/pytestfiles

To execute these files this script can be used:

.. code::

   pytest/executepytest.py

Example

Call of a single test case in command line:

.. code::

   component_test.py --testid="JPP_0201"

Corresponding ``pytest`` file containing the call of this test:

.. code::

   pytest/pytestfiles/test_03_PARAMETER_SUBSTITUTION_GOODCASE.py

Class name inside the ``pytest`` file containing the call of this test:

.. code::

   class Test_PARAMETER_SUBSTITUTION_GOODCASE:

The test code itself:

.. code::

   def test_JPP_0201(self, Description):
      nReturn = CExecute.Execute("JPP_0201")
      assert nReturn == 0

The ``pytest`` XML log file can be found here:

.. code::

   pytest/logfiles/PyTestLog.xml

TOC_

----

Test case documentation
-----------------------

The configuration of every test case inside ``TestConfig.py`` includes a description and an expectation.

**Example**

.. code::

   dictUsecase['DESCRIPTION'] = "JSON file with nested parameter / string parameter substitution in parameter name"
   dictUsecase['EXPECTATION'] = "JsonPreprocessor creates a new string with all dollar operator expressions resolved as string"

The content is printed to console during every component test execution.

Additionally to this the command line option ``--codedump`` also generates out of all test case configurations several
test case overview lists in the following formats:

.. code::

   JPP_TestUsecases.csv
   JPP_TestUsecases.html
   JPP_TestUsecases.rst
   JPP_TestUsecases.txt

TOC_

----


List of test cases
------------------

A complete list of all implemented test cases can be found here:

`JPP_TestUsecases.html <https://htmlpreview.github.io/?https://github.com/test-fullautomation/python-jsonpreprocessor/blob/develop/test/JPP_TestUsecases.html>`_

TOC_


.. _TOC: `Table of content`_
