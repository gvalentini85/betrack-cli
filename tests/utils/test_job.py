#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for our module `betrack.utils.job`.
"""


from unittest             import TestCase, skip
from tempfile             import NamedTemporaryFile
from numpy                import arange, array, zeros, uint8, float64
from pandas               import DataFrame
from cv2                  import VideoWriter, VideoWriter_fourcc
from os                   import remove, name
from os.path              import isfile
from betrack.utils.job    import *
from betrack.utils.parser import open_configuration

class TestJob(TestCase):

    @classmethod
    def setUpClass(cls):
        # Create temporary video file..
        cls._vf         = NamedTemporaryFile(mode='w', suffix='.avi', delete=False)
        cls._vf.close()
        cls._nframes    = 10
        codec           = VideoWriter_fourcc('M', 'J', 'P', 'G')
        cls._framerate  = cls._nframes
        cls._frameshape = (100, 100, 3)
        oshape          = cls._frameshape[0:2][::-1]
        writer          = VideoWriter(cls._vf.name, codec, cls._framerate, oshape)
        
        for i in arange(0, cls._nframes):
            f          = zeros(cls._frameshape, dtype=uint8)
            f[:, :, 1] = 100
            f[:, :, 2] = 200
            f          = array(f)
            writer.write(f)
        writer.release()        
        
        
    @classmethod
    def tearDownClass(cls):
        # Remove temporary file..
        if name != 'nt': remove(cls._vf.name)

        
    def test_job_str(self):
        job             = Job('dummy.avi')        
        output          = job.str() 
        nlines          = len(output.split('\n'))
        self.assertEqual(nlines, 2)

        job.margins     = [0, 100, 0, 100]        
        output          = job.str() 
        nlines          = len(output.split('\n'))
        self.assertEqual(nlines, 3)

        job.period      = [0, 100]        
        job.periodtype  = 'frame'
        output          = job.str() 
        nlines          = len(output.split('\n'))
        self.assertEqual(nlines, 4)

        
    def test_job_load_frames(self):
        job = Job(self._vf.name)
        job.load_frames()        
        self.assertEqual(job.framerate,   self._framerate)
        self.assertEqual(job.frameshape,  self._frameshape)
        self.assertEqual(job.nframes, self._nframes)
        job.release_memory()

        job.period     = [0, 5]
        job.periodtype = 'frame'
        job.load_frames()        
        self.assertEqual(job.framerate,   self._framerate)
        self.assertEqual(job.frameshape,  self._frameshape)
        self.assertEqual(job.nframes, 5)
        job.release_memory()

        job.period     = [0, 0.5]
        job.periodtype = 'second'
        job.load_frames()        
        self.assertEqual(job.framerate,   self._framerate)
        self.assertEqual(job.frameshape,  self._frameshape)
        self.assertEqual(job.nframes, 5)
        job.release_memory()
        
        job.period     = [0, 0.0083]
        job.periodtype = 'minute'
        job.load_frames()        
        self.assertEqual(job.framerate,   self._framerate)
        self.assertEqual(job.frameshape,  self._frameshape)
        self.assertEqual(job.nframes, 5)
        job.release_memory()

        
    def test_job_load_frames_IOError(self):
        job = Job('dummy.avi')        
        with self.assertRaises(IOError):
            job.load_frames()


    def test_job_release_memory(self):
        job         = Job(self._vf.name)
        job.load_frames()        
        job.pframes = 'memory allocated'
        job.dflink  = 'memory allocated'
        with open(job.h5storage, 'w'): pass
        job.release_memory()
        self.assertEqual(job.frames,  None)
        self.assertEqual(job.pframes, None)
        self.assertEqual(job.dflink,  None)
        self.assertFalse(isfile(job.h5storage))

        
    def test_job_export_trajectories(self):
        job         = Job(self._vf.name)
        job.margins = [10, 100, 10, 100]
        job.load_frames()
        job.dflink  = DataFrame(data={'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                      'y': [3, 4, 3, 4, 3, 4, 3, 4, 3,  4]})

        job.export_trajectories('hdf')
        self.assertTrue(isfile(job.h5tracks))
        remove(job.h5tracks)

        job.export_trajectories('csv')
        self.assertTrue(isfile(job.csvtracks))
        remove(job.csvtracks)

        job.export_trajectories('json')
        self.assertTrue(isfile(job.jsontracks))
        remove(job.jsontracks)
        job.release_memory()


    def test_job_valid_margins(self):
        job = Job(self._vf.name)
        job.load_frames()
        self.assertFalse(job.valid_margins())

        job.margins = [0, 100, 0, 100.0]
        self.assertFalse(job.valid_margins())

        job.margins = [-1, 100, 0, 100]
        self.assertFalse(job.valid_margins())
        job.margins = [100, 100, 0, 100]
        self.assertFalse(job.valid_margins())
        job.margins = [1000, 100, 0, 100]
        self.assertFalse(job.valid_margins())

        job.margins = [0, 1, 0, 100]
        self.assertFalse(job.valid_margins())
        job.margins = [0, 0, 0, 100]
        self.assertFalse(job.valid_margins())
        job.margins = [0, 1000, 0, 100]
        self.assertFalse(job.valid_margins())

        job.margins = [0, 100, -1, 100]
        self.assertFalse(job.valid_margins())
        job.margins = [0, 100, 100, 100]
        self.assertFalse(job.valid_margins())
        job.margins = [0, 100, 1000, 100]
        self.assertFalse(job.valid_margins())

        job.margins = [0, 100, 0, 1]
        self.assertFalse(job.valid_margins())
        job.margins = [0, 100, 0, 0]
        self.assertFalse(job.valid_margins())
        job.margins = [0, 100, 0, 1000]
        self.assertFalse(job.valid_margins())

        job.margins = [0, 90, 0, 90]
        self.assertTrue(job.valid_margins())
        job.margins = [10, 100, 10, 100]
        self.assertTrue(job.valid_margins())
        job.margins = [10, 90, 10, 90]
        self.assertTrue(job.valid_margins())
        job.release_memory()
       

    def test_job_valid_margins_TypeError(self):
        job = Job('dummy.avi')
        with self.assertRaises(TypeError):
            job.valid_margins()
        

    def test_job_preprocess_video(self):
        job         = Job(self._vf.name)
        job.margins = [10, 90, 10, 90]        
        job.load_frames()
        job.preprocess_video(invert=False)
        self.assertNotEqual(job.pframes, None)
        self.assertEqual(job.pframes[0].shape[0:2], (80, 80))

        unexpected = job.pframes[0][0, 0]
        job.preprocess_video(invert=True)
        self.assertNotEqual(job.pframes[0][0, 0], unexpected)        
        job.release_memory()

        
    def test_job_preprocess_video_TypeError(self):
        job = Job('dummy.avi')
        with self.assertRaises(TypeError):
            job.preprocess_video()

            
    def test_job_preprocess_video_ValueError(self):
        job         = Job(self._vf.name)
        job.margins = [0, 100, 0, 100.0]
        job.load_frames()
        with self.assertRaises(ValueError):
            job.preprocess_video()
        job.release_memory()

            
    def test_configure_jobs(self):
        cf = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('test-configure-jobs: None')
        cf.close()
        config = open_configuration(cf.name)
        self.assertEqual(configure_jobs(config), [])
        remove(cf.name)

        cf = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('jobs:\n')
        cf.write('  - video: dummy.avi\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(jobs, [])

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n') 
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 1)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    crop-margins: [0, 100, 0]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 1)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-frame: [0, 100.0]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 1)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-frame: [0, 100]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 2)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-second: [0, hundread]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 2)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-second: [0, 100]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 3)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-minute: [0, hundread]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 3)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-minute: [0, 100]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 4)

        cf = open(cf.name, "a")
        cf.write('  - video: ' + self._vf.name + '\n')
        cf.write('    period-frame: [0, 100]\n')
        cf.write('    period-minute: [0, 100]\n')
        cf.close()
        config = open_configuration(cf.name)
        jobs   = configure_jobs(config['jobs'])
        self.assertEqual(len(jobs), 4)
        
        remove(cf.name)

