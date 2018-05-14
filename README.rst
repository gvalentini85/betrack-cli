betrack
*******

.. image:: https://travis-ci.org/gvalentini85/betrack-cli.svg?branch=master
    :target: https://travis-ci.org/gvalentini85/betrack-cli
    :alt: Travis build status	     

.. image:: https://ci.appveyor.com/api/projects/status/x0h7p5o3f3r04m6a/branch/master?svg=true 
   :target: https://ci.appveyor.com/project/gvalentini85/betrack-cli
   :alt: Appveyor build status	 

.. image:: https://codecov.io/gh/gvalentini85/betrack-cli/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gvalentini85/betrack-cli
   :alt: Codecov coverage status

*A command line toolkit to automatically track collective behaviors.*

What follow is kept here temporary for reference and come from the skeleton
template skele-cli.

Installation
============

Documentation
=============

The documentation can be accessed online `here <https://gvalentini85.github.io/betrack-cli/>`_


HTML Format
-----------

Generate the documentation in *html* format::
  
    $ cd docs/
    $ sphinx-build -b html \source \build

PDF Format
----------

Generate the documentation in *pdf* format::
  
    $ cd docs/
    $ sphinx-build -b latex \source \build
    $ cd build/
    $ make

Examples
--------

Getting Help
------------

Copyright and Licensing
-----------------------


skele-cli
=========

*A skeleton command line program in Python.*



Usage
-----

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!
