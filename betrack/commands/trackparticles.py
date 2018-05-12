"""
The `track-particles` command.
"""


from json import dumps
from .command import BetrackCommand


class TrackParticles(BetrackCommand):
    """Say hello, world!"""

    def run(self):

        # Parse options and get list of jobs..
        print('\033[01m' + '\033[94m' + 'Parsing parameters..' + '\x1b[0m')
        
        # Loop over jobs..
        for job in range(0, 10):
            job + 1
            # Retrieve job-specific parameters..

            # Open video..

            # Preprocess video..

            # Locate features..

            # Link trajectories..

            # Filter trajectories..

            # Saving trajectories..

            # Annotate video..

            # Clean up..
        
        print('TrackParticles: Hello, world!')
        print('You supplied the following options:',
              dumps(self.options, indent=2, sort_keys=True))
