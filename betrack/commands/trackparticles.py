#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The `track-particles` command.
"""


from json import dumps

from os import remove
from os.path import isfile
from tqdm import tqdm
import sys
import trackpy

from betrack.commands.command import BetrackCommand
from betrack.utils.message    import mprint, wprint, eprint
from betrack.utils.parser     import open_configuration, parse_bool, parse_int, parse_float
from betrack.utils.job        import configure_jobs 


class TrackParticles(BetrackCommand):
    """Say hello, world!"""


    def __init__(self, options, *args, **kwargs):
        """
        TrackParticles constructor. 
        """
        
        super(TrackParticles, self).__init__(options, *args, **kwargs)
        
        self.jobs          = []         # List of jobs to process
        self.featuresdark  = False      # True if features in the video are dark

        self.diameter      = None
        self.minmass       = 100
        self.maxsize       = None
        self.separation    = None
        self.noisesize     = 1
        self.smoothingsize = None
        self.threshold     = None
        self.percentile    = 64
        self.topn          = None
        self.preprocess    = True
        
    def configure_tracker(self, filename):
        """
        """

        try:
            config = open_configuration(filename)            
        except IOError:
            eprint('File not found:', filename)
            sys.exit()

        # Parse tracker configuration..
        try:
            self.featuresdark = parse_bool(config, 'tp-featuresdark')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.diameter = parse_int(config, 'tp-diameter')
            if self.diameter % 2 == 0:
                raise ValueError('<tp-diameter> must be odd')
        except ValueError as err:
            if err[0] == 'attribute not found!':
                eprint('Attribute <tp-diameter> is required.')
            else:                
                eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()

        try:
            self.minmass = parse_float(config, 'tp-minmass')
            if self.minmass < 0:
                raise ValueError('<tp-minmass> must be non-negative')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.maxsize = parse_float(config, 'tp-maxsize')
            if self.maxsize <= 0:
                raise ValueError('<tp-maxsize> must be positive')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.separation = parse_float(config, 'tp-separation')
            if self.separation < 0:
                raise ValueError('<tp-separation> must be non-negative')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.noisesize = parse_float(config, 'tp-noisesize')
            if self.noisesize <= 0:
                raise ValueError('<tp-noisesize> must be positive')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.smoothingsize = parse_float(config, 'tp-smoothingsize')
            if self.smoothingsize <= 0:
                raise ValueError('<tp-smoothingsize> must be positive')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.threshold = parse_float(config, 'tp-threshold')
            if self.threshold <= 0:
                raise ValueError('<tp-threshold> must be positive')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.percentile = parse_float(config, 'tp-percentile')
            if self.percentile < 0 or self.percentile >= 100.0:
                raise ValueError('<tp-percentile> must be in the interval [0, 100)')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.topn = parse_int(config, 'tp-topn')
            if self.topn <= 0:
                raise ValueError('<tp-topn> must be positive')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        try:
            self.preprocess = parse_bool(config, 'tp-preprocess')
        except ValueError as err:
            if err[0] != 'attribute not found!':
                eprint('Invalid attribute: ', err[0], '.', sep='')
                sys.exit()

        # Parse jobs..
        self.jobs = configure_jobs(config['jobs'])
        if len(self.jobs) == 0:
            eprint('No job specified!')
            sys.exit()                


    def locate_features(self, job):
        """

        """

        # Initalize storage file..        
        if isfile(job.h5storage): remove(job.h5storage)
        

        # Locate features in all frames..
        d  = '\033[01m' + '...Locating features'
        ut = ' frame'
        pf = [dict(features=0)]
        with trackpy.PandasHDFStoreBig(job.h5storage) as sf, tqdm(job.pframes, desc=d, unit=ut) as t:       
            for i, frame in enumerate(t):
                features = trackpy.locate(frame, diameter=self.diameter, minmass=self.minmass,
                                          maxsize=self.maxsize, separation=self.separation,
                                          noise_size=self.noisesize,
                                          smoothing_size=self.smoothingsize,
                                          percentile=self.percentile, topn=self.topn,
                                          preprocess=self.preprocess,
                                          threshold=self.threshold)
                
                if hasattr(frame, 'frame_no') and frame.frame_no is not None:
                    frame_no = frame.frame_no
                else:
                    frame_no = i
                    features['frame'] = i
                    
                t.set_postfix(nfeatures=len(features))
                if len(features) == 0:
                    continue                
                sf.put(features)        

        
    def link_trajectories(self, job):
        """
        # TODO:
        # - add first-frame last-frame as job attributes/variables
        # - add first-second last-second as job attributes
        # - add first-minute last-minute as job attributes
        # - add linking paramters to yml..
        """
        
        # Link trajectories in all frames..
        nframes = len(job.pframes) 
        with trackpy.PandasHDFStoreBig(job.h5storage) as sf:
            d  = '\033[01m' + '...Linking trajectories'
            ut = ' frame'            
            for linked in tqdm(trackpy.link_df_iter(sf, search_range=5, memory=3), desc=d, unit=ut, total=nframes):
                sf.put(linked)
                
        
    def filter_trajectories(self):
        """
        """

        
    def export_trajectories(self):
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
        
        trackpy.quiet()
        
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
                wprint('...Unable to load video. Skipping job.')
                continue
            except IndexError:
                wprint('...Selected period is out of range for the video. Skipping job.')
                continue                

            # Preprocess video..
            mprint('...Preprocessing video..', end='\r')
            try:
                job.preprocess_video(invert=self.featuresdark)
            except ValueError as err:                
                wprint('Preprocessing video: ', err[0], '. Skipping job.', sep='')
                continue            
            mprint('...Preprocessing video: Done.')

            # Locate features..
            self.locate_features(job)

            # Link trajectories..
            self.link_trajectories(job)

            # Filter trajectories..
            wprint('Filtering trajectories:', end='')            
            self.filter_trajectories()
            eprint('\tNot yet implemented!')

            # Saving trajectories..
            wprint('Exporting trajectories:', end='')            
            self.export_trajectories()
            eprint('\tNot yet implemented!')

            # Export annotated video..
            wprint('Exporting video..', end='')            
            self.export_video()
            eprint('\tNot yet implemented!')

            # Clean up..

        # Summarize completed jobs..
        print('TrackParticles: Hello, world!')
        print('You supplied the following options:',
              dumps(self.options, indent=2, sort_keys=True))
