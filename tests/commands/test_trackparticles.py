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
from os       import remove, name
from os.path  import isfile, dirname, realpath
from cv2      import VideoWriter, VideoWriter_fourcc
from numpy    import arange, array, zeros, uint8

from betrack.commands.trackparticles import *

class TestTrackParticles(TestCase):

    @classmethod
    def setUpClass(cls):
        # Create temporary video file..
        cls._vf         = NamedTemporaryFile(mode='w', suffix='.avi', delete=False)
        cls._vf.close()
        cls._nframes    = 10
        cls._pdiameter  = 11      # Must be odd!
        cls._nparticles = 5
        cls._voffset    = 100
        cls._hoffset    = 10        
        codec           = VideoWriter_fourcc('M', 'J', 'P', 'G')
        cls._framerate  = cls._nframes
        cls._frameshape = (1000, 1000, 3)
        oshape          = cls._frameshape[0:2][::-1]
        writer          = VideoWriter(cls._vf.name, codec, cls._framerate, oshape)
        
        for i in arange(0, cls._nframes):
            f = zeros(cls._frameshape, dtype=uint8)
            for p in arange(0, cls._nparticles):
                pr         = int(cls._pdiameter/2)
                y          = cls._voffset * (p + 1)
                y          = arange(y - pr, y + pr + 1)
                x          = cls._voffset + cls._hoffset * (i + 1)
                x          = arange(x - pr, x + pr + 1)
                f[y, x, 1] = 255
            f = array(f)
            writer.write(f)
        writer.release()        
        
        
    @classmethod
    def tearDownClass(cls):
        # Remove temporary file..
        if name != 'nt': remove(cls._vf.name)
    
    def test_configure_tracker(self):        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('parallel: sure!')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        with self.assertRaises(SystemExit) as cm:
            tp.configure_tracker(opt['--configuration'])
        self.assertEqual(cm.exception.code, EX_CONFIG)
        remove(cf.name)

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


    def test_locate_features(self):
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: '  + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: ' + str(self._hoffset) * 2 + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])
        self.assertEqual(tp.jobs[0].outdir, dirname(realpath(self._vf.name)))
        
        tp.jobs[0].load_frames()
        tp.jobs[0].preprocess_video()        
        tp.locate_features(tp.jobs[0])
        self.assertTrue(isfile(tp.jobs[0].h5storage))
        self.assertEqual(dirname(realpath(tp.jobs[0].h5storage)),
                         dirname(realpath(self._vf.name)))

        with trackpy.PandasHDFStoreBig(tp.jobs[0].h5storage) as sf:
            res = sf.dump()
        self.assertEqual(res.shape, (self._nframes * self._nparticles, 9))            
        tp.jobs[0].release_memory()          
        remove(cf.name)

    def test_locate_features_parallel(self):        
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('parallel: True\n')
        cf.write('tp-locate-diameter: '  + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: ' + str(self._hoffset) * 2 + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])
        self.assertEqual(tp.jobs[0].outdir, dirname(realpath(self._vf.name)))
        
        tp.jobs[0].load_frames()
        tp.jobs[0].preprocess_video()        
        tp.locate_features(tp.jobs[0])
        self.assertTrue(isfile(tp.jobs[0].h5storage))
        self.assertEqual(dirname(realpath(tp.jobs[0].h5storage)),
                         dirname(realpath(self._vf.name)))

        with trackpy.PandasHDFStoreBig(tp.jobs[0].h5storage) as sf:
            res = sf.dump()
        self.assertEqual(res.shape, (self._nframes * self._nparticles, 9))            
        tp.jobs[0].release_memory()          
        remove(cf.name)
        
        
    def test_link_trajectories(self):
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: '  + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: ' + str(self._hoffset * 2) + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])        
        tp.jobs[0].load_frames()
        tp.jobs[0].preprocess_video()        
        tp.locate_features(tp.jobs[0])
        tp.link_trajectories(tp.jobs[0])
        
        self.assertTrue(isfile(tp.jobs[0].h5storage))
        self.assertEqual(dirname(realpath(tp.jobs[0].h5storage)),
                         dirname(realpath(self._vf.name)))

        with trackpy.PandasHDFStoreBig(tp.jobs[0].h5storage) as sf:
            res = sf.dump()
        self.assertEqual(res.shape, (self._nframes * self._nparticles, 10))            
        self.assertEqual(tp.jobs[0].dflink.shape, (self._nframes * self._nparticles, 10))
        tp.jobs[0].release_memory()          
        remove(cf.name)

        
    def test_filter_trajectories(self):
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: '     + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: '    + str(self._hoffset * 2) + '\n')
        cf.write('tp-filter-st-threshold: ' + str(int(self._nframes / 2)) + '\n')
        cf.write('tp-filter-cl-threshold: 200\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])        
        tp.jobs[0].load_frames()
        tp.jobs[0].preprocess_video()        
        tp.locate_features(tp.jobs[0])
        tp.link_trajectories(tp.jobs[0])
        tp.filter_trajectories(tp.jobs[0])
        
        self.assertEqual(tp.jobs[0].dflink.shape, (self._nframes * self._nparticles, 10))
        tp.jobs[0].release_memory()          
        remove(cf.name)
        
    def test_export_video(self):
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: '     + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: '    + str(self._hoffset * 2) + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])        
        tp.jobs[0].load_frames()
        tp.jobs[0].preprocess_video()        
        tp.locate_features(tp.jobs[0])
        tp.link_trajectories(tp.jobs[0])
        tp.export_video(tp.jobs[0])
        
        self.assertTrue(isfile(tp.jobs[0].avitracked))
        self.assertEqual(dirname(realpath(tp.jobs[0].avitracked)),
                         dirname(realpath(self._vf.name)))
        tp.jobs[0].release_memory()
        remove(tp.jobs[0].avitracked)
        remove(cf.name)


    def test_export_video_parallel(self):
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('parallel: True\n')
        cf.write('tp-locate-diameter: '     + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: '    + str(self._hoffset * 2) + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])        
        tp.jobs[0].load_frames()
        tp.jobs[0].preprocess_video()        
        tp.locate_features(tp.jobs[0])
        tp.link_trajectories(tp.jobs[0])
        tp.export_video(tp.jobs[0])
        
        self.assertTrue(isfile(tp.jobs[0].avitracked))
        self.assertEqual(dirname(realpath(tp.jobs[0].avitracked)),
                         dirname(realpath(self._vf.name)))
        tp.jobs[0].release_memory()
        remove(tp.jobs[0].avitracked)
        remove(cf.name)
        
        
    def test_run(self):
        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: '     + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: '    + str(self._hoffset * 2) + '\n')
        cf.write('tp-filter-st-threshold: ' + str(int(self._nframes / 2)) + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-frame: [0, 100]\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    crop-margins: [0, 2000, 0, 2000]\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])
        rval = tp.run()
        self.assertEqual(rval, EX_OK)
        remove(cf.name)
        remove(tp.jobs[0].avitracked)

        cf  = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('tp-locate-diameter: '     + str(self._pdiameter) + '\n')
        cf.write('tp-link-searchrange: '    + str(self._hoffset * 2) + '\n')
        cf.write('tp-filter-st-threshold: ' + str(int(self._nframes / 2)) + '\n')
        cf.write('jobs:\n')
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    crop-margins: [0, 2000, 0, 2000]\n')
        cf.close()
        opt = {'--configuration': cf.name}
        tp  = TrackParticles(opt)
        tp.configure_tracker(opt['--configuration'])
        rval = tp.run()        
        self.assertEqual(rval, EX_CONFIG)
        remove(cf.name)
        
