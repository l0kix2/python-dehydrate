# coding: utf-8

import sys

# It's odd, but setuptools provide by distribute package.
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='dehydrate',
    version='0.1dev',
    packages=find_packages(),
    tests_require=['pytest', 'mock', 'coveralls'],
    cmdclass={'test': PyTest},
)
