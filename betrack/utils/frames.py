#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The module :py:mod:`~betrack.utils.frames` provides a set of utilities to
preprocess video frames. 

These utilities include functions to convert color frames to gray scale, 
:py:func:`~betrack.utils.frames.as_gray`, 
to crop frames, :py:func:`~betrack.utils.frames.crop`, 
to flip frames around one or two axis, :py:func:`~betrack.utils.frames.flip`, 
to invert the colors of frames, :py:func:`~betrack.utils.frames.invert_colors`, 
and to reverse the order of the frames columns giving each color channe,
:py:func:`~betrack.utils.frames.reverse_colors`.

.. note:: All functions in this module implement lazy evaluation. When passed
          a Slicerator, they will return a Pipeline of the results. 
          When passed any other objects, their behavior is unchanged.
"""

from pims import pipeline

@pipeline
def as_gray(frame):
    """
    Convert a frame to gray scale. This function implements lazy evaluation.

    :param frame: the frame to be converted
    :type frame: ``pims.frame.Frame`` or ``numpy.ndarray``
    :returns: the frame converted in gray scale
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """
    
    red   = frame[:, :, 0]
    blue  = frame[:, :, 1]
    green = frame[:, :, 2]
    rval  = 0.2125 * red + 0.7154 * green + 0.0721 * blue
    
    return rval.astype(frame.dtype)

    
@pipeline
def crop(frame, margins):
    """
    Crop a frame according to the passed margins ([xmin, xmax, ymin, ymax]). 
    This function implements lazy evaluation.

    :param frame: the frame to be converted
    :type series: ``pims.frame.Frame`` or ``numpy.ndarray``
    :param list margins: the new margins of the cropped frame 
    :returns: the cropped frame
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """

    return frame[margins[2]:margins[3], margins[0]:margins[1]]

@pipeline
def flip(frame, direction):
    """
    Convert a frame to gray scale. This function implements lazy evaluation.

    :param frame: the frame to be converted
    :type frame: ``pims.frame.Frame`` or ``numpy.ndarray``
    :returns: the frame in gray scale
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """
    
    print('frames.flip not yet implemented!')

@pipeline
def invert_colors(frame, maxval=255):
    """

    """
        
    return maxval - frame[:, :]


@pipeline
def reverse_colors(frame):
    """
    Reverse the order of colors in a frame from RGB to BGR and from BGR to
    RGB.

    """
    
    return frame[:, :, ::-1]
