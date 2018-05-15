#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The `track-particles` command.
"""


from json import dumps

import sys

from .command import BetrackCommand
from betrack.utils.message import mprint, wprint, eprint
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
        njobs = len(self.jobs)        
        mprint('Found', njobs, 'valid jobs.')
    
        # Loop over jobs..
        for job, i in zip(self.jobs, range(1, njobs + 1)):
            mprint('Working on job ', i, ':', sep='')
            mprint(job.str(ind='...'))

            
            # Open video..
            try:
                job.load_frames()
                mprint('...Number of frames: ', len(job.frames))
            except IOError:
                wprint('...Video file not found. Skipping job.')
                
                

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
