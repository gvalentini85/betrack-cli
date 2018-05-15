#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the job module..
"""


import os

from .message import wprint
from .parser import parse_file, parse_directory

class Job:
    """
    """

    def __init__(self, video, outdir=''):
        """
        """


        self.video   = video
        self.outdir  = outdir
        
        if self.outdir == '':
            self.outdir= os.path.dirname(os.path.realpath(self.video))


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
            wprint('\tJob ', i, ': attribute <video> not found. Skipping job.', sep='')
            continue        
        except IOError:
            wprint('\tJob ', i, ': file not found. Skipping job.', sep='')
            continue
        
        try:
            outdir = parse_directory(j, 'outdir')
        except (ValueError, IOError):
            outdir = ''
        
        obj = Job(video, outdir)
        jobobjs.append(obj)

    return jobobjs

                
