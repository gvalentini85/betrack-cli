#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The `annotate-video` command.
"""


from numpy import arange, array
from cv2   import (VideoWriter, VideoWriter_fourcc, putText, circle, rectangle,
                   flip, FONT_HERSHEY_SIMPLEX, LINE_AA)
from tqdm  import tqdm

from betrack.commands.command import BetrackCommand
from betrack.utils.frames     import reverse_colors, crop
from betrack.utils.message    import eprint
from betrack.utils.parser     import (open_configuration, parse_str)

class AnnotateVideo(BetrackCommand):
    """Say hello, world!"""

    def __init__(self, options, *args, **kwargs):
        """
        `AnnotateVideo` constructor. 
        """
        
        super(AnnotateVideo, self).__init__(options, *args, **kwargs)

        self.mgap            = 50     # Additional margins to be added to the cropped video
        self.drawregion      = False  # Draw or not the cropped region, if any
        self.drawframenumber = False  # Draw or not the frame number
        self.framenumberpos  = 0      # Position where to draw frame number [-4:4]
        self.flipframes      = ''     # Flip frames vert. 'x', horiz. 'y', or both 'xy'/'yx'

        self.linethickness   = 2
        self.textfont        = FONT_HERSHEY_SIMPLEX
        self.textfontscale   = 0.7
        self.regioncolor     = (120, 245, 65)
        self.particlecolor   = (25, 100, 255)
        self.particleradius  = 3

        
    def configure_annotator(self, filename):
        """
        """

        try:
            config = open_configuration(filename)            
        except IOError:
            eprint('File not found:', filename)
            sys.exit()
            
        try:
            self.flipframes = parse_str(config, 'av-flipframes')
            if not self.flipframes in ['x', 'y', 'xy', 'yx']:
                raise ValueError('<tp-flipframes> must be either \'x\'' + 
                                 ', \'y\', \'xy\', \'yx\'')        
        except ValueError as err:
            eprint('Invalid attribute: ', err[0], '.', sep='')
            sys.exit()
        except KeyError: pass

                
    def draw_particles(self, frame, df, particles):
        """
        """

        # Subset df for selected particles..
        if particles: df = df[df['particle'] in particles]

        for p in df['particle']:
            # Get particle position..
            pos = tuple(df[df['particle'] == p][['x','y']].astype(int).values[0])
        
            # Add particle id..
            putText(frame, str(p), (pos[0] + 3, pos[1] + 3), self.textfont,
                    self.textfontscale, self.particlecolor, self.linethickness,
                    lineType=LINE_AA, bottomLeftOrigin=True)
        
            # Add particle position..
            circle(frame, pos, self.particleradius, self.particlecolor,
                   thickness=-1, lineType=LINE_AA)

    def draw_region(self, frame, region):
        """
        """
        tl = (region[0], region[2])
        br = (region[1], region[3])
        rectangle(frame, tl, br, self.regioncolor, self.linethickness,
                  lineType=LINE_AA)

    def draw_frame_number(self, frame, fnum, region):
        """
        0 -> auto mode
        1 -> top-left outside tracked region (-1 inside)
        2 -> top-right outside tracked region (-2 inside)
        3 -> bottom-left outside tracked region (-3 inside)
        4 -> bottom-right outside tracked region (-4 inside)
        """

        if self.framenumberpos == 0:
            if self.drawregion: self.framenumberpos = 1
            else:               self.framenumberpos = -1

        if self.drawregion == False and self.framenumberpos > 0:
            self.framenumberpos = -self.framenumberpos

        offset = int(round((region[3] - region[2]) * 0.01))
        if   self.framenumberpos == 1:
            pos = (region[0], region[3] + offset)
        elif self.framenumberpos == -1:
            pos = (region[0], region[3] - offset)
        elif self.framenumberpos == 2:
            pos = (region[1], region[3] + offset)
        elif self.framenumberpos == -2:
            pos = (region[1], region[3] - offset)
        elif self.framenumberpos == 3:
            pos = (region[0], region[2] - offset)
        elif self.framenumberpos == -3:
            pos = (region[0], region[2] + offset)
        elif self.framenumberpos == 4:
            pos = (region[1], region[2] - offset)
        elif self.framenumberpos == -4:
            pos = (region[1], region[2] + offset)
            
        putText(frame, 'Frame: ' + str(fnum), pos, self.textfont,
                self.textfontscale, self.regioncolor, self.linethickness,
                   lineType=LINE_AA, bottomLeftOrigin=True)

        
    def annotator(self, job):
        """
        """

        # Init annotator..
        job.pframes = reverse_colors(job.frames)
        codec       = VideoWriter_fourcc('M', 'J', 'P', 'G')
        fps         = job.framerate
        oshape      = job.frameshape[0:2][::-1]
        oldmargins  = job.margins

        if oldmargins is None:
            oldmargins = [0, job.frameshape[1], 0, job.frameshape[0]]
        
        if job.valid_margins() and self.drawregion:
            job.margins = [a - b for a, b in zip(job.margins,
                                                 [self.mgap, -self.mgap,
                                                  self.mgap, -self.mgap])]
            if job.valid_margins():
                oshape = (job.margins[1] - job.margins[0], job.margins[3] - job.margins[2])
            else:
                job.margins     = oldmargins
                self.drawregion = False
                # Frame number should be inside in this case!
        else: self.drawregion = False
        writer = VideoWriter(job.avitracked, codec, fps, oshape)

        # Loop over frames, annotate, crop and save each of them..
        d       = '\033[01m' + '...Exporting video:'
        ut      = ' frame'
        for i in tqdm(arange(job.period[0], job.period[1]), desc=d, unit=ut, total=job.nframes):
            
            # Get frame, subset tracks..
            f  = array(job.pframes[i])
            df = job.dflink[job.dflink['frame'] == i]

            # Draw particles..
            self.draw_particles(f, df, job.drawparticles)

            # Draw tracked region..
            if self.drawregion: self.draw_region(f, oldmargins)

            # Draw frame number..
            if self.drawframenumber: self.draw_frame_number(f, i, oldmargins)

            # Crop frame..
            if job.valid_margins(): f = crop(f, job.margins)

            # Flip frame..
            if   self.flipframes == 'x': flip(f, flipCode=0, dst=f)
            elif self.flipframes == 'y': flip(f, flipCode=1, dst=f)
            elif self.flipframes == 'xy' or self.flipframes == 'yx':
                flip(f, flipCode=-1, dst=f)

            # Write frame to file..
            writer.write(f)
            
        # Close writer..
        writer.release()

        
    def run(self):
        """
        """
        eprint('AnnotateVideo.run not yet implemented!')
