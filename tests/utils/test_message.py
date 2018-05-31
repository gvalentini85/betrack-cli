#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for our module `betrack.utils.message`.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from betrack.utils.message import Message

class TestMessage(TestCase):
    
    def test_mprint(self):
        rval = popen(['python', '-c', 
                      'from betrack.utils.message import mprint; mprint(\'Hello world!\')'], 
                     stdout=PIPE).communicate()[0]
        expected = Message.BOLD + Message.GREEN + 'Hello world!\n' + Message.ENDS
        self.assertEqual(rval, expected.encode())


    def test_wprint(self):
        rval = popen(['python', '-c', 
                      'from betrack.utils.message import wprint; wprint(\'Hello world!\')'], 
                     stdout=PIPE).communicate()[0]
        expected = Message.BOLD + Message.YELLOW + 'Hello world!\n' + Message.ENDS
        self.assertEqual(rval, expected.encode())


    def test_eprint(self):
        rval = popen(['python', '-c', 
                      'from betrack.utils.message import eprint; eprint(\'Hello world!\')'], 
                     stdout=PIPE).communicate()[0]
        expected = Message.BOLD + Message.RED + 'Hello world!\n' + Message.ENDS
        self.assertEqual(rval, expected.encode())
        
