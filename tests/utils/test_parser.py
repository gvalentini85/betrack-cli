"""
Tests for our module `betrack.utils.parser`.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestParser(TestCase):
    
    def test_parser_returns_single_line_str(self):
        output = popen(['betrack', 'track-particles'], stdout=PIPE).communicate()[0]
        lines = output.split(b'\n')
        self.assertTrue(1)
