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

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-minmass: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-maxsize: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-separation: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-noisesize: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-smoothingsize: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-threshold: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-percentile: -1.5\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-topn: -1\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-locate-preprocess: -1\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: -1\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-link-memory: -1\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-link-predict: yep\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-link-adaptivestop: -1.0\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-link-adaptivestep: -1.0\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-filter-st-threshold: -1\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-filter-cl-quantile: -1.0\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('tp-filter-cl-threshold: 0\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)
        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: 11\n')
        cf.write('tp-link-searchrange: 10\n')
        cf.write('jobs:\n')
        cf.write('  - video: dummy.avi\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)
        
