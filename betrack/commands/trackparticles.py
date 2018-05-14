"""
The `track-particles` command.
"""


from json import dumps

import sys

from .command import BetrackCommand
from ..utils.message import mprint, wprint, eprint
from ..utils.parser import open_configuration
from ..utils.job import configure_jobs 


class TrackParticles(BetrackCommand):
    """Say hello, world!"""


    def __init__(self, options, *args, **kwargs):
        """
        TrackParticles constructor. 
        """
        super(TrackParticles, self).__init__(options, *args, **kwargs)
        self.jobs = []

        
    def configure_tracker(self, filename):
        """
        """

        try:
            config = open_configuration(filename)            
        except IOError:
            eprint('File not found:', filename)
            sys.exit()

        # Parse tracker configuration..

        # Parse jobs..
        self.jobs = configure_jobs(config['jobs'])
        if len(self.jobs) == 0:
            eprint('No job specified!')
            sys.exit()                
                


    def preprocess_video(self):
        """
        """


    def locate_features(self):
        """
        """

        
    def link_trajectories(self):
        """
        """

        
    def filter_trajectories(self):
        """
        """

        
    def save_trajectories(self):
        """
        """
        

    def export_video(self):
        """
        """
        
        
    def run(self):
        """
        Run the `track-particle` command.
#    Compute the range of a continuously-valued time series.
#    
#    Examples: ::
#    
#        >>> from pyinform import utils
#        >>> utils.series_range([0,1,2,3,4,5])
#        (5, 0, 5)
#        >>> utils.series_range([-0.1, 8.5, 0.02, -6.3])
#        (14.8, -6.3, 8.5)
#    :param sequence series: the time series
#    :returns: the range and the minimum/maximum values
#    :rtype: 3-tuple (float, float, float)
#    :raises InformError: if an error occurs within the ``inform`` C call

        """

        
        # Parse options and get list of jobs..
        mprint('Reading configuration file.. ')        
        self.configure_tracker(self.options['--configuration'])
        mprint('Found', len(self.jobs), 'valid jobs.')
    
        # Loop over jobs..
        for job in self.jobs:
            # Open video..
            wprint('Reading video file:', 'filename', end='')
            eprint('\tNot yet implemented!')

            # Preprocess video..
            wprint('Preprocessing video..', end='')            
            self.preprocess_video()
            eprint('\tNot yet implemented!')

            # Locate features..
            wprint('Locating features:', end='')            
            self.locate_features()
            eprint('\tNot yet implemented!')

            # Link trajectories..
            wprint('Linking trajectories:', end='')            
            self.link_trajectories()
            eprint('\tNot yet implemented!')

            # Filter trajectories..
            wprint('Filtering trajectories:', end='')            
            self.filter_trajectories()
            eprint('\tNot yet implemented!')

            # Saving trajectories..
            wprint('Saving trajectories:', end='')            
            self.save_trajectories()
            eprint('\tNot yet implemented!')

            # Export annotated video..
            wprint('Exporting video..', end='')            
            self.export_video()
            eprint('\tNot yet implemented!')

            # Clean up..
        
        print('TrackParticles: Hello, world!')
        print('You supplied the following options:',
              dumps(self.options, indent=2, sort_keys=True))
