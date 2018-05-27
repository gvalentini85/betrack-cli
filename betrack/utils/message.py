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
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    ENDS    = '\x1b[0m'
    BOLD    = '\033[01m'

    def disable(self):
        self.BLUE   = ''
        self.GREEN  = ''
        self.YELLOW = ''
        self.RED    = ''
        self.ENDS   = ''
        self.BOLD   = ''
        

def mprint(*args, **kwargs):
    """

    """

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.GREEN,   end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)


def wprint(*args, **kwargs):
    """

    """

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.YELLOW, end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)


def eprint(*args, **kwargs):
    """

    """

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.RED,    end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)
