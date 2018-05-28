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
		  Default value: no subperiod selected.
===============   =======================================================================

.. note:: Attributes `period-frame`, `period-second`, and `period-minute` are
	  mutually exclusive!



.. _particles:

Track the Position of Agents
============================

The first command that a *betrack* user generally encounter is the `track-particles`
command. This command let a user track the identity and the position over time of
the agents in a set of videos.

The `track-particles` command can be issued by typing in a terminal:

.. code-block:: bash

   $ betrack track-particles --configuration=<file>

where `<file>` represent the path to a YAML configuration file.

When the `track-particles` command is issued, *betrack* performs the same routine for
each defined job: it preprocesses the video, locates the features in each frame,
links features across frames to recognize particles, filters the recognized particles,
and exports data and tracked video. Locating, linking, and filtering particles is
performed using the Python `trackpy
<https://soft-matter.github.io/trackpy/v0.3.2/>`_ module that is build around the
popular Crocker–Grier algorithm [Cro1996]_. As a matter of fact, the `track-particles`
command is a wrapper of the *trackpy* module designed to make the use of this
module simple and efficient while maintaining the flexibility of its underlying
engine. Additional information with respect to this guide on how to set parameters
of the locate, link, and filter functionalities can be found in the
trackpy `API <http://soft-matter.github.io/trackpy/v0.4.1/api.html>`_ and
`tutorials <http://soft-matter.github.io/trackpy/v0.4.1/tutorial.html>`_.

The `track-particles` command can be used as a standalone command, if only identity
and position of agents are of interest. More importantly, it forms the basis to build
a behavior classifier model by pre-labelling videos from which images can be
extracted to create a training dataset of behaviors.

See also commands :ref:`sample-behaviors <sample>`, :ref:`train-classifier <train>`,
:ref:`track-behaviors <behaviors>`, and :ref:`annotate-video <annotate>`.


.. _particles-examples:

Examples
--------

Minimal working example:

.. code-block:: yaml
		
   tp-locate-diameter: 13
   tp-link-searchrange: 20
   
   jobs:
     - video: ~/path/to/video/file.avi


.. _particles-attributes:

List of attributes
------------------

=========================   ==============================================================
`tp-exportas`               String giving the format used when exporting the tracked
                            trajectories. Accepted values are `'hdf'`, `'csv'`, `'json'`.
			    Default value: `'csv'`.
			    
`tp-locate-diameter`        Odd integer giving the size of the feature in pixels which is
                            assumed the same in each dimension. **Required attribute!**

`tp-locate-featuresdark`    Boolean specifying if the features of interest are dark or
                            bright. Used to determine whether to invert the color scale
			    of the video or not. Default value: `False`.

`tp-locate-minmass`         Float or integer giving the minimum integrated brightness of
                            a particle. Default value: `100`.

`tp-locate-maxsize`         Float or integer giving the maximum radius-of-gyration of the
                            brightness of a particle. Default value: no maximum
			    radius-of-gyration set.

`tp-locate-separation`      Float giving the minimum separation between features. Default
                            value: `tp-locate-diameter + 1`.

`tp-locate-noisesize`       Float giving the width of the Gaussian blurring kernel in
                            pixels. Default value: `1`.

`tp-locate-smoothingsize`   The size in pixels of the square kernel used in the rolling
                            average smoothing. Default value: `tp-locate-diameter`.

`tp-locate-threshold`       Integer or float giving the threshold based on the results of
                            the bandpass filter below which to clip features. Default
			    value: `1` and `1/255`, respectively, for integer and float
			    videos.

`tp-locate-percentile`      Float giving the percentile of pixels to be used as a
                            threshold when selecting features with peaks brighter than this
			    percentile. Default value: `64.0`.

`tp-locate-topn`            Integer giving the maximum number of features above
                            `tp-locate-minmass` to be returned. Default value: return all
                            features above `tp-locate-minmass`.

`tp-locate-preprocess`      Boolean specifying if the video frames should be preprocessed
                            with a bandpass filter or not. Default value: `True`.

`tp-link-searchrange`

`tp-link-memory`

`tp-link-predict`

`tp-link-adaptivestop`

`tp-link-adaptivestep`

`tp-filter-st-threshold`

`tp-filter-quantile`

`tp-filter-cl-threshold`
=========================   ==============================================================


.. _sample:

Build a Database of Behaviors
=============================

.. _sample-examples:

Examples
--------

.. _sample-attributes:

List of attributes
------------------



.. _train:

Train a Behavior Classifier Model
=================================

.. _train-examples:

Examples
--------

.. _train-attributes:

List of attributes
------------------

.. _behaviors:

Track the Behavior of Agents
============================

.. _behaviors-examples:

Examples
--------

.. _behaviors-attributes:

List of attributes
------------------

.. _annotate:

Customize Video Annotations
===========================

.. _annotate-examples:

Examples
--------

.. _annotate-attributes:

List of attributes
------------------


.. rubric:: References

.. [Cro1996] Crocker, J.C. and Grier, D.G.. *Methods of digital video microscopy
	     for colloidal studies*. Journal of colloid and interface science,
	     179(1), pp.298-310, 1996.
