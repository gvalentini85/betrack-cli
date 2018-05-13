"""
Tests for our `betrack hello` subcommand.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestFrames(TestCase):
    
    def test_returns_multiple_lines(self):
        output = popen(['betrack', 'track-particles'], stdout=PIPE).communicate()[0]
        lines = output.split(b'\n')
        self.assertTrue(len(lines) != 1)
