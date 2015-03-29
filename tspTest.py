# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:58:53 2015

@author: martin
"""

import random
import unittest

import pickle
import tsp

import graphBit

import bigGroup
import sys

import work

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
        self.assertEqual(self.bpc, 5455)
        
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
        
    def test_main13(self):
        self.argv=[13,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 5868)
        
    def test_main14(self):
        self.argv=[14,"citiesAndDistances.pickled","output.pickled"]
        self.bpc=tsp.main(self.argv)
        self.assertEqual(self.bpc, 6115)
        
class TestGraphBit(unittest.TestCase):

    def setUp(self):
        cities = pickle.load(open("citiesAndDistances.pickled", "r"))
        self.num_cities = 14                           
        self.city_distance = cities[1]
        self.graph = graphBit.GraphBit(self.num_cities, self.city_distance)
        
    def test_distance(self):
        distance = self.graph.distance(1,2)
        self.assertEqual(distance, self.city_distance[1][2])
        
    def test_pheremone(self):
        self.graph.pheromone_matrix[1][2] = 2
        pheromone = self.graph.pheromone(1,2)
        self.assertEqual(pheromone, 2)
        
    def test_etha(self):
        for i in range (0,self.num_cities):
            for j in range (0,self.num_cities):
                if i != j:
                    self.assertEqual(self.graph.etha(i,j), 1.0/self.city_distance[i][j])
                    
    def test_update_pheromone(self):
        self.graph.update_pheromone(1,2,2)
        self.assertEqual(self.graph.pheromone_matrix[1][2], 2)
        
    def test_reset_pheromone(self):
        self.graph.pheromone_matrix[1][2] = 2
        self.graph.reset_pheromone()
        self.assertEqual(self.graph.pheromone_matrix[1][2], 0.00016420361247947455)
        
    def test_average_distance(self):
        self.assertEqual(self.graph.average_distance(), 870)

    def test_average_pheromone(self):
        self.graph.reset_pheromone()
        self.assertEqual(self.graph.average_pheromone(), 0.0001642036124794748)
        
    def test_average(self):
        self.assertEqual(self.graph.average(self.city_distance), 870)

class TestBigGroup(unittest.TestCase):

    def setUp(self):
        random.seed(1)
        cities = pickle.load(open("citiesAndDistances.pickled", "r"))
        self.num_cities = 14                           
        self.city_distance = cities[1]
        self.num_ants = 28
        self.num_iterations = 20
        self.num_repetitions = 1
        self.completed_repetitions = 0
        self.graph = graphBit.GraphBit(self.num_cities, self.city_distance)
        self.graph.reset_pheromone()
        self.workers = bigGroup.BigGroup(self.graph, self.num_ants, self.num_iterations,self.num_repetitions,self.completed_repetitions)

    def test_reset(self):
        self.workers.best_path_cost = 1
        self.workers.best_path_vector = [2,3]
        self.workers.best_path_matrix = [4,5]
        self.workers.last_best_path_iteration = 6
        self.workers.reset()
        self.assertEqual(self.workers.best_path_cost,sys.maxint)
        self.assertEqual(self.workers.best_path_vector,None)
        self.assertEqual(self.workers.best_path_matrix,None)
        self.assertEqual(self.workers.last_best_path_iteration,0)
        
    def test_start(self):
        self.workers.start()
        self.assertEqual(self.workers.best_path_cost, 6115)
        
    def test_iteration(self):
        self.workers.ants=self.workers.c_workers()
        self.workers.iter_counter=0
        self.workers.iteration()
        print self.workers.best_path_cost
        self.assertEqual(self.workers.best_path_cost, 6283)

    def test_num_ants(self):
        self.workers.ants=self.workers.c_workers()
        self.assertEqual(self.workers.number_of_ants(), self.num_ants)
        
    def test_num_iterations(self):
        self.assertEqual(self.workers.number_of_iterations(), self.num_iterations)
        
    def test_iteration_counter(self):
        self.workers.iter_counter=42
        self.assertEqual(self.workers.iteration_counter(), 42)
        
    def test_update(self):
        self.assertEqual(1, 1)

    def test_done(self):
        self.workers.iter_counter=4
        self.assertEqual(self.workers.done(), 0)
        self.workers.iter_counter=self.num_iterations
        self.assertEqual(self.workers.done(), 1)
        
    def test_c_workers(self):
        self.workers.c_workers
        self.assertEqual(1, 1)
        
    def test_gloabal_update_rule(self):
        self.assertEqual(1, 1)
        
class TestWork(unittest.TestCase):

    def setUp(self):
        random.seed(1)        

if __name__ == '__main__':
    test_classes_to_run = [TestMain, TestGraphBit, TestBigGroup]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)