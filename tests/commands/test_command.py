#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for our module `betrack.commands.command`.
"""


from unittest import TestCase
from betrack.commands.command import *

class TestBetrackCommand(TestCase):
    
    def test_betrack_command(self):
        bc = BetrackCommand(None, None, None)        
        self.assertEqual(bc.options, None)
        self.assertEqual(bc.args, (None, None))
        self.assertEqual(bc.kwargs, {})

        
    def test_betrack_command_run_NotImplementedError(self):
        bc = BetrackCommand(None, None, None)
        with self.assertRaises(NotImplementedError):
            bc.run()
