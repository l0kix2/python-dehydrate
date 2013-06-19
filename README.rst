python-dehydrate
================
.. image:: https://travis-ci.org/l0kix2/python-dehydrate.png?branch=master
    :target: https://travis-ci.org/l0kix2/python-dehydrate?branch=master

.. image:: https://coveralls.io/repos/l0kix2/python-dehydrate/badge.png?branch=master
    :target: https://coveralls.io/r/l0kix2/python-dehydrate?branch=master

Small lib for representing python objects as a dicts.


Motivation
==========
Why would you need library like this? One of obvious use cases is to convert
complex objects with methods, lots of atributes and so on into dicts for
serializing (into json/yaml/xml/pickle/whatever). You can control
dehydration process by describing how to fetch values from object and how to
present it in dehydrated structure using simple syntax.


Examples
========
Simple cases
------------
In simplest of possible cases you just want get object, list wanted attributes
and get mapping with keys based on attribute names and values from them.
Use ``dehydrate`` shortcut for this case::

    >>> from dehydrate import dehydrate
    >>> from examples import Person
    >>> iron_man = Person(first_name='Tony', login='iron_man')
    >>> dehydrated = dehydrate(obj=iron_man, specs=('first_name', 'login'))
    >>> sorted(dehydrated.items())
    [('first_name', 'Tony'), ('login', 'iron_man')]

Some notes:

- I use list representation of dict in examples because it has predictable
  order of items in it. It's important, because this pieces of code are tests.
- In docs I will refer to ``examples`` package, which you can find in repo.

If requested attribute name resolves to method of object, then result of
calling it will be set in dehydrated dict. In ``Person`` class we have method
``full_name``, so let's try to get its return value::

    >>> from dehydrate import dehydrate
    >>> from examples import Person
    >>> iron_man = Person(first_name='Tony', last_name='Stark')
    >>> dehydrated = dehydrate(obj=iron_man, specs=('full_name',))
    >>> sorted(dehydrated.items())
    [('full_name', 'Tony Stark')]

But what if you want put ``first_name`` attribute in ``name`` key of resulted
dict? Just specify both strings in ``specs`` (*spec* can be one object or
two-tuple)::

    >>> from dehydrate import dehydrate
    >>> from examples import Person
    >>> iron_man = Person(first_name='Tony', login='iron_man')
    >>> dehydrated = dehydrate(obj=iron_man, specs=(
    ...     ('first_name', 'name'),
    ...     'login',
    ... ))
    >>> sorted(dehydrated.items())
    [('login', 'iron_man'), ('name', 'Tony')]

Second argument always be used as a key if exists in spec.


More complex cases
------------------
Sometimes you will want to add some value in dehydrated dict, which is not
attribute of dehydrated object. Or you may want not use attribute and add some
another handling for this element instead. In our example we creating
special class for this called ``PersonDehydrator`` (inherited from
``dehydrate.Dehydrator``) and set some methods on it::

    >>> from examples import Person, PersonDehydrator
    >>> iron_man = Person(password='iRon42', login='iron_man')
    >>> dehydrated = PersonDehydrator(specs=(
    ...     'password',
    ...     ('superhero_status', 'is_superhero'),
    ... )).dehydrate(obj=iron_man)
    >>> sorted(dehydrated.items())
    [('is_superhero', True), ('password', '******')]

In example you can see, that object has ``password`` attribute, but
``PersonDehydrator``'s ``get_password`` used for ``password`` spec. Also you can
mention, that result of calling ``get_superhero_status`` was set in key
``is_superhero`` because of second item in spec was declared.
You can declare ``specs`` using attribute of dehydrator class
or by passing argument into its ``__init__`` method.


Recursive dehydration
---------------------
The most valuable feature of lib is that you can describe how to recursively
dehydrate complex fields on object::

    >>> from dehydrate import dehydrate
    >>> from examples import Person, PersonDehydrator
    >>> octopus = Person(login='octopus')
    >>> spider_man = Person(login='spidey', archenemy=octopus)
    >>> dehydrated = dehydrate(
    ...     specs=(
    ...         'login',
    ...         {'target': 'archenemy', 'specs': ('login',)}
    ...     ),
    ...     obj=spider_man
    ... )
    >>> dehydrated['login']
    'spidey'
    >>> list(dehydrated['archenemy'].items())
    [('login', 'octopus')]

Second spec in ``specs`` is so-called ``ComplexSpec``, it described by
mapping with one required key ``target``, which describes how to get value for
serialization. Other acceptable keys are:

- ``dehydrator`` — class, which can be used for dehydrating of complex target.
- ``specs`` — iterable of same structure as described above.
- ``iterable`` — flag, which specifies should target be handled as iterable.


Installation
============
Simple::

 pip install dehydrate

must be fine.

Requirements
------------
* six (did I mentioned python 3 support? We have one.)


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
* Review tests, because now they not very maintainable. Use sane examples like
  in readme.
* Add comprehensive docs about everything.
* Maybe move complex examples with classes into docs from readme.
