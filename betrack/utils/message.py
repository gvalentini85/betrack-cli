#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the message module..
"""


# Imports
from __future__ import print_function
import sys

class Message:
    BLUE    = '\033[94m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    ENDS    = '\x1b[0m'
    BOLD    = '\033[01m'

    def disable(self):
        self.BLUE   = ''
        self.YELLOW = ''
        self.RED    = ''
        self.ENDS   = ''
        self.BOLD   = ''
        

def mprint(*args, **kwargs):
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

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.BLUE,   end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)


def wprint(*args, **kwargs):
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

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.YELLOW, end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)


def eprint(*args, **kwargs):
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

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.RED,    end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)
