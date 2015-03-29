#This module contains the information for the colony of ants for ant colony optimisation

import random
import sys
import work
import variables


class BigGroup:
    def __init__(self, graph, num_ants, num_iterations, num_repetitions, completed_repetitions):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.num_repetitions = num_repetitions
        self.completed_repetitions = completed_repetitions
        self.Alpha = variables.Alpha
        self.reset()

    def reset(self):
        self.best_path_cost = sys.maxint
        self.best_path_vector = None
        self.best_path_matrix = None
        self.last_best_path_iteration = 0

    def start(self):                                                    #Runs the simulation for the required iterations
        self.ants = self.c_workers()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()
            self.global_updating_rule()

    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.run()

    def number_of_ants(self):                                         
        return len(self.ants)

    def number_of_iterations(self):
        return self.num_iterations

    def iteration_counter(self):
        return self.iter_counter

    def update(self, ant):                          #Takes the best and average path of each ant for the iteration
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.best_path_cost:
            self.best_path_cost = ant.path_cost
            self.best_path_matrix = ant.path_matrix
            self.best_path_vector = ant.path_vector
            self.last_best_path_iteration = self.iter_counter                   

    def done(self):
        return self.iter_counter == self.num_iterations

    def c_workers(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = work.Work(i, random.randint(0, self.graph.num_cities - 1), self)  #Creates multiple instances of work, one for each ant
            ants.append(ant)
        return ants
 
    def global_updating_rule(self):
        self.avg_path_cost /= len(self.ants)
        print "%s %%" % ((float(self.iter_counter)/(self.num_iterations*self.num_repetitions)+float(self.completed_repetitions)/self.num_repetitions)*100)
        for r in range(0, self.graph.num_cities):
            for s in range(0, self.graph.num_cities):
                if r != s:
                    evaporation = (1 - self.Alpha) * self.graph.pheromone(r, s)
                    deposition = self.Alpha * self.best_path_matrix[r][s] / self.best_path_cost                     #Consider removing delt_pheromone, only time used here
                    self.graph.update_pheromone(r, s, evaporation + deposition)
