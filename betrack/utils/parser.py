#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the `parser` module..
"""


from os.path import isfile, isdir, abspath
import errno
import yaml

from .message import wprint
        

def open_configuration(filename):
    """
    
    """

    if isfile(filename):
        # Open yml file..
        filename = abspath(filename)        
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
        if isfile(val):
            return val
        else:
            raise IOError(errno.ENOENT, 'file not found', val)            
    else:
        raise ValueError('attribute not found!', key)            


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
        if isdir(val):
            return val
        else:
            raise IOError(errno.ENOENT, 'directory not found', val)            
    else:
        raise ValueError('attribute not found!', key)            

def parse_int(src, key, nentries=1):
    """
    Parse a dictionary ``src`` and return an int or a list of int specified by ``key``. 
    This function checks that the value or values specified by ``key`` is of 
    type int or list of int and raises a ``ValueError`` otherwise.

    :param dict src: the source dictionary
    :param str key: the key specifing the directory name
    :param int nentries: the number of integers to parse
    :returns: read integer(s)
    :rtype: int or list of int
    :raises ValueError: if the read value/values are not valid
    """

    if nentries < 1:
        raise ValueError('expected number of entries must be greater than zero')
    
    if src.has_key(key):
        val = src.get(key)
        if type(val) == int:
            if nentries != 1:
                msg = 'attribute ' + key + ' has 1 entry, expected ' + str(nentries)
                raise ValueError(msg)
            return val
        elif type(val) == list:
            nval = len(val)
            if nval != nentries:
                msg  = 'attribute ' + key + ' has ' + str(nval)
                msg += ' entries, expected ' + str(nentries)
                raise ValueError(msg)
            for m in range(0, nval):
                if type(val[m]) != int:                    
                    raise ValueError('entry ' + str(m + 1) + ' is not int')
            return val                            
        else:
            raise ValueError('attribute ' + key + ' is not of type int or list')
    else:
        raise ValueError('attribute not found!', key)            


def parse_float(src, key, nentries=1):
    """
    Parse a dictionary ``src`` and return a float or a list of float specified by ``key``. 
    This function checks that the value or values specified by ``key`` is of 
    type float or list of float and raises a ``ValueError`` otherwise.

    :param dict src: the source dictionary
    :param str key: the key specifing the directory name
    :param int nentries: the number of floats to parse
    :returns: read float(s)
    :rtype: float or list of float
    :raises ValueError: if the read value/values are not valid
    """

    if nentries < 1:
        raise ValueError('expected number of entries must be greater than zero')
    
    if src.has_key(key):
        val = src.get(key)
        if type(val) == float:
            if nentries != 1:
                msg = 'attribute ' + key + ' has 1 entry, expected ' + str(nentries)
                raise ValueError(msg)
            return val
        elif type(val) == list:
            nval = len(val)
            if nval != nentries:
                msg  = 'attribute ' + key + ' has ' + str(nval)
                msg += ' entries, expected ' + str(nentries)
                raise ValueError(msg)
            for m in range(0, nval):
                if type(val[m]) != float:                    
                    raise ValueError('entry ' + str(m + 1) + ' is not float')
            return val                            
        else:
            raise ValueError('attribute ' + key + ' is not of type float or list')
    else:
        raise ValueError('attribute not found!', key)            


def parse_int_or_float(src, key, nentries=1):
    """
    Parse a dictionary ``src`` and return an int or float or a list of int or 
    float specified by ``key``. This function checks that the value or values 
    specified by ``key`` is of type int or float or list of int or float and 
    raises a ``ValueError`` otherwise.

    :param dict src: the source dictionary
    :param str key: the key specifing the directory name
    :param int nentries: the number of floats to parse
    :returns: read float(s)
    :rtype: float or list of float
    :raises ValueError: if the read value/values are not valid
    """

    if nentries < 1:
        raise ValueError('expected number of entries must be greater than zero')
    
    if src.has_key(key):
        val = src.get(key)
        if type(val) == int or type(val) == float:
            if nentries != 1:
                msg = 'attribute ' + key + ' has 1 entry, expected ' + str(nentries)
                raise ValueError(msg)
            return val
        elif type(val) == list:
            nval = len(val)
            if nval != nentries:
                msg  = 'attribute ' + key + ' has ' + str(nval)
                msg += ' entries, expected ' + str(nentries)
                raise ValueError(msg)
            for m in range(0, nval):
                if type(val[m]) != int and type(val[m]) != float:                    
                    raise ValueError('entry ' + str(m + 1) + ' is not int or float')
            return val                            
        else:
            raise ValueError('attribute ' + key + ' is not of type int or float or list')
    else:
        raise ValueError('attribute not found!', key)            


def parse_bool(src, key, nentries=1):
    """
    Parse a dictionary ``src`` and return a bool or a list of bool specified by ``key``. 
    This function checks that the value or values specified by ``key`` is of 
    type bool or list of bool and raises a ``ValueError`` otherwise.

    :param dict src: the source dictionary
    :param str key: the key specifing the directory name
    :param int nentries: the number of booleans to parse
    :returns: read boolean(s)
    :rtype: bool or list of bool
    :raises ValueError: if the read value/values are not valid
    """

    if nentries < 1:
        raise ValueError('expected number of entries must be greater than zero')
    
    if src.has_key(key):
        val = src.get(key)
        if type(val) == bool:
            if nentries != 1:
                msg = 'attribute ' + key + ' has 1 entry, expected ' + str(nentries)
                raise ValueError(msg)
            return val
        elif type(val) == list:
            nval = len(val)
            if nval != nentries:
                msg  = 'attribute ' + key + ' has ' + str(nval)
                msg += ' entries, expected ' + str(nentries)
                raise ValueError(msg)
            for m in range(0, nval):
                if type(val[m]) != bool:                    
                    raise ValueError('entry ' + str(m + 1) + ' is not bool')
            return val                            
        else:
            raise ValueError('attribute ' + key + ' is not of type bool or list')
    else:
        raise ValueError('attribute not found!', key)            

