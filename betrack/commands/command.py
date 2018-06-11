#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The module :py:mod:`~betrack.commands.command` define a common interface
for all commands of *betrack* through the class 
:py:class:`~betrack.commands.command.BetrackCommand`.
"""

try:
    from os import EX_OK, EX_CONFIG
except ImportError:
    EX_OK     = 0
    EX_CONFIG = 78

from sys                      import exit
from betrack.utils.message    import eprint
from betrack.utils.parser     import open_configuration, parse_bool


class BetrackCommand(object):
    """
    The class :py:class:`~betrack.commands.command.BetrackCommand` defines
    a common interface that all commands of *betrack* must implement. 

    In particular, it defines a constructor that takes as argument the command 
    line options automatically parsed by means of ``docopt`` and a
    :py:func:`~betrack.commands.command.BetrackCommand.run` method that must
    be implemented by all inheriting classes.
    """

    def __init__(self, options, *args, **kwargs):
        """
        Constructor for the class :py:class:`~betrack.commands.command.BetrackCommand`.

        .. note:: This class is an interface and should never be explicitly instantiated!

        :param dict options: list of options passed by command line
        :param list \*args: variable length argument list
        :param list \*\*kwargs: arbitrary keyworded arguments
        """
        
        self.options   = options
        self.args      = args
        self.kwargs    = kwargs
        self.parallel  = False
        self.EX_OK     = EX_OK
        self.EX_CONFIG = EX_CONFIG
        


    def configure_betrack(self, filename):
        """
        Configures *betrack* according to the configuration file given by
        ``filename``. If a required attribute is missing from the configuration
        file or if the value of an attribute in the configuration is invalid, 
        this function prints an error message and halts the execution of *betrack*.

        :param str filename: the name of the configuration file
        """
        
        try:
            config = open_configuration(filename)            
        except IOError:
            eprint('File not found:', filename)
            exit(self.EX_CONFIG)
            
        try:
            self.parallel = parse_bool(config, 'parallel')
        except ValueError as err:
            eprint('Invalid attribute: ', str(err), '.', sep='')
            exit(self.EX_CONFIG)
        except KeyError: pass
            

    def run(self):
        """
        Defines an interface method
        :py:func:`~betrack.commands.command.BetrackCommand.run` that must be
        implemented by an inheriting class. This method is automatically 
        called when the corresponding command is passed through the command
        line interface and represents the primary method implementing the
        command.

        :raises NotImplementedError: if the method ``run`` is not implemented
        """
        
        raise NotImplementedError('Command not implemented!')
