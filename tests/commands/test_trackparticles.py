"""
Tests for our `betrack track-particles` subcommand.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestTrackParticles(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['betrack', 'track-particles'], stdout=PIPE).communicate()[0]
        lines = output.split(b'\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_hello_world(self):
        output = popen(['betrack', 'track-particles'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'TrackParticles: Hello, world!' in output)
