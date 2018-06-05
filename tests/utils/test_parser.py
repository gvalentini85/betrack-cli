#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
Tests for our module `betrack.utils.parser`.
"""


from unittest import TestCase, skip
from tempfile import NamedTemporaryFile
from os       import remove
from os.path  import dirname, abspath

from betrack.utils.parser import *

class TestParser(TestCase):

    def test_open_configuration(self):
        cf = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('test-open-configuration: True')
        cf.close()
        config = open_configuration(cf.name)
        self.assertDictEqual({'test-open-configuration': True}, config)
        remove(cf.name)

            
    def test_open_configuration_IOError(self):
        cf = NamedTemporaryFile(suffix='.yml')
        cf.close()
        with self.assertRaises(IOError):        
            config = open_configuration(cf.name)

            
    def test_parse_file(self):        
        cf = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        cf.write('test-parse-file: ' + cf.name)
        cf.close()
        config = open_configuration(cf.name)
        fname  = parse_file(config, 'test-parse-file')
        self.assertEqual(cf.name, fname)
        remove(cf.name)

            
    def test_parse_file_IOError(self):
        cf = NamedTemporaryFile(suffix='.yml')
        cf.close()
        config = {'test-parse-file': cf.name}
        with self.assertRaises(IOError):        
            fname = parse_file(config, 'test-parse-file')

            
    def test_parse_file_KeyError(self):        
        config = {'test-parse-file-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_file(config, 'missing-attribute')

        
    def test_parse_directory(self):
        cf = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        dnamew = dirname(abspath(cf.name))
        cf.write('test-parse-directory: ' + dnamew)
        cf.close()
        config = open_configuration(cf.name)
        dnamer  = parse_directory(config, 'test-parse-directory')
        self.assertEqual(dnamer, dnamew)
        remove(cf.name)

        
    def test_parse_directory_IOError(self):
        cf = NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
        dnamew = dirname(abspath(cf.name)) + cf.name
        cf.write('test-parse-directory: ' + dnamew)
        cf.close()
        config = open_configuration(cf.name)
        with self.assertRaises(IOError):                    
            dnamer = parse_directory(config, 'test-parse-directory')
        remove(cf.name)

        
    def test_parse_directory_KeyError(self):        
        config = {'test-parse-directory-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_directory(config, 'missing-attribute')

            
    def test_parse_int(self):
        val  = 1
        key  = 'test-parse-int'
        rval = parse_int({key: val}, key)
        self.assertEqual(rval, val)

        
    def test_parse_int_list(self):        
        val  = [1, 2]
        key  = 'test-parse-int'
        rval = parse_int({key: val}, key, nentries=2)
        self.assertEqual(rval, val)

        
    def test_parse_int_invalid_nentries(self):
        val = 1
        key = 'test-parse-int'
        with self.assertRaises(ValueError):
            rval = parse_int({key: val}, key, nentries=0)

        with self.assertRaises(ValueError):
            rval = parse_int({key: val}, key, nentries=2)

        with self.assertRaises(ValueError):
            val  = [1, 2]
            rval = parse_int({key: val}, key, nentries=1)            

        
    def test_parse_not_int(self):        
        key = 'test-parse-int'
        with self.assertRaises(ValueError):
            val  = '1'
            rval = parse_int({key: val}, key, nentries=1)

        with self.assertRaises(ValueError):
            val  = ['1', 2]
            rval = parse_int({key: val}, key, nentries=2)            

        with self.assertRaises(ValueError):
            val  = [1, '2']
            rval = parse_int({key: val}, key, nentries=2)            
            

    def test_parse_int_KeyError(self):        
        config = {'test-parse-int-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_int(config, 'missing-attribute')

        
    def test_parse_float(self):
        val  = 1.0
        key  = 'test-parse-float'
        rval = parse_float({key: val}, key)
        self.assertEqual(rval, val)

        
    def test_parse_float_list(self):        
        val  = [1.0, 2.0]
        key  = 'test-parse-float'
        rval = parse_float({key: val}, key, nentries=2)
        self.assertEqual(rval, val)

        
    def test_parse_float_invalid_nentries(self):
        val = 1.0
        key = 'test-parse-float'
        with self.assertRaises(ValueError):
            rval = parse_float({key: val}, key, nentries=0)

        with self.assertRaises(ValueError):
            rval = parse_float({key: val}, key, nentries=2)

        with self.assertRaises(ValueError):
            val  = [1.0, 2.0]
            rval = parse_float({key: val}, key, nentries=1)            

            
    def test_parse_not_float(self):        
        key = 'test-parse-float'
        with self.assertRaises(ValueError):
            val  = '1'
            rval = parse_float({key: val}, key, nentries=1)

        with self.assertRaises(ValueError):
            val  = ['1', 2]
            rval = parse_float({key: val}, key, nentries=2)            

        with self.assertRaises(ValueError):
            val  = [1, '2']
            rval = parse_float({key: val}, key, nentries=2)            

            
    def test_parse_float_KeyError(self):        
        config = {'test-parse-float-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_float(config, 'missing-attribute')


    def test_parse_int_or_float(self):
        val  = 1
        key  = 'test-parse-int-or-float'
        rval = parse_int_or_float({key: val}, key)
        self.assertEqual(rval, val)

        val  = 1.0
        key  = 'test-parse-int-or-float'
        rval = parse_int_or_float({key: val}, key)
        self.assertEqual(rval, val)
        
        
    def test_parse_int_or_float_list(self):        
        val  = [1, 2]
        key  = 'test-parse-int-or-float'
        rval = parse_int_or_float({key: val}, key, nentries=2)
        self.assertEqual(rval, val)

        val  = [1.0, 2]
        key  = 'test-parse-int-or-float'
        rval = parse_int_or_float({key: val}, key, nentries=2)
        self.assertEqual(rval, val)

        val  = [1.0, 2.0]
        key  = 'test-parse-int-or-float'
        rval = parse_int_or_float({key: val}, key, nentries=2)
        self.assertEqual(rval, val)
        
        
    def test_parse_int_or_float_invalid_nentries(self):
        val = 1
        key = 'test-parse-int-or-float'
        with self.assertRaises(ValueError):
            rval = parse_int_or_float({key: val}, key, nentries=0)

        with self.assertRaises(ValueError):
            rval = parse_int_or_float({key: val}, key, nentries=2)

        with self.assertRaises(ValueError):
            val  = [1.0, 2]
            rval = parse_int_or_float({key: val}, key, nentries=1)            

            
    def test_parse_not_int_or_float(self):        
        key = 'test-parse-int-or-float'
        with self.assertRaises(ValueError):
            val  = '1'
            rval = parse_int_or_float({key: val}, key, nentries=1)

        with self.assertRaises(ValueError):
            val  = ['1', 2]
            rval = parse_int_or_float({key: val}, key, nentries=2)            

        with self.assertRaises(ValueError):
            val  = [1, '2']
            rval = parse_int_or_float({key: val}, key, nentries=2)            

            
    def test_parse_int_or_float_KeyError(self):        
        config = {'test-parse-int-or-float-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_int_or_float(config, 'missing-attribute')
        
        
    def test_parse_bool(self):
        val  = True
        key  = 'test-parse-bool'
        rval = parse_bool({key: val}, key)
        self.assertEqual(rval, val)

        
    def test_parse_bool_list(self):        
        val  = [True, False]
        key  = 'test-parse-bool'
        rval = parse_bool({key: val}, key, nentries=2)
        self.assertEqual(rval, val)

        
    def test_parse_bool_invalid_nentries(self):
        val = True
        key = 'test-parse-bool'
        with self.assertRaises(ValueError):
            rval = parse_bool({key: val}, key, nentries=0)

        with self.assertRaises(ValueError):
            rval = parse_bool({key: val}, key, nentries=2)

        with self.assertRaises(ValueError):
            val  = [1.0, 2.0]
            rval = parse_bool({key: val}, key, nentries=1)            

            
    def test_parse_not_bool(self):        
        key = 'test-parse-bool'
        with self.assertRaises(ValueError):
            val  = 'True'
            rval = parse_bool({key: val}, key, nentries=1)

        with self.assertRaises(ValueError):
            val  = ['1', False]
            rval = parse_bool({key: val}, key, nentries=2)            

        with self.assertRaises(ValueError):
            val  = [True, '2']
            rval = parse_bool({key: val}, key, nentries=2)            

            
    def test_parse_bool_KeyError(self):
        config = {'test-parse-bool-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_bool(config, 'missing-attribute')
            

    def test_parse_str(self):
        val  = 'string'
        key  = 'test-parse-str'
        rval = parse_str({key: val}, key)
        self.assertEqual(rval, val.encode())

        
    def test_parse_str_list(self):        
        val  = ['a string', 'another string']
        key  = 'test-parse-str'
        rval = parse_str({key: val}, key, nentries=2)
        self.assertEqual(rval, val)

        
    def test_parse_str_invalid_nentries(self):
        val = 'string'
        key = 'test-parse-str'
        with self.assertRaises(ValueError):
            rval = parse_str({key: val}, key, nentries=0)

        with self.assertRaises(ValueError):
            rval = parse_str({key: val}, key, nentries=2)

        with self.assertRaises(ValueError):
            val  =  ['a string', 'another string']
            rval = parse_str({key: val}, key, nentries=1)            

            
    def test_parse_not_str(self):        
        key = 'test-parse-str'
        with self.assertRaises(ValueError):
            val  = 1
            rval = parse_str({key: val}, key, nentries=1)

        with self.assertRaises(ValueError):
            val  = [1, 'another string']
            rval = parse_str({key: val}, key, nentries=2)            

        with self.assertRaises(ValueError):
            val  = ['a string', 2]
            rval = parse_str({key: val}, key, nentries=2)            

            
    def test_parse_str_KeyError(self):        
        config = {'test-parse-str-KeyError': 0}
        with self.assertRaises(KeyError):        
            fname = parse_str(config, 'missing-attribute')
