#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for our `betrack annotate-video` subcommand.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestAnnotateVideo(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['betrack', 'annotate-video'], stdout=PIPE).communicate()[0]
        lines = output.split(b'\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_hello_world(self):
        output = popen(['betrack', 'annotate-video'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'AnnotateVideo: Hello, world!' in output)
