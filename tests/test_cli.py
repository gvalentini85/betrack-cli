#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""Tests for our main betrack CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from betrack import __cli__ as CLI
from betrack import __version__ as VERSION

class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['betrack', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Usage:' in output)

        output = popen(['betrack', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['betrack', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), CLI.encode() + b' ' + VERSION.encode())
