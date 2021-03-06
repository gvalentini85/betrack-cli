#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The module :py:mod:`~betrack.utils.job` defines a container for all 
information pertinent to one specific job (i.e., job-specific attributes) by
means of the class :py:class:`~betrack.utils.job.Job` and a set of
methods that support the execution of a job. 

This module also provides a function, :py:func:`~betrack.utils.job.configure_jobs`,
to initialize a list of jobs according to a configuration file.
"""


from os      import remove
from os.path import dirname, realpath, isfile, splitext, basename, join
from pandas  import HDFStore
from pims    import Video
from errno   import ENOENT

from imageio.core import NeedDownloadError
import imageio

from betrack.utils.message import wprint
from betrack.utils.parser  import (parse_file, parse_directory, parse_int, parse_float,
                                   parse_int_or_float)
from betrack.utils.frames  import as_gray, crop, invert_colors

class Job:
    """
    The class :py:class:`betrack.utils.job.Job` defines a container for all
    information pertinent to one specific job and a set of methods that support 
    the execution of a job.
    """

    def __init__(self, video, outdir='', margins=None, period=None, periodtype=None):
        """
        Constructor for the Job class.

        :param str video: path to video file 
        :param str outdir: path of output directory
        :param list margins: new margins to crop the video
        :param list period: selected period of the video to be processed
        :param str periodtype: type of the passed period (``frame``, ``second``, ``minute``)
        :returns: a job object
        :rtype: Job

        """

        self.video         = video        # Video file name
        self.outdir        = outdir       # Output directory
        self.margins       = margins      # Margins to crop frames
        self.frames        = None         # Original video frames
        self.framerate     = None         # Original video frame rate
        self.frameshape    = None         # Original video frame shape
        self.pframes       = None         # Preprocessed video frames
        self.nframes       = None         # Number of selected frames (see self.period)
        self.period        = period       # Initial and final frame indexes (2-tuple)
        self.periodtype    = periodtype   # Period type: 'frame', 'second', 'minute'
        self.dflink        = None         # Dataframe of the linked trajectories
        self.drawparticles = []           # List of particles to annotate, [] means all
        
        if self.outdir == '': self.outdir = dirname(realpath(self.video))            
        self.h5storage  = join(self.outdir, splitext(basename(video))[0] + '-locate.h5')        
        self.h5tracks   = join(self.outdir, splitext(basename(video))[0] + '-tracks.h5')     
        self.csvtracks  = join(self.outdir, splitext(basename(video))[0] + '-tracks.csv')        
        self.jsontracks = join(self.outdir, splitext(basename(video))[0] + '-tracks.json')
        self.avitracked = join(self.outdir, splitext(basename(video))[0] + '-tracked.avi')       


    def str(self, ind=''):
        """
        Returns a string representation of a Job object useful to print 
        information on screen.

        :param str ind: String used for indentation of new lines.
        :returns: a String representing the Job
        :rtype: str 
        """
        
        rval  = ind + 'Video file: '       + self.video
        rval += '\n' + ind + 'Output directory: ' + self.outdir
        if self.margins is not None:
            rval += '\n' + ind + 'Crop margins: '     + str(self.margins)
        if self.period is not None and self.periodtype is not None:
            rval += '\n' + ind + 'Selected period (' + self.periodtype + '): '
            rval += str(self.period)
        
        return rval

    
    def load_frames(self):
        """
        This function loads the video frames, determines the shape and rate of
        frames and, if necessary, select a subperiod of the video according to 
        attributes ``tp-period-frame``, ``tp-period-second``, or ``tp-period-minute``.

        :raises IOError: if the video file is not found
        :raises ValueError: if the selected period is out of range for the video
        """

        # Load video..
        if isfile(self.video):
            try:
                self.frames     = Video(self.video)
                self.framerate  = self.frames.frame_rate
                self.frameshape = self.frames.frame_shape
            except NeedDownloadError:
                imageio.plugins.ffmpeg.download()
                self.frames     = Video(self.video)
                self.framerate  = self.frames.frame_rate
                self.frameshape = self.frames.frame_shape
        else:
            raise IOError(ENOENT, 'file not found', self.video)

        # Select period..
        nframes = self.frames.get_metadata()['nframes']
        if self.period is not None and self.periodtype is not None:
            if self.periodtype == 'second':
                self.period = [int(round(p*self.framerate)) for p in self.period]
                self.periodtype = 'frame'
            elif self.periodtype == 'minute':
                self.period = [int(round(p*60*self.framerate)) for p in self.period]
                self.periodtype = 'frame'

            if (self.period[0] < 0 or
                self.period[0] > nframes - 1 or
                self.period[1] < 1 or
                self.period[1] > nframes):
                raise IndexError("selected period is out of range for the video")            
        else:
            self.period = [0, nframes]
            self.periodtype = 'frame'
        self.nframes = self.period[1] - self.period[0]

        
    def release_memory(self):
        """
        This function attempts to release the memory allocated by the original and
        processed video frames and by the tracked particles data structure. 
        It also deletes the temporary storage file created by
        :py:func:`~betrack.commands.trackparticles.TrackParticles.locate_features`.

        .. note:: Memory is effectively released only if no additional aliases have
                  been created that point to the frames, to the processed frames, 
                  and/or to the trajectories of the video.       
        """

        self.frames.close()
        self.frames  = None
        self.pframes = None
        self.dflink  = None
        if isfile(self.h5storage): remove(self.h5storage)


    def export_trajectories(self, exportas):        
        """
        Export a ``DataFrame`` of the linked trajectories to a file. Possible
        output formats are ``'csv'``, ``'hdf'``, and ``'json'``.

        :param str exportas: The format used to export the data
        """

        # Convert trajectories to the size of the original video..
        if self.valid_margins():
            self.dflink.y += self.margins[2]
            self.dflink.x += self.margins[0]

        # Save trajectories..
        if exportas == 'hdf':
            if isfile(self.h5tracks): remove(self.h5tracks)
            hdf = HDFStore(self.h5tracks)
            hdf.put('dflink', self.dflink, format='table', data_columns=True)
            hdf.close()
        elif exportas == 'csv':
            if isfile(self.csvtracks): remove(self.csvtracks)
            self.dflink.to_csv(self.csvtracks)
        elif exportas == 'json':
            if isfile(self.jsontracks): remove(self.jsontracks)
            df = self.dflink.index = range(0, self.dflink.shape[0])
            self.dflink.to_json(self.jsontracks)
    

    def valid_margins(self):
        """
        Checks the validity of the margins set to crop the video frames with
        respect to the shape of the frames. That is, checks if the margins are
        within the shape of the frames.

        :returns: whether the margins are valid or not
        :rtype: bool
        :raise TypeError: if the video frames are not loaded
        """

        if self.frames is None:
            raise TypeError('video not loaded')        
        
        if type(self.margins) is list:
            if len(self.margins) == 4:
                for m in range(0, 4):
                    if type(self.margins[m]) is not int:
                        return False
                    
                xmin = self.margins[0]
                xmax = self.margins[1]
                ymin = self.margins[2]
                ymax = self.margins[3]
                
                if xmin < 0 or xmin >= xmax or xmin > self.frameshape[1]:
                    return False
                if xmax < 2 or xmax <= xmin or xmax > self.frameshape[1]:
                    return False                
                if ymin < 0 or ymin >= ymax or ymin > self.frameshape[0]:
                    return False
                if ymax < 2 or ymax <= ymin or ymax > self.frameshape[0]:
                    return False
                return True 
        return False
        

    def preprocess_video(self, invert=False):
        """
        This function performs a preprocessing of the video frames according to the
        settings in the configuration file. It crops, converts to gray scale, and
        inverts the colors of the video.

        :param bool invert: whether to invert the colors of the frame of not
        :raise TypeError: if the video frames are not loaded
        :raise ValueError: if the margins are not valid
        """
        
        # Initialize pframes..
        if self.frames is not None:
            self.pframes = self.frames
        else: raise TypeError('video not loaded')
        
        # Crop video..
        if self.margins is not None:
            if self.valid_margins():
                self.pframes = crop(self.pframes, self.margins)
            else: raise ValueError('crop margins are not valid')
            
        # If RGB, convert to gray scale..
        if len(self.frameshape) == 3 and self.frameshape[2] == 3:
            self.pframes = as_gray(self.pframes)

        # Invert video..
        if invert: self.pframes = invert_colors(self.pframes)        


def configure_jobs(jobs):
    """
    Configures and returns a list of :py:class:`~betrack.utils.job.Job` objects.
    Jobs whose configuration is found to be invalid are skipped and not added to
    the list. If no valid job is found in the dictionaries, this function 
    returns an empty list.

    :param list jobs: the list of job dictionaries to be configured
    :returns: a list of :py:class:`~betrack.utils.job.Job` objects
    :rtype: list
    """


    jobobjs = []

    # Parse jobs..
    for j, i in zip(jobs, range(1, len(jobs) + 1)):
        # Parse attribute <video>..
        try:
            video = parse_file(j, 'video')            
        except KeyError:
            wprint('...Job ', i, ': Attribute <video> not found. Skipping job.', sep='')
            continue        
        except IOError:
            wprint('...Job ', i, ': Video file not found. Skipping job.', sep='')
            continue

        # Parse attribute <outdir>..        
        try:
            outdir = parse_directory(j, 'outdir')
        except (KeyError, IOError):
            outdir = ''

        # Parse attribute <crop-margins>..            
        try:
            margins = parse_int(j, 'crop-margins', nentries=4)
        except ValueError as err:
            wprint('...Job ', i, ': Invalid attribute (', str(err),
                   '). Skipping job.', sep='')
            continue
        except KeyError:
            margins = None

        # Parse attribute <period-*>..                                
        period     = None
        periodtype = None
        pf         = 'period-frame'  in j
        ps         = 'period-second' in j
        pm         = 'period-minute' in j
        
        # Parse attribute <period-frame>..                        
        if pf and not (ps or pm):
            try:
                period     = parse_int(j, 'period-frame', nentries=2)
                periodtype = 'frame'
            except ValueError as err:
                wprint('...Job ', i, ': Invalid attribute (', str(err),
                       '). Skipping job.', sep='')
                continue
        # Parse attribute <period-second>..                
        elif ps and not (pf or pm):
            try:
                period = parse_int_or_float(j, 'period-second', nentries=2)
                periodtype = 'second'
            except ValueError as err:
                wprint('...Job ', i, ': Invalid attribute (', str(err),
                       '). Skipping job.', sep='')
                continue
        # Parse attribute <period-minute>..                        
        elif pm and not (pf or ps):
            try:
                period = parse_int_or_float(j, 'period-minute', nentries=2)
                periodtype = 'minute'
            except ValueError as err:
                wprint('...Job ', i, ': Invalid attribute (', str(err),
                       '). Skipping job.', sep='')
                continue
        elif (pf and ps) or (pf and pm) or (ps and pm):
            wprint('...Job ', i, ': <period-frame>, <period-second> and <period-minute>' +
                   ' are mutually exclusive. Skipping job.', sep='')
            continue
        
        # Add job to the list..         
        obj = Job(video, outdir, margins, period, periodtype)
        jobobjs.append(obj)

    return jobobjs

                
