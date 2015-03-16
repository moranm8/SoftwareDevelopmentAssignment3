# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:58:53 2015

@author: martin
"""

import random
import unittest
import tsp

class TestMain(unittest.TestCase):
    
    def setUp(self):
        self.argv=[12,"citiesAndDistances.pickled","output.pickled"]
        random.seed(1)
        
    def test_main(self):
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5760)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(verbosity=2).run(suite)