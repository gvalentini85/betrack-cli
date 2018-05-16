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
    Crop a frame according to the passed margins ([xmin, xmax, ymin, ymax]). 
    This function implements lazy evaluation.

#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
    :param frame: the frame to be converted
    :type ``pims.frame.Frame`` or ``numpy.ndarray``
    :param list margins: the new margins of the cropped frame 
    :returns: the cropped frame
    :rtype: ``pims.frame.Frame`` or ``numpy.ndarray``
    """

    return frame[margins[2]:margins[3], margins[0]:margins[1]]

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
def invert_colors(frame, maxval=255):
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
        
    return maxval - frame[:, :]


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
