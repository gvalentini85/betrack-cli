#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The module :py:mod:`~betrack.utils.message` defines a set of wrappers for the
``print`` function that decorate printed text according to the context of the
message.

This module formats and prints status messages 
with :py:func:`~betrack.utils.message.mprint`, warning messages
with :py:func:`~betrack.utils.message.wprint`, and error messages
with :py:func:`~betrack.utils.message.eprint`.
"""


# Imports
from __future__ import print_function
import sys

class Message:
    """
    The class :py:class:`~betrack.utils.message.Message` defines a set of
    constant variables useful to format printed text.

    These variables include specifiers for the 
    :py:const:`~betrack.utils.message.Message.BLUE`,
    :py:const:`~betrack.utils.message.Message.GREEN`, 
    :py:const:`~betrack.utils.message.Message.YELLOW`, and
    :py:const:`~betrack.utils.message.Message.RED` colors, for
    :py:const:`~betrack.utils.message.Message.BOLD` text and to reset
    the text formatting to its default configuration,
    :py:const:`~betrack.utils.message.Message.ENDS`.
    """
    
    BLUE    = '\033[94m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    ENDS    = '\x1b[0m'
    BOLD    = '\033[01m'
    

def mprint(*args, **kwargs):
    """
    Formats the values as a status message and prints them to a stream, 
    or to ``sys.stdout`` by default.

    :param file: a file-like object (stream); defaults to the current ``sys.stdout``
    :type file: file object
    :param str sep: string inserted between values, default to one space
    :param str end: string appended after the last value, default to newline.
    """

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.GREEN,   end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)


def wprint(*args, **kwargs):
    """
    Formats the values as a warning message and prints them to a stream, 
    or to ``sys.stdout`` by default.

    :param file: a file-like object (stream); defaults to the current ``sys.stdout``
    :type file: file object
    :param str sep: string inserted between values, default to one space
    :param str end: string appended after the last value, default to newline.
    """

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.YELLOW, end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)


def eprint(*args, **kwargs):
    """
    Formats the values as an error message and prints them to a stream, 
    or to ``sys.stdout`` by default.

    :param file: a file-like object (stream); defaults to the current ``sys.stdout``
    :type file: file object
    :param str sep: string inserted between values, default to one space
    :param str end: string appended after the last value, default to newline.
    """

    file  = kwargs.get('file', sys.stdout)    
    print(Message.BOLD + Message.RED,    end='', file=file)
    print(*args, **kwargs)
    print(Message.ENDS, end='', file=file)
