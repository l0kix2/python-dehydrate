# coding: utf-8

# It's odd, but setuptools provide by distribute package.
from setuptools import setup, find_packages

setup(
    name='dehydrate',
    version='0.1dev',
    packages=find_packages(),
    tests_require=['pytest', 'mock']
)
