python-dehydrate
================
.. image:: https://travis-ci.org/l0kix2/python-dehydrate.svg?branch=v0.3.6
    :target: https://travis-ci.org/l0kix2/python-dehydrate

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
    >>> from pretend import stub as Person
    >>> iron_man = Person(first_name='Tony', login='iron_man')
    >>> dehydrated = dehydrate(obj=iron_man, specs=('first_name', 'login'))
    >>> sorted(dehydrated.items())
    [('first_name', 'Tony'), ('login', 'iron_man')]

Some notes:

- I use list representation of dict in examples because it has predictable
  order of items in it. It's important, because this pieces of code are tests.

If requested attribute name resolves to method of object, then result of
calling it will be set in dehydrated dict. In ``Person`` class we have method
``full_name``, so let's try to get its return value::

    >>> from dehydrate import dehydrate
    >>> from pretend import stub as Person
    >>> iron_man = Person(full_name=lambda: 'Tony Stark')
    >>> dehydrated = dehydrate(obj=iron_man, specs=('full_name',))
    >>> sorted(dehydrated.items())
    [('full_name', 'Tony Stark')]

But what if you want put ``first_name`` attribute in ``name`` key of resulted
dict? Just specify both strings in ``specs`` (*spec* can be one object or
two-tuple)::

    >>> from dehydrate import dehydrate
    >>> from pretend import stub as Person
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

    >>> from pretend import stub as Person
    >>> from examples import PersonDehydrator
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

Notes:

- In docs I will refer to ``examples`` package, which you can find in repo.


Recursive dehydration
---------------------
The most valuable feature of lib is that you can describe how to recursively
dehydrate complex fields on object::

    >>> from dehydrate import dehydrate, S
    >>> from pretend import stub as Person
    >>> from examples import PersonDehydrator
    >>> octopus = Person(login='octopus')
    >>> spider_man = Person(login='spidey', archenemy=octopus)
    >>> dehydrated = dehydrate(
    ...     specs=(
    ...         S('login'),
    ...         S(target='archenemy', type='nested', specs=(
    ...             S('login'),
    ...         )),
    ...     ),
    ...     obj=spider_man
    ... )
    >>> dehydrated['login']
    'spidey'
    >>> list(dehydrated['archenemy'].items())
    [('login', 'octopus')]

You can see, that specs for nested elements are described with use of
``dehydrate.S`` shortcut (And simple specs as well for the sake of sanity).
Acceptable arguments are for ``type='nested'``:

- ``target`` — name, that describes how to get value from object (or use hook
  on dehydrator)
- ``dehydrator`` — class, which can be used for dehydrating of complex target
  (``dehydrate.Dehydrator`` by default).
- ``specs`` — iterable of same structure as described above (it is optional
  in case if you describe specs on dehydrator class, but make good sense,
  if you ant use default ``Dehydrator`` class).


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
* Add comprehensive docs about everything.
* Move complex examples with classes into docs from readme.
* Write docstrings and auto-generate some additional docs.

