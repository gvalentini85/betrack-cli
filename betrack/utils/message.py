# Add copyright here..
"""
Description of the message module..
"""

# Imports
from __future__ import print_function

class Message:
    MESSAGE = 'm'
    WARNING = 'w'
    ERROR   = 'e'    
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
        
def mprint(obj, type):
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
    
    if type == Message.MESSAGE: print(Message.BOLD + Message.BLUE, end='')
    if type == Message.WARNING: print(Message.BOLD + Message.YELLOW, end='')
    if type == Message.ERROR:   print(Message.BOLD + Message.RED, end='')
    print(obj)
    print(Message.ENDS, end='')
