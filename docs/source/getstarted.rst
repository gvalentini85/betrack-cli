Getting Started
===============

Requirements and Suggestions
----------------------------

*betrack* requires a few Python modules and other resources to
correctly process video files. All required Python modules are listed as
dependencies of the package and are automatically installed during the
*betrack* installation. Other external dependencies include:

#. ``FFmpeg``

   .. note:: if ``FFmpeg`` is not present on your system, *betrack* will
	     attempt to download and install it. In some cases, notably on
	     Windows using Python 3.4, this process may fail and ``FFmpeg``
	     should be installed instead `manually <http://ffmpeg.org/>`_
	     before *betrack*.
  
Other Python packages that may enhance the performance of *betrack* are
instead nott required and listed here as suggestions. If present, *betrack*
will attempt to exploit their functionalities to boost performance. Suggested
packages include:

* ``numba`` (see `<https://numba.pydata.org/>`_)

Installation using Pip
----------------------

.. warning::

   *betrack* is currently under heavy development and is not yet on PyPI.


Installation from Source
------------------------

If you are want to install *betrack* from source directly, we
recommend closing the `repository <https://github.com/gvalentini85/betrack-cli>`_
and installing the package using pip. You can do so by issuing the
following commands in a terminal:

.. code-block:: bash
		
    $ git clone https://github.com/gvalentini85/betrack-cli.git
    $ cd betrack-cli/
    $ pip install .
    
If you want to install *betrack* system-wise you might need to use ``sudo`` privileges
depending on your environment. If you want to install *betrack* for your account only, or
if you don't have ``sudo`` privileges on your machine you can use the ``--user``
option:

.. code-block:: bash
		
    $ git clone https://github.com/gvalentini85/betrack-cli.git
    $ cd betrack-cli/
    $ pip install --user .

If you are planning to modify or contribute to the *betrack* package
you may want to follow the instructions to install *betrack* in editable
mode included in :ref:`editable-install`.

