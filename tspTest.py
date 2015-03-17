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
        random.seed(1)
 
    def test_main2(self):
        self.argv=[2,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 4366)

    def test_main3(self):
        self.argv=[3,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 4908)
       
    def test_main4(self):
        self.argv=[4,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5313)
        
    def test_main5(self):
        self.argv=[5,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5396)
        
    def test_main6(self):
        self.argv=[6,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5464)
        
    def test_main7(self):
        self.argv=[7,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5463)
        
    def test_main8(self):
        self.argv=[8,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5453)
        
    def test_main9(self):
        self.argv=[9,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5444)
        
    def test_main10(self):
        self.argv=[10,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5525)
        
        
    def test_main11(self):
        self.argv=[11,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5678)
        
        
    def test_main12(self):
        self.argv=[12,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5760)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(verbosity=2).run(suite)