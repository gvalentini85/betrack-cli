# Add copyright here..
"""
Description of the `parser` module..
"""

"""

"""

import os
import errno
import yaml

from .message import wprint
        

def open_configuration(filename):
    """
    
    """

    if os.path.isfile(filename):
        # Open yml file..
        filename = os.path.abspath(filename)        
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
        return config
    else:
        # Raise exception
        raise IOError(errno.ENOENT, 'file not found', filename)

def parse_file(src, key):
    """
    Parse a dictionary ``src`` and return a file name specified by ``key``. 
    This function checks that the file specified by ``key`` exists.

    :param dict src: the source dictionary
    :param str key: the key specifing the file name
    :returns: a file name
    :rtype: str
    :raises IOError: if the file specified by ``key`` is not found 
    :raises ValueError: if the attribute ``key`` is not found in ``src``
    """

    if src.has_key(key):
        val = src.get(key)
        if os.path.isfile(val):
            return val
        else:
            raise IOError(errno.ENOENT, 'file not found', val)            
    else:
        raise ValueError('Attribute not found!', key)            


def parse_directory(src, key):
    """
    Parse a dictionary ``src`` and return a directory name specified by ``key``. 
    This function checks that the directory specified by ``key`` exists.

    :param dict src: the source dictionary
    :param str key: the key specifing the directory name
    :returns: a directory name
    :rtype: str
    :raises IOError: if the directory specified by ``key`` is not found 
    :raises ValueError: if the attribute ``key`` is not found in ``src``
    """

    if src.has_key(key):
        val = src.get(key)
        if os.path.isdir(val):
            return val
        else:
            raise IOError(errno.ENOENT, 'directory not found', val)            
    else:
        raise ValueError('Attribute not found!', key)            
    
