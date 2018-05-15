#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the frames module..
"""

from pims import pipeline

@pipeline
def as_gray(frame):
    """
    Convert a frame to gray scale. This function implements lazy evaluation.

#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
    :param frame: the frame to be converted
    :type ``pims.frame.Frame`` or ``numpy.ndarray``
    :returns: the frame in gray scale
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """

    red   = frame[:, :, 0]
    blue  = frame[:, :, 1]
    green = frame[:, :, 2]
        
    return 0.2125 * red + 0.7154 * green + 0.0721 * blue
    
@pipeline
def crop(frame, margins):
    """
    Convert a frame to gray scale. This function implements lazy evaluation.

#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
    :param frame: the frame to be converted
    :type ``pims.frame.Frame`` or ``numpy.ndarray``
    :returns: the frame in gray scale
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """
    
    print('frames.crop not yet implemented!')
    return frame

@pipeline
def flip(frame, direction):
    """
    Convert a frame to gray scale. This function implements lazy evaluation.

#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
    :param frame: the frame to be converted
    :type ``pims.frame.Frame`` or ``numpy.ndarray``
    :returns: the frame in gray scale
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """
    
    print('frames.flip not yet implemented!')

@pipeline
def invert_colors(frame):
    """
#    Compute the range of a continuously-valued time series.
#    
#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
#    :param sequence series: the time series
#    :returns: the range and the minimum/maximum values
#    :rtype: 3-tuple (float, float, float)
#    :raises InformError: if an error occurs within the ``inform`` C call
    """
    
    print('frames.invert not yet implemented!')

@pipeline
def reverse_colors(frame):
    """
#    Compute the range of a continuously-valued time series.
#    
#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
#    :param sequence series: the time series
#    :returns: the range and the minimum/maximum values
#    :rtype: 3-tuple (float, float, float)
#    :raises InformError: if an error occurs within the ``inform`` C call
    """
    
    print('frames.reverse_colors not yet implemented!')
