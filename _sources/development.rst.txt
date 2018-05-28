***********
Development
***********


Requirements
============

In order to modify or contribute to the source code of *betrack* you
must first install the following softwares:

* `Python <https://www.python.org/downloads/>`_
  
* `pip <https://pip.pypa.io/en/stable/installing/>`_

* `git <https://git-scm.com/book/en/v1/Getting-Started-Installing-Git>`_

* `sphinx <http://www.sphinx-doc.org/en/stable/install.html>`_

  

Editable Installation
=====================

If you are planning to modify or contribute to the development of *betrack*,
you want to clone the `GitHub repository <https://github.com/gvalentini85/betrack-cli>`_
and install *betrack* (*and all development dependencies*) from source in
editable mode. By doing so, changes made to the source code of *betrack* will
be immediately available to use wherever *betrack* is installed on your system.

To clone and install *betrack* in editable mode issue the following commands
in a terminal:

.. code-block:: bash

   $ git clone https://github.com/gvalentini85/betrack-cli.git
   $ pip install -e .[test]
   

Testing
=======

*betrack* is unit-tested using `pytest <http://pytest.org/latest/>`_. Information
about code coverage is collected using the
`pytest coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin and is available
online using `codecov <https://codecov.io/gh/gvalentini85/betrack-cli>`_ (Current
status: |COV|).

.. |COV| image:: https://codecov.io/gh/gvalentini85/betrack-cli/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gvalentini85/betrack-cli
   :alt: Codecov coverage status

If you'd like to run all tests for this project, you want to issue the
following command in a terminal:

.. code-block:: bash

    $ python setup.py test

.. note: The codecov plugin is automatically triggered on Travis!

Generate Documentation
======================

*betrack* is documented using `sphinx <http://www.sphinx-doc.org/>`_ and its
documentation is hosted on `GitHub pages <https://gvalentini85.github.io/betrack-cli/>`_.

.. note::
   
   To generate the documentation of *betrack* you need to `install sphinx
   <http://www.sphinx-doc.org/en/stable/install.html>`_!

The documentation can be generated in *html* format by navigating in the
`docs/` folder and issuing the proper `sphinx-build` command:

.. code-block:: bash
  
    $ cd docs/
    $ sphinx-build -b html \source \build

Alternatively, the following code generates the documentation in *pdf* format:

.. code-block:: bash
  
    $ cd docs/
    $ sphinx-build -b latex \source \build
    $ cd build/
    $ make

Deploy to PyPI
==============

.. warning:: This information is not yet tested! Copy and pasted from `skele`
	     

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
    
    
API Documentation
=================

.. automodule:: betrack.cli

betrack.commands
----------------

* :py:mod:`betrack.commands.command`

  * :py:class:`~betrack.commands.command.BetrackCommand`

    * :py:func:`~betrack.commands.command.BetrackCommand.__init__`

    * :py:func:`~betrack.commands.command.BetrackCommand.run`

* :py:mod:`betrack.commands.annotatevideo`

  * :py:class:`~betrack.commands.annotatevideo.AnnotateVideo`

    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.__init__`

    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.configure_annotator`
      
    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.draw_particles`
      
    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.draw_region`
      
    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.draw_frame_number`
      
    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.annotator`
      
    * :py:func:`~betrack.commands.annotatevideo.AnnotateVideo.run`

* :py:mod:`betrack.commands.trackbehaviors`
    
* :py:mod:`betrack.commands.trackparticles`

  * :py:class:`~betrack.commands.trackparticles.TrackParticles`

    * :py:func:`~betrack.commands.trackparticles.TrackParticles.__init__`

    * :py:func:`~betrack.commands.trackparticles.TrackParticles.configure_tracker`
      
    * :py:func:`~betrack.commands.trackparticles.TrackParticles.locate_features`
      
    * :py:func:`~betrack.commands.trackparticles.TrackParticles.link_trajectories`
      
    * :py:func:`~betrack.commands.trackparticles.TrackParticles.filter_trajectories`
      
    * :py:func:`~betrack.commands.trackparticles.TrackParticles.export_video`
      
    * :py:func:`~betrack.commands.trackparticles.TrackParticles.run`
      
* :py:mod:`betrack.commands.trainclassifier`
  
* :py:mod:`betrack.commands.samplebehaviors`
  

command
^^^^^^^

.. automodule:: betrack.commands.command

    .. autoclass:: betrack.commands.command.BetrackCommand

        .. automethod:: betrack.commands.command.BetrackCommand.__init__

        .. automethod:: betrack.commands.command.BetrackCommand.run
			

annotatevideo
^^^^^^^^^^^^^

