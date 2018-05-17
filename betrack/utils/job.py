#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Description of the job module..
"""


from os.path import dirname, realpath, isfile, splitext, basename
from pims import Video

from betrack.utils.message import wprint
from betrack.utils.parser  import parse_file, parse_directory, parse_int
from betrack.utils.frames  import as_gray, crop, invert_colors

class Job:
    """
    """

    def __init__(self, video, outdir='', margins=None, period=None, periodtype=None):
        """
        Constructor for the Job class.

        :param video: path to video file 
        :param outdir: path of output directory
        :returns: a job object
        :rtype: Job

        """

        self.video      = video        # Video file name
        self.outdir     = outdir       # Output directory
        self.margins    = margins      # Margins to crop frames
        self.frames     = None         # Original video frames
        self.pframes    = None         # Preprocessed video frames
        self.period     = period       # Initial and final frame indexes (2-tuple)
        self.periodtype = periodtype   # Period type: 'frame', 'second', 'minute'
        
        if self.outdir == '':
            self.outdir= dirname(realpath(self.video))
        self.h5storage = outdir + splitext(basename(video))[0] + '-locate.h5'        


    def str(self, ind=''):
        """
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
        """
        if isfile(self.video):
            self.frames = Video(self.video)
        else:
            raise IOError(errno.ENOENT, 'file not found', self.video)

    def unload_frames(self):
        """
        """
        wprint('def unload_frames(self): Not yet implemented!')

    def valid_margins(self):
        """
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
                
                if xmin < 0 or xmin >= xmax or xmin > self.frames.frame_shape[1]:
                    return False
                if xmax < 1 or xmax <= xmin or xmax > self.frames.frame_shape[1]:
                    return False                
                if ymin < 0 or ymin >= ymax or ymin > self.frames.frame_shape[0]:
                    return False
                if ymax < 1 or ymax <= ymin or ymax > self.frames.frame_shape[0]:
                    return False
                return True 
        return False
        

    def preprocess_video(self, invert=False):
        """
        """

        # Select period..
        if self.period is not None and self.periodtype is not None:
            if self.periodtype == 'second':
                self.period = [int(round(p*self.frames.frame_rate)) for p in self.period]
                self.period = 'frame'
            if self.periodtype == 'minute':
                self.period = [int(round(p*60*self.frames.frame_rate)) for p in self.period]
                self.period = 'frame'
            if self.periodtype == 'frame':
                self.frames = self.frames[range(self.period[0], self.period[1])]
        
        # Initialize pframes..
        if self.frames is not None:
            self.pframes = self.frames
        else: raise TypeError('video not loaded')
        
        # Crop video..
        if self.valid_margins():
            self.pframes = crop(self.pframes, self.margins)
        else: raise ValueError('crop margins are not valid')
            
        # If RGB, convert to gray scale..
        if len(self.pframes[0].shape) == 3:
            self.pframes = as_gray(self.pframes)
        elif len(self.pframes[0].shape) != 1:
            raise ValueError('video color format not recognized')

        # Invert video..
        if invert:
            if self.frames.pixel_type == 'uint8':
                self.pframes = invert_colors(self.pframes, 255)
            elif self.frames.pixel_type == 'uint16':
                self.pframes = invert_colors(self.pframes, 65535)
            elif self.frames.pixel_type == 'uint32':
                self.pframes = invert_colors(self.pframes, 2**32)
            else:
                ValueError('cannot invert colors for dtype' + str(self.frames.pixel_type))
        


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
        # Parse attribute <video>..
        try:
            video = parse_file(j, 'video')            
        except ValueError:
            wprint('...Job ', i, ': Attribute <video> not found. Skipping job.', sep='')
            continue        
        except IOError:
            wprint('...Job ', i, ': Video file not found. Skipping job.', sep='')
            continue

        # Parse attribute <outdir>..        
        try:
            outdir = parse_directory(j, 'outdir')
        except (ValueError, IOError):
            outdir = ''

        # Parse attribute <crop-margins..            
        try:
            margins = parse_int(j, 'crop-margins', nentries=4)
        except ValueError as err:
            if err[0] != 'attribute not found!':
                wprint('...Job ', i, ': Invalid attribute (', err[0],
                       '). Skipping job.', sep='')
                continue
            else:
                margins = None

        # Parse attribute <period-*>..                                
        period     = None
        periodtype = None
        pf         = j.has_key('period-frame')
        ps         = j.has_key('period-second')
        pm         = j.has_key('period-minute')
        
        # Parse attribute <period-frame>..                        
        if pf and not (ps or pm):
            try:
                period     = parse_int(j, 'period-frame', nentries=2)
                periodtype = 'frame'
            except:
                if err[0] != 'attribute not found!':
                    wprint('...Job ', i, ': Invalid attribute (', err[0],
                           '). Skipping job.', sep='')
                    continue
        # Parse attribute <period-second>..                
        elif ps and not (pf or pm):
            try:
                period = parse_float(j, 'period-second', nentries=2)
                periodtype = 'second'
            except:
                if err[0] != 'attribute not found!':
                    wprint('...Job ', i, ': Invalid attribute (', err[0],
                           '). Skipping job.', sep='')
                    continue
        # Parse attribute <period-minute>..                        
        elif pm and not (pf or ps):
            try:
                period = parse_float(j, 'period-minute', nentries=2)
                periodtype = 'minute'
            except:
                if err[0] != 'attribute not found!':
                    wprint('...Job ', i, ': Invalid attribute (', err[0],
                           '). Skipping job.', sep='')
                    continue
        else:
            wprint('...Job ', i, ': <period-frame>, <period-second> and <period-miinute>' +
                   ' are mutually exclusive. Skipping job.', sep='')
            continue
        
        # Add job to the list..         
        obj = Job(video, outdir, margins, period, periodtype)
        jobobjs.append(obj)

    return jobobjs

                
