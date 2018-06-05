#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for module `betrack.commands.trackparticles`.
"""

try:
    from os import EX_OK, EX_CONFIG
except ImportError:
    EX_OK     = 0
    EX_CONFIG = 78

from unittest import TestCase, skip
from tempfile import NamedTemporaryFile
from os       import remove

from betrack.commands.trackparticles import *

class TestTrackParticles(TestCase):
    
    def test_configure_tracker(self):        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-exportas: excel')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 12')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('jobs:')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)
        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-featuresdark: 11\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)
        
