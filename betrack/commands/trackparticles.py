"""
The `track-particles` command.
"""


from json import dumps
from .command import BetrackCommand


class TrackParticles(BetrackCommand):
    """Say hello, world!"""

    def run(self):
        print('TrackParticles: Hello, world!')
        print('You supplied the following options:',
              dumps(self.options, indent=2, sort_keys=True))
