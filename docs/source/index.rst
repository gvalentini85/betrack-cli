.. betrack documentation master file, created by
   sphinx-quickstart on Sun May 13 17:01:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#########
*betrack*
#########

.. image:: https://travis-ci.org/gvalentini85/betrack-cli.svg?branch=master
    :target: https://travis-ci.org/gvalentini85/betrack-cli
    :alt: Travis build status	     

.. image:: https://ci.appveyor.com/api/projects/status/x0h7p5o3f3r04m6a/branch/master?svg=true 
   :target: https://ci.appveyor.com/project/gvalentini85/betrack-cli
   :alt: Appveyor build status	 

.. image:: https://codecov.io/gh/gvalentini85/betrack-cli/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gvalentini85/betrack-cli
   :alt: Codecov coverage status


A major challenge in the study of collective animal behavior is to extract accurate
data from recordings of experiments, label them according to the identity of the involved
agents, and recognize the behaviors performed by these agents over time.

*betrack* aims to ease this challenge by providing a command line toolkit to support
all the necessary steps in the above workflow. Given a set of video recordings of
experiments performed in the same experimental setup, *betrack* allows to:

1. Track the identity and the position over time of agents.
   
2. Label behaviors and automatically exctract images to build a database of the
   labelled behaviors.
   
3. Train a deep learning classifier model based on a behavior database of labelled images.
   
4. Use a trained classifier model to track, in addition to the identity and to the position
   over time of agents, also the behavior that agents perform over time.
   
5. Customize the annotations shown in previously tracked videos with the aim to produce
   recordings suitable for research dissemination and scientific communication.

*betrack* is an open-source toolkit written in Python. It is cross-platform, developed
on OS X and currently tested using continuous integration on both linux and Windows.
*betrack* is compatible with both Python 2 (version 2.7) and Python 3 (versions 3.4, 3.5,
and 3.6) and is distributed under the terms of the MIT license (see `LICENSE
<https://github.com/gvalentini85/betrack-cli/blob/master/LICENSE>`_).

.. attention::

   *betrack* is currently under heavy development and most of its features are not yet
   available/implemented.

   As a rule of thumb, features that have been implemented and are available to the
   user are those already documented in this guide. That said, all available features
   are to be assumed as preliminary implementations and are largely untested.


.. toctree::
   :maxdepth: 2

   getstarted
   usage
   development

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
