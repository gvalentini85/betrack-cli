# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The module :py:mod:`~betrack.commands.trackparticles` implements the 
particle tracking engine of *betrack* that is used in the ``track-particles`` 
command. It is primary a wrapper of the 
`trackpy <http://soft-matter.github.io/trackpy/>`_ module and is designed to
provide a simple and efficient yet flexible interface of ``trackpy`` 
through the class :py:class:`~betrack.commands.trackparticles.TrackParticles`.
"""


from json import dumps

# Needed to turn off 'PyTables will pickle object' warnings..
import warnings
import pandas
warnings.filterwarnings('ignore', category=pandas.io.pytables.PerformanceWarning)

from os      import remove    
from os.path import isfile
from tqdm    import tqdm
import sys
import trackpy

from betrack.commands.command import BetrackCommand
from betrack.utils.message    import mprint, wprint, eprint
from betrack.utils.parser     import (open_configuration, parse_bool, parse_int,
                                      parse_float, parse_int_or_float, parse_str)
from betrack.utils.job        import configure_jobs 


class TrackParticles(BetrackCommand):
    """
    The class :py:class:`~betrack.commands.trackparticles.TrackParticles` defines
    a set of functionalities that combined together implement the ``track-particles``
    command of *betrack*. It allows to load videos, locate features, link and filter
    them as well as to export the results both as a data file and as an annotated 
    video.
    """

    def __init__(self, options, *args, **kwargs):
        """
        Constructor for the class :py:class:`~betrack.commands.trackparticles.TrackParticles`.

        :param dict options: list of options passed by command line
        :param list \*args: variable length argument list
        :param list \*\*kwargs: arbitrary keyworded arguments
        """
        
        super(TrackParticles, self).__init__(options, *args, **kwargs)
        
        self.jobs                      = []      # List of jobs to process
        self.exportas                  = 'csv'

        self.locate_featuresdark       = False   # True if features in the video are dark
        self.locate_diameter           = None
        self.locate_minmass            = 100
        self.locate_maxsize            = None
        self.locate_separation         = None
        self.locate_noisesize          = 1
        self.locate_smoothingsize      = None
        self.locate_threshold          = None
        self.locate_percentile         = 64.0
        self.locate_topn               = None
        self.locate_preprocess         = True

        self.link_searchrange          = None
        self.link_memory               = 0
        self.link_predict              = False
        self.link_adaptivestop         = None
        self.link_adaptivestep         = 0.95

        self.filter_stubs_threshold    = None
        self.filter_clusters_quantile  = None
        self.filter_clusters_threshold = None

        
    def configure_tracker(self, filename):
        """
        Configures the particle tracker according to the configuration file given by
        ``filename``. If a required attribute is missing from the configuration
        file or if the value of an attribute in the configuration is invalid, 
        this function prints an error message and halts the execution of *betrack*.

        :param str filename: the name of the configuration file
        """

        try:
            config = open_configuration(filename)            
        except IOError:
            eprint('File not found:', filename)
            sys.exit()

        # Parse tracker configuration..
        try:
            self.exportas = parse_str(config, 'tp-exportas')
            if not self.exportas in ['hdf', 'csv', 'json']:
                raise ValueError('<tp-exportas> must be either \'hdf\', \'csv\', or \'json\'')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass
                
        try:
            self.locate_diameter = parse_int(config, 'tp-locate-diameter')
            if self.locate_diameter % 2 == 0:
                raise ValueError('<tp-locate-diameter> must be odd')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError:
            eprint('Attribute <tp-locate-diameter> is required.')
            sys.exit()
            
        try:
            self.locate_featuresdark = parse_bool(config, 'tp-locate-featuresdark')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass
        
        try:
            self.locate_minmass = parse_int_or_float(config, 'tp-locate-minmass')
            if self.locate_minmass < 0:
                raise ValueError('<tp-locate-minmass> must be non-negative')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_maxsize = parse_int_or_float(config, 'tp-locate-maxsize')
            if self.locate_maxsize <= 0:
                raise ValueError('<tp-locate-maxsize> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_separation = parse_float(config, 'tp-locate-separation')
            if self.locate_separation < 0:
                raise ValueError('<tp-locate-separation> must be non-negative')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_noisesize = parse_float(config, 'tp-locate-noisesize')
            if self.locate_noisesize <= 0:
                raise ValueError('<tp-locate-noisesize> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_smoothingsize = parse_float(config, 'tp-locate-smoothingsize')
            if self.locate_smoothingsize <= 0:
                raise ValueError('<tp-locate-smoothingsize> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_threshold = parse_int_or_float(config, 'tp-locate-threshold')
            if self.locate_threshold <= 0:
                raise ValueError('<tp-locate-threshold> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_percentile = parse_float(config, 'tp-locate-percentile')
            if self.locate_percentile < 0 or self.locate_percentile >= 100.0:
                raise ValueError('<tp-locate-percentile> must be in the interval [0, 100)')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_topn = parse_int(config, 'tp-locate-topn')
            if self.locate_topn <= 0:
                raise ValueError('<tp-locate-topn> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.locate_preprocess = parse_bool(config, 'tp-locate-preprocess')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.link_searchrange = parse_int_or_float(config, 'tp-link-searchrange')
            if self.link_searchrange <= 0:
                raise ValueError('<tp-link-searchrange> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError:
            eprint('Attribute <tp-link-searchrange> is required.')
            sys.exit()

        try:
            self.link_memory = parse_int(config, 'tp-link-memory')
            if self.link_memory < 0:
                raise ValueError('<tp-link-memory> must be non-negative')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.link_predict = parse_bool(config, 'tp-link-predict')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.link_adaptivestop = parse_float(config, 'tp-link-adaptivestop')
            if self.link_adaptivestop <= 0:
                raise ValueError('<tp-link-adaptivestop> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.link_adaptivestep = parse_float(config, 'tp-link-adaptivestep')
            if self.link_adaptivestep <= 0 or self.link_adaptivestep >= 1.0:
                raise ValueError('<tp-link-adaptivestep> must be in the interval (0.0, 1.0)')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.filter_stubs_threshold = parse_int(config, 'tp-filter-st-threshold')
            if self.filter_stubs_threshold <= 0:
                raise ValueError('<tp-filter-st-threshold> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass
                
        try:
            self.filter_clusters_quantile = parse_float(config, 'tp-filter-cl-quantile')
            if self.filter_clusters_quantile <= 0 or self.filter_clusters_quantile >= 1.0:
                raise ValueError('<tp-filter-cl-quantile> must be in the interval (0.0, 1.0)')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

        try:
            self.filter_clusters_threshold = parse_int(config,
                                                       'tp-filter-cl-threshold')
            if self.filter_clusters_threshold <= 0:
                raise ValueError('<tp-filter-cl-threshold> must be positive')
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

                
        # Parse jobs..
        self.jobs = configure_jobs(config['jobs'])
        if len(self.jobs) == 0:
            eprint('No job specified!')
            sys.exit()                


    def locate_features(self, job):
        """
        Loops over each frame of the video defined by ``job`` and locates features
        based on the current configuration of the particle tracker. This function
        stores the results of its execution in a temporary HDF file defined by
        :py:attr:`betrack.utils.job.Job.h5storage`.
        
        :param job: the job whose features need to be located
        :type job: :py:class:`~betrack.utils.job.Job`
        """

        # Initalize storage file..        
        if isfile(job.h5storage): remove(job.h5storage)
        

        # Locate features in all frames..
        d  = '\033[01m' + '...Locating features'
        ut = ' frame'
        pf = [dict(features=0)]
        with trackpy.PandasHDFStoreBig(job.h5storage) as sf, tqdm(job.pframes, desc=d, unit=ut) as t:       
            for i, frame in enumerate(t):
                features = trackpy.locate(frame, diameter=self.locate_diameter,
                                          minmass=self.locate_minmass,
                                          maxsize=self.locate_maxsize,
                                          separation=self.locate_separation,
                                          noise_size=self.locate_noisesize,
                                          smoothing_size=self.locate_smoothingsize,
                                          percentile=self.locate_percentile,
                                          topn=self.locate_topn,
                                          preprocess=self.locate_preprocess,
                                          threshold=self.locate_threshold)
                
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
        Loops over each frame of the video defined by ``job`` and links features
        based on the current configuration of the particle tracker. This function
        stores the results of its execution in a temporary HDF file defined by
        :py:attr:`betrack.utils.job.Job.h5storage` overwriting the results of the
        execution of 
        :py:func:`~betrack.commands.trackparticles.TrackParticles.locate_features`.

        .. note:: This function must be called after a call to
                  :py:func:`~betrack.commands.trackparticles.TrackParticles.locate_features`.
        
        :param job: the job whose features need to be linked
        :type job: :py:class:`~betrack.utils.job.Job`
        """
        
        # Link trajectories in all frames..
        nframes = len(job.pframes) 
        with trackpy.PandasHDFStoreBig(job.h5storage) as sf:
            d  = '\033[01m' + '...Linking trajectories'
            ut = ' frame'
            if self.link_predict: tp = trackpy.predict.NearestVelocityPredict()
            else: tp = trackpy
            for linked in tqdm(tp.link_df_iter(sf,
                                               search_range=self.link_searchrange,
                                               memory=self.link_memory,
                                               adaptive_stop=self.link_adaptivestop,
                                               adaptive_step=self.link_adaptivestep),
                               desc=d, unit=ut, total=nframes):
                sf.put(linked)
            job.dflink = sf.dump()
                
                
        
    def filter_trajectories(self, job):
        """
        Filters the trajectories of the video defined by ``job`` based on the current 
        configuration of the particle tracker. This function can filter trajectories
        by length in terms of minimum number of frames and/or by clusters in terms of
        minimum feature size.

        .. note:: This function must be called after a call to
                  :py:func:`~betrack.commands.trackparticles.TrackParticles.link_trajectories`.
        
        :param job: the job whose trajectories need to be filtered
        :type job: :py:class:`~betrack.utils.job.Job`
        """

        # Filter out trajectories with few points..
        if self.filter_stubs_threshold is not None:
            job.dflink = trackpy.filter_stubs(job.dflink,
                                              threshold=self.filter_stubs_threshold)

        # Filter out trajectories with a mean particle size above a quantile..
        if (self.filter_clusters_quantile is not None or
            self.filter_clusters_threshold is not None):
            job.dflink = trackpy.filter_clusters(job.dflink,
                                                 quantile=self.filter_clusters_quantile,
                                                 threshold=self.filter_clusters_threshold)
            
        
    def export_video(self, job):
        """
        Exports the tracked features defined by ``job`` as a video based on the current 
        configuration of the particle tracker and of the video annotator. This function 
        calls :py:func:`betrack.commands.annotatevideo.AnnotateVideo.annotator` with a 
        minimal configuration that shows particles' position and identity, tracked region,
        and frame number. Additional arguments to the video annotator can be given
        explicitly in the configuration file.

        .. note:: This function must be called after a call to
                  :py:func:`~betrack.commands.trackparticles.TrackParticles.link_trajectories`.
        
        :param job: the job whose features need to be exported as a video
        :type job: :py:class:`~betrack.utils.job.Job`
        """

        from betrack.commands.annotatevideo import AnnotateVideo

        # Create AnnotateVideo object..
        av = AnnotateVideo(self.options)
        
        # Configure the object..
        av.drawregion      = True
        av.drawframenumber = True
        av.configure_annotator(self.options['--configuration'])
        
        # Annotate and export video..
        av.annotator(job)
        
        
    def run(self):
        """
        This method implements the ``track-particle`` command of *betrack*. It is 
        automatically called when the corresponding command is passed through the command
        line interface.

        This method processes in a batch a sequence of videos with the aim to
        track the position and identity of particles. It preprocesses each video, locates
        features, links and filters their trajectories, and exports the results both
        as a data file and as an annotated video. 

        :returns: ``os.EX_OK`` on success or ``os.EX_CONFIG`` otherwise
        :rtype: int
        """
        
        trackpy.quiet()
        
        # Parse options and get list of jobs..
        mprint('Reading configuration file.. ')
        self.configure_tracker(self.options['--configuration'])
        njobs = len(self.jobs)        
        mprint('Found', njobs, 'valid jobs.')
    
        # Loop over jobs..
        completed = 0
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
                job.preprocess_video(invert=self.locate_featuresdark)
            except ValueError as err:                
                wprint('Preprocessing video: ', err[0], '. Skipping job.', sep='')
                continue            
            mprint('...Preprocessing video: Done')

            # Locate features..
            self.locate_features(job)

            # Link trajectories..
            self.link_trajectories(job)

            # Filter trajectories..
            if (self.filter_stubs_threshold is not None or
                self.filter_clusters_quantile is not None or
                self.filter_clusters_threshold is not None):
                mprint('...Filtering trajectories:', end='\r')
                sys.stdout.flush()
                self.filter_trajectories(job)
                mprint('...Filtering trajectories: Done')            

            # Export trajectories..
            mprint('...Exporting trajectories (', self.exportas, '):', sep='', end='\r')
            sys.stdout.flush()
            job.export_trajectories(self.exportas)
            mprint('...Exporting trajectories (', self.exportas, '): Done', sep='')

            # Export annotated video..
            self.export_video(job)

            # Clean up..
            mprint('...Release job resources:', end='\r')
            job.release_memory()
            mprint('...Release job resources: Done')

            completed += 1


        # Summarize completed jobs..
        if completed > 0:
            mprint('Batch process completed, ', completed, '/', njobs,
                   ' jobs successfully completed!     \(^-^)/', sep='')
            return EX_OK
        else:
            mprint('Batch process completed, ', completed, '/', njobs,
                   ' jobs successfully completed!     ¯\_(ツ)_/¯ ', sep='')
            return EX_CONFIG
