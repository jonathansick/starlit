#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import glob
from setuptools import setup, find_packages

PACKAGENAME = "starlit"


def rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def get_version():
    with open(rel_path(os.path.join(PACKAGENAME, "__init__.py"))) as f:
        for line in f:
            if line.startswith("VERSION"):
                version = re.findall(r'\"(.+?)\"', line)[0]
                return version
    return "0.0.0.dev"


try:
    long_description = open(rel_path('README.rst'), 'rt').read()
except IOError:
    long_description = ''


extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


setup(
    name=PACKAGENAME,
    version=get_version(),
    author='Jonathan Sick',
    author_email='jonathansick@mac.com',
    license='MIT',
    description='Tools for working with astro literature databases',
    url='https://github.com/jonathansick/starlit',
    long_description=long_description,
    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'Topic :: Text Processing :: Markup :: LaTeX',
                 'Topic :: Scientific/Engineering :: Astronomy',
                 'License :: OSI Approved :: MIT License'],

    packages=find_packages(),
    package_data={PACKAGENAME: ['data/unicode.xml']},
    include_package_data=True,
    scripts=glob.glob(os.path.join('scripts', '*.py')),
    install_requires=['ads',
                      'bibtexparser',
                      'pymongo',
                      'xmltodict'],

    tests_require=['pytest',
                   'pytest-pep8',
                   'pytest-cov'],
    **extra
)
