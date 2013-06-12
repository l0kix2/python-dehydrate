python-dehydrate
================
.. image:: https://travis-ci.org/l0kix2/python-dehydrate.png?branch=master
    :target: https://travis-ci.org/l0kix2/python-dehydrate?branch=master

.. image:: https://coveralls.io/repos/l0kix2/python-dehydrate/badge.png?branch=master
    :target: https://coveralls.io/r/l0kix2/python-dehydrate?branch=master

Small lib for representing python objects as a dicts.


Motivation
==========
Why would you need library like this? One of obvious use cases is to prepare
data for serializing (into json/yaml/xml/pickle/whatever). You can control
dehydration process by describing how to fetch values from object and how to
present it in dehydrated structure using simple syntax.


Examples
========


Philosophy
==========
  * Easy things should be done easily.
  * Complex things must be possible.


Testing
=======
Test written with use of `pytest`_ library and neat `pytest pep8 plugin`_.
You should run ``python setup.py test`` for running full test suite or
``coverage run --source=dehydrate setup.py test`` for tests with coverage.
Tests automatically runs at `Travis CI`_.

.. _pytest: http://pytest.org/
.. _pytest pep8 plugin: https://pypi.python.org/pypi/pytest-pep8
.. _Travis CI: https://travis-ci.org/l0kix2/python-dehydrate?branch=master


Contribution
============
Any contribution is welcome. Use fork/pull request mechanism on github.

If you add some code, you should add some tests, so coverage of master branch
should always be 100%. Refer to Testing_ section for more instructions.

Let me speak from my heart :). I will be very glad, if you correct my clumsy
english phrases in docs and docstings or even advise more appropriate names
for variables in code.


TODO
====
  * Think about giving opportunity to put results in Ordered dict instead of
    simple dict.
  * Add functionality for converting all values of some type using handlers on
    dehydrator class.
