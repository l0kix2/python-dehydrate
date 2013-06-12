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
Simple case
-----------
In simplest of possible cases you just want get object, list wanted attributes
and get mapping with keys based on attribute names and values from them.
Use ``dehydrate`` shortcut for this case.
>>> from dehydrate import dehydrate
>>> from examples import Person
>>> iron_man = Person(first_name='Tony', login='iron_man')
>>> dehydrated = dehydrate(obj=iron_man, fields=('first_name', 'login'))
>>> sorted(dehydrated.items())
[('first_name', 'Tony'), ('login', 'iron_man')]

* I use list representation of dict in examples because it has predictable
order of items in it.

But what if you want put ``first_name`` attribute in ``name`` key of resulted
dict? Just specify both strings in fields.
>>> from dehydrate import dehydrate
>>> from examples import Person
>>> iron_man = Person(first_name='Tony', login='iron_man')
>>> dehydrated = dehydrate(obj=iron_man, fields=(
...     ('first_name', 'name'),
...     'login',
... ))
>>> sorted(dehydrated.items())
[('login', 'iron_man'), ('name', 'Tony')]


Philosophy
==========
  * Easy things should be done easily.
  * Complex things must be possible.


Testing
=======
Test written with use of `pytest`_ library and neat `pytest pep8 plugin`_.
You should run ``python setup.py test`` for running full test suite or
``coverage run --source=dehydrate setup.py test`` for tests with coverage.
Tests automatically runs at `Travis CI`_. Examples in documentation are also
picked by test command.

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