.. automodule:: betrack.commands.annotatevideo

    .. autoclass:: betrack.commands.annotatevideo.AnnotateVideo

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.__init__

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.configure_annotator

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.draw_particles

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.draw_region

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.draw_frame_number
			
        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.annotator
			
        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.run
			

trackparticles
^^^^^^^^^^^^^^

.. automodule:: betrack.commands.trackparticles

    .. autoclass:: betrack.commands.trackparticles.TrackParticles

        .. automethod:: betrack.commands.trackparticles.TrackParticles.__init__

        .. automethod:: betrack.commands.trackparticles.TrackParticles.configure_tracker
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.locate_features
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.link_trajectories
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.filter_trajectories
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.export_video
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.run
			
			
betrack.utils
-------------

The module :py:mod:`betrack.utils` is a collection of modules that provide
utilities functions useful across all commands of *betrack*.

These modules and their classes/functions are:

* :py:mod:`betrack.utils.frames`

  * :py:func:`~betrack.utils.frames.as_gray`
    
  * :py:func:`~betrack.utils.frames.crop`

  * :py:func:`~betrack.utils.frames.flip`
    
  * :py:func:`~betrack.utils.frames.invert_colors`
    
  * :py:func:`~betrack.utils.frames.reverse_colors`

* :py:mod:`betrack.utils.job`

  * :py:class:`~betrack.utils.job.Job`

    * :py:func:`~betrack.utils.job.Job.__init__`

    * :py:func:`~betrack.utils.job.Job.str`

    * :py:func:`~betrack.utils.job.Job.load_frames`

    * :py:func:`~betrack.utils.job.Job.release_memory`

    * :py:func:`~betrack.utils.job.Job.export_trajectories`

    * :py:func:`~betrack.utils.job.Job.valid_margins`			
			
    * :py:func:`~betrack.utils.job.Job.preprocess_video`

  * :py:func:`~betrack.utils.job.configure_jobs`
       
* :py:mod:`betrack.utils.message`

  * :py:class:`~betrack.utils.message.Message`
		   
  * :py:func:`~betrack.utils.message.mprint`
		    
  * :py:func:`~betrack.utils.message.wprint`
		    
  * :py:func:`~betrack.utils.message.eprint`			

* :py:mod:`betrack.utils.parser`

  * :py:func:`~betrack.utils.parser.open_configuration`
		    
  * :py:func:`~betrack.utils.parser.parse_file`
		    
  * :py:func:`~betrack.utils.parser.parse_directory`
		    
  * :py:func:`~betrack.utils.parser.parse_int`
		    
  * :py:func:`~betrack.utils.parser.parse_float`
		    
  * :py:func:`~betrack.utils.parser.parse_int_or_float`
		    
  * :py:func:`~betrack.utils.parser.parse_bool`
		    
  * :py:func:`~betrack.utils.parser.parse_str`


frames
^^^^^^

.. automodule:: betrack.utils.frames
    :members:
		
    .. autofunction:: betrack.utils.frames.as_gray(frame)
		
    .. autofunction:: betrack.utils.frames.crop
		
    .. autofunction:: betrack.utils.frames.flip
		
    .. autofunction:: betrack.utils.frames.invert_colors
		
    .. autofunction:: betrack.utils.frames.reverse_colors
		   		   

job
^^^

.. automodule:: betrack.utils.job

    .. autoclass:: betrack.utils.job.Job

        .. automethod:: betrack.utils.job.Job.__init__

        .. automethod:: betrack.utils.job.Job.str

        .. automethod:: betrack.utils.job.Job.load_frames

        .. automethod:: betrack.utils.job.Job.release_memory

        .. automethod:: betrack.utils.job.Job.export_trajectories

        .. automethod:: betrack.utils.job.Job.valid_margins			
			
        .. automethod:: betrack.utils.job.Job.preprocess_video

    .. autofunction:: betrack.utils.job.configure_jobs			
			
			
message
^^^^^^^

.. automodule:: betrack.utils.message

    .. autoclass:: betrack.utils.message.Message
		   
    .. autofunction:: betrack.utils.message.mprint
		    
    .. autofunction:: betrack.utils.message.wprint
		    
    .. autofunction:: betrack.utils.message.eprint			


parser
^^^^^^

.. automodule:: betrack.utils.parser

    .. autofunction:: betrack.utils.parser.open_configuration
		    
    .. autofunction:: betrack.utils.parser.parse_file
		    
    .. autofunction:: betrack.utils.parser.parse_directory
		    
    .. autofunction:: betrack.utils.parser.parse_int
		    
    .. autofunction:: betrack.utils.parser.parse_float
		    
    .. autofunction:: betrack.utils.parser.parse_int_or_float
		    
    .. autofunction:: betrack.utils.parser.parse_bool
		    
    .. autofunction:: betrack.utils.parser.parse_str

		    
