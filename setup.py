#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from betrack import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        print("RunTests:run")
        errno = call(['pytest', '--cov', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'betrack',
    version = __version__,
    description = 'A Python command line toolkit to track collective behaviors.',
    long_description = long_description,
    url = 'https://github.com/gvalentini85/betrack-cli',
    author = 'Gabriele Valentini',
    author_email = 'gvalent3@asu.edu',
    license = 'MIT',
    classifiers = [
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'pyyaml', 'pims', 'trackpy'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov', 'codecov'],
    },
    entry_points = {
        'console_scripts': [
            'betrack=betrack.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
