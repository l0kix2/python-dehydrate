# coding: utf-8

import sys

# It's odd, but setuptools provide by distribute package.
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--pep8',
            '--clearcache',
            '--doctest-glob=*.rst',
            # '--doctest-modules',
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


readme_text = open('README.rst').read()
changelog_text = open('CHANGELOG.rst').read()
setup(
    name='dehydrate',
    version='0.1.1',
    packages=['dehydrate'],
    url='https://github.com/l0kix2/python-dehydrate',
    license='MIT',
    author='Kirill Sibirev',
    author_email='l0kix2@gmail.com',
    description='Small lib for representing python objects as a dicts',
    long_description=readme_text + '\n\n' + changelog_text,
    setup_requires=['six'],
    tests_require=['pytest', 'mock', 'coverage', 'coveralls'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
