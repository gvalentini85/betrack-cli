#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
The `annotate-video` command.
"""


from json import dumps
from .command import BetrackCommand


class AnnotateVideo(BetrackCommand):
    """Say hello, world!"""

    def run(self):
        print('AnnotateVideo: Hello, world!')
        print('You supplied the following options:',
              dumps(self.options, indent=2, sort_keys=True))
