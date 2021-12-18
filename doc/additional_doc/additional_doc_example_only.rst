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

Json Preprocessor's Documentation
=================================

Section 1
---------

The *Json* Preprocessor is used to do **this** and **that**.

Section 2
---------

This is required *because of* ...

Nice picture:

.. image:: /images/DocTest.png
.. image:: /images/DocTest.jpg

Tables
------

Grid table

+---------------+-------------------+
| True          | True              |
+---------------+-------------------+
| False         | False             |
+---------------+-------------------+
| None          | None              |
+---------------+-------------------+

Simple table

=====  =====  ======
   Inputs     Output
------------  ------
  A      B    A or B
=====  =====  ======
False  False  False
True   False  True
False  True   True
True   True   True
=====  =====  ======


References
----------

For more information please refer to QuickRef_

.. _QuickRef: https://docutils.sourceforge.io/docs/user/rst/quickref.html

Back to `Section 1`_

Back to `Section 2`_

Back to `Tables`_


Text blocks
-----------

.. note:: (*directive*: ``note``; *box*: ``boxnote``) : Be noticed about ...

.. hint:: (*directive*: ``hint``; *box*: ``boxhint``) : Be informed about this hint ...

.. tip:: (*directive*: ``tip``; *box*: ``boxtip``) : Be informed about this tip ...


.. attention:: (*directive*: ``attention``; *box*: ``boxattention``) : Give attention to ...

.. caution:: (*directive*: ``caution``; *box*: ``boxcaution``) : Be careful with ...

.. important:: (*directive*: ``important``; *box*: ``boximportant``) : Urgently think about ...


.. danger:: (*directive*: ``danger``; *box*: ``boxdanger``) : Be aware of this danger ...

.. warning:: (*directive*: ``warning``; *box*: ``boxwarning``) : Be warned about ...

.. error:: (*directive*: ``error``; *box*: ``boxerror``) : You must not do this error ...


That's it.


Mathematics
-----------

Let's compute this:

.. math:: \clubsuit \cdot \sigma_\mathrm{mean} = \frac{\sigma}{\sqrt{N} \cdot 9^{\sqrt{9}}} \cdot \spadesuit

