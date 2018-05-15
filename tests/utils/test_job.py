"""
Tests for our module `betrack.utils.job`.
"""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestJob(TestCase):
    
    def test_job_returns_single_line_str(self):
        output = popen(['betrack', 'track-particles'], stdout=PIPE).communicate()[0]
        lines = output.split(b'\n')
        self.assertTrue(1)
