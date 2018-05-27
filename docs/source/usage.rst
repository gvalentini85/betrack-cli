*****
Usage
*****

*betrack* is a command line toolkit that can be executed by issuing simple
commands in a terminal. For example, typing the command `betrack` prints the
message:

.. code-block:: bash

   $ betrack
   Usage:
   betrack -h | --help
   betrack --version
   betrack track-particles -c <file> | --configuration=<file>

This message provides minimal information on the patterns of usage of
*betrack*. The `betrack` command accepts different combinations of arguments,
for example, the code below prints the installed version of *betrack*:		

.. code-block:: bash

   $ betrack --version
   betrack 0.1.0

The general usage of the command `betrack` follows this pattern:
		
.. code-block:: bash

   $ betrack <command> -c <file> | --configuration=<file>

In the above code, *betrack* is instructed to execute the subcommand `<command>`
using the configuration file `<file>` passed either using the short option `-c` 
or the long option `--configuration`.

   
Explain the typical workflow to follow using *betrack*..

.. _preliminary:

Preliminary Concepts
====================

*betrack* is designed to process videos in a batch, that is, to apply the
same or similar tracking configuration to a set of videos and process them one
after the other in a sequence.

In the terminology of *betrack*, each video to be
processed is called a *job*. Jobs are characterized by attributes that provide
all necessary information about how to process a video, where to find it and where
to store the results of *betrack*. These attributes are divided into job-specific
attributes, that vary for each video to be processed, and job-wise attributes, that
are instead kept constant for the entire batch of videos. Both types of attributes
are passed to *betrack* using a configuration file written in `YAML
<https://en.wikipedia.org/wiki/YAML>`_.

.. note::

   Most job-specific and job-wise attributes are optional and, if a value
   is not provided, *betrack* will revert to a default configuration
   for the corresponding attribute. Required attributes are defined as such
   in this documentation. If not provided, *betrack* will halt its execution
   and exit with an error message.
   

.. _preliminary-examples:
   
Examples
--------

A list of jobs can be specified in a YAML configuration file using the `jobs`
keyword which begins the definition of a list of jobs. To be considered
valid, each job must include at least the keyword `video` to specify the path of
the video file to be processed in that job. For example, the following YAML code
defines a list of two jobs:

.. code-block:: yaml

   jobs:
     - video: ~/path/to/video/file.avi
     - video: ~/path/to/another/video/file.avi

*betrack* reads the configuration file, parses all attributes (i.e., both
job-specific and job-wise attributes), and checks the validity of the passed
configuration. In the case in which the specification of a job (i.e., job-specific
attributes) contains a syntax error or an invalid value, the job is ignored
and is not added to the list of jobs to be processed. *betrack* will inform
the user with a warning message describing the issue with the job specification.

.. note::

   If the definition of a job-wise attribute (i.e., those defined outside the
   scope of the keyword `jobs`) contains a syntax error or an
   invalid value, *betrack* will halt its execution and exit with an error
   message.

Job-specific attributes generally vary across jobs. These attributes can be
passed to *betrack* by augmenting the minimal definition of a job shown above.
For example, the code below defines two jobs:

.. code-block:: yaml
		
   jobs:
     - video:        ~/path/to/video/file.avi
       crop-margins: [200, 1200, 500, 1500]       
     - video:        ~/path/to/another/video/file.avi
       period-frame: [0, 5000]

In the first job, *betrack* is instructed to crop the video and focus on
a 1000 by 1000 pixels region. In the second job, *betrack* is instructed to
process only the first 5000 frames of the video.

   
.. _preliminary-attributes:

List of attributes
------------------

===============   =======================================================================
`jobs`            Indented list of jobs where each job definition starts with a dash '-'
                  (see also the :ref:`preliminary-examples` above). **Required
		  attribute!**

`video`           File or path to a file specifying the video to be processed in a job.
                  **Required attribute!**

`outdir`          Directory or path to a directory where to store all output files as
                  well as temporary files created by *betrack*. Default value: path to
		  video file exctracted from `video`.

`crop-margins`    List of four integers, `[<xmin>, <xmax>, <ymin>, <ymax>]`, defining a
                  subregion (in pixels) of the video to be processed while the remaining
		  outside portion of the video will be ignored and cropped.
		  Default value: no cropping.

`period-frame`    List of two integers, `[<first-frame>, <last-frame>]`, defining a
                  subperiod (in frames) of the video to be processed while the remaining
		  part of the video will be ignored by *betrack*.
		  Default value: no subperiod selected.

`period-second`   List of two integers or floats, `[<first-second>, <last-second>]`,
                  defining a subperiod (in seconds) of the video to be processed while
		  the remaining part of the video will be ignored by *betrack*.
		  Default value: no subperiod selected.

`period-minute`   List of two integers or floats, `[<first-minute>, <last-minute>]`,
                  defining a subperiod (in minutes) of the video to be processed while
		  the remaining part of the video will be ignored by *betrack*.
		  Default value: no subperiod selected.s
===============   =======================================================================

.. note:: Attributes `period-frame`, `period-second`, and `period-minute` are
	  mutually exclusive!



.. _particles:

Track the Position of Agents
============================

The first command that a *betrack* user generally encounter is the `track-particles`
command. This command let a user track the identity and the position over time of
the agents in a set of videos.

When the `track-particles` command is issued, *betrack* performs the same routine for
each defined job: it preprocesses the video, locates the features in each frame,
links features across frames to recognize particles, filters the recognized particles,
and exports data and tracked video. Locating, linking, and filtering particles is
performed using the Python `trackpy
<https://soft-matter.github.io/trackpy/v0.3.2/>`_ module that is build around the
popular Crocker–Grier algorithm [Cro1996]_. As a matter of fact, the `track-particles`
command is a wrapper of the *trackpy* module designed to make the use of this
module simple and efficient while maintaining the flexibility of its underlying
engine.


The `track-particles` command can be used as a standalone command, if only identity
and position of agents are of interest. More importantly, it forms the basis to build
a behavior classifier model by pre-labelling videos from which images can be
extracted to create a training dataset of behaviors.

The `track-particles` command can be issued by typing in a terminal:

.. code-block:: bash

   $ betrack track-particles --configuration=<file>

where `<file>` represent the path to a YAML configuration file.


.. _particles-examples:

Examples
--------



.. _particles-attributes:

List of attributes
------------------

=========================   ==============================================================
`tp-featuresdark`

`tp-exportas`

`tp-locate-diameter`

`tp-locate-minmass`

`tp-locate-maxsize`

`tp-locate-separation`

`tp-locate-noisesize`

`tp-locate-smoothingsize`

`tp-locate-threshold`

`tp-locate-percentile`

`tp-locate-topn`

`tp-locate-preprocess`

`tp-link-searchrange`

`tp-link-memory`

`tp-link-predict`

`tp-link-adaptivestop`

`tp-link-adaptivestep`

`tp-filter-st-threshold`

`tp-filter-quantile`

`tp-filter-cl-threshold`
=========================   ==============================================================



Build a Database of Behaviors
=============================

Minimal example
---------------

List of all attributes
----------------------



Train a Behavior Classifier Model
=================================

Minimal example
---------------

List of all attributes
----------------------



Track the Behavior of Agents
============================

Minimal example
---------------

List of all attributes
----------------------



Customize Video Annotations
===========================

Minimal example
---------------

List of all attributes
----------------------

.. rubric:: References

.. [Cro1996] Crocker, J.C. and Grier, D.G.. *Methods of digital video microscopy
	     for colloidal studies*. Journal of colloid and interface science,
	     179(1), pp.298-310, 1996.
