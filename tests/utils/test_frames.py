#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for module `betrack.utils.frames`.
"""


from unittest             import TestCase
from numpy                import zeros, uint8
from betrack.utils.frames import *

class TestFrames(TestCase):
    
    def test_as_gray(self):
        f          = zeros((10, 10, 3), dtype=uint8)
        f[:, :, 0] = 100
        fg         = as_gray(f)
        self.assertEqual(fg.shape, (10, 10)) 
        self.assertEqual(fg.dtype, uint8) 
        self.assertEqual(fg[0, 0], 21)


    def test_crop(self):
        f  = zeros((10, 10, 3), dtype=uint8)
        fc = crop(f, [2, 7, 2, 7])
        self.assertEqual(fc.shape, (5, 5, 3)) 
        self.assertEqual(fc.dtype, uint8) 

        
    def test_invert_colors(self):
        f       = zeros((10, 10), dtype=uint8)
        f[:, :] = 100
        fic     = invert_colors(f)
        self.assertEqual(fic.shape, (10, 10)) 
        self.assertEqual(fic.dtype, uint8) 
        self.assertEqual(fic[0, 0], 155)
        

    def test_reverse_colors(self):
        f          = zeros((10, 10, 3), dtype=uint8)
        f[:, :, 0] = 100
        f[:, :, 2] = 200
        fg         = reverse_colors(f)
        self.assertEqual(fg.shape, (10, 10, 3)) 
        self.assertEqual(fg.dtype, uint8) 
        self.assertEqual(fg[0, 0, 2], f[0, 0, 0])
        self.assertEqual(fg[0, 0, 1], f[0, 0, 1])
        self.assertEqual(fg[0, 0, 0], f[0, 0, 2])
