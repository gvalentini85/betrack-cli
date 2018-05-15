#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the job module..
"""


from os.path import dirname, realpath, isfile
from pims import Video

from betrack.utils.message import wprint
from betrack.utils.parser  import parse_file, parse_directory, parse_int
from betrack.utils.frames  import as_gray, crop, invert_colors

class Job:
    """
    """

    def __init__(self, video, outdir='', margins=None):
        """
        Constructor for the Job class.

        :param video: path to video file 
        :param outdir: path of output directory
        :returns: a job object
        :rtype: Job

        """

        self.video    = video        # Video file name
        self.outdir   = outdir       # Output directory
        self.margins  = margins      # Margins to crop frames
        self.frames   = None         # Original video frames
        self.pframes  = None         # Preprocessed video frames
        
        if self.outdir == '':
            self.outdir= dirname(realpath(self.video))

    def str(self, ind=''):
        """
        """
        
        rval  = ind + 'Video file: '       + self.video        + '\n'
        rval += ind + 'Output directory: ' + self.outdir       + '\n'
        rval += ind + 'Crop margins: '     + str(self.margins)
        
        return rval

    
    def load_frames(self):
        """
        """
        if isfile(self.video):
            self.frames = Video(self.video)
        else:
            raise IOError(errno.ENOENT, 'file not found', self.video)

    def unload_frames(self):
        """
        """
        wprint('def unload_frames(self): Not yet implemented!')
        

    def preprocess_video(self, invert=False):
        """
        """
                
        # Initialize pframes..
        if self.frames is not None:
            self.pframes = self.frames
        else:
            raise TypeError('video not loaded')
        
        # Crop video..
        if self.margins is not None:
            self.pframes = crop(self.pframes, self.margins)
            
        # Convert to gray scale..
        if len(self.pframes[0].shape) == 3:
            self.pframes = as_gray(self.pframes)

        # Invert video..
        if invert:
            self.pframes = invert_colors(self.pframes)
        


def configure_jobs(jobs):
    """
    Configure and return a list of jobs. Return an empty list if
    no valid job is found.

    :param jobs: the list of jobs dictionaries to be configured
    :type: list of dict
    :returns: a list of jobs objects
    :rtype: list of Job
    """


    jobobjs = []

    # Parse jobs..
    for j, i in zip(jobs, range(1, len(jobs) + 1)):
        try:
            video = parse_file(j, 'video')            
        except ValueError:
            wprint('\tJob ', i, ': Attribute <video> not found. Skipping job.', sep='')
            continue        
        except IOError:
            wprint('\tJob ', i, ': Video file not found. Skipping job.', sep='')
            continue
        
        try:
            outdir = parse_directory(j, 'outdir')
        except (ValueError, IOError):
            outdir = ''

        try:
            margins = parse_int(j, 'crop-margins', nentries=4)
        except ValueError as err:
            if err[0] != 'Attribute not found!':
                wprint('\tJob ', i, ': Invalid attribute video (', err[0],
                       '). Skipping job.', sep='')
                continue
            else:
                margins = None
        
        obj = Job(video, outdir, margins)
        jobobjs.append(obj)

    return jobobjs

                
