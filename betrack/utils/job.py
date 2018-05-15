#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the job module..
"""


from os.path import dirname, realpath, isfile

from betrack.utils.message import wprint
from .parser import parse_file, parse_directory

class Job:
    """
    """

    def __init__(self, video, outdir=''):
        """
        Constructor for the Job class.

        :param video: path to video file 
        :param outdir: path of output directory
        :returns: a job object
        :rtype: Job

        """


        self.video   = video        # Video file name
        self.outdir  = outdir       # Output directory
        self.frames  = None         # Video frames
        
        if self.outdir == '':
            self.outdir= dirname(realpath(self.video))

    def str(self, ind=''):
        """
        """
        
        rval  = ind + 'Video file: ' + self.video + '\n'
        rval += ind + 'Output directory: ' + self.outdir
        
        return rval

    
    def load_frames(self):
        """
        """
        if isfile(self.video):
            self.frames = pims.Video(self.video)
        else:
            raise IOError(errno.ENOENT, 'file not found', self.video)
        


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
        
        obj = Job(video, outdir)
        jobobjs.append(obj)

    return jobobjs

                
