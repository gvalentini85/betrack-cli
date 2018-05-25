#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for our module `betrack.utils.message`.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestMessage(TestCase):
    
    def test_mprint_returns_single_line_str(self):
        output = popen(['betrack', 'track-particles'], stdout=PIPE).communicate()[0]
        lines = output.split(b'\n')
        self.assertTrue(1)