#This module contains the work each invidual ant will do

import math
import random
import variables

class Work():
    def __init__(self, ID, start_city, colony):
        self.ID = ID
        self.start_city = start_city
        self.colony = colony
        self.current_city = self.start_city
        self.graph = self.colony.graph
        self.path_vector = []
        self.path_vector.append(self.start_city)
        self.path_cost = 0
        self.Beta = variables.Beta
        self.Q0 = variables.Q0
        self.Rho = variables.Rho
        self.not_traveled_vector = []
        for i in range(0, self.graph.num_cities):
            if i != self.start_city:
                self.not_traveled_vector.append(i)
        self.path_matrix = []
        for i in range(0, self.graph.num_cities):
           self.path_matrix.append([0] * self.graph.num_cities)

    #could this be simpler?
    def run(self):
        graph = self.colony.graph
        while len(self.not_traveled_vector)>0:
            new_city = self.state_transition_rule(self.current_city)
            self.path_cost += graph.distance(self.current_city, new_city)
            self.path_vector.append(new_city)
            self.path_matrix[self.current_city][new_city] = 1 
            self.local_updating_rule(self.current_city, new_city)
            self.current_city = new_city
        self.path_cost += graph.distance(self.path_vector[-1], self.path_vector[0])
        self.colony.update(self)
        self.__init__(self.ID, self.start_city, self.colony)


    def state_transition_rule(self, current_city):
        q = random.random()
        max_city = -1
        if q < self.Q0:
            max_city = self.exploitation(current_city)
        else:
            max_city = self.exploration(current_city)
        if max_city < 0:
            raise Exception("max_city < 0")
        self.not_traveled_vector.remove(max_city)
        return max_city

    def exploitation(self, current_city):
        graph = self.colony.graph
        max_city = -1
        max_val = -1
        val = None
        for city in self.not_traveled_vector:
            if graph.pheromone(current_city, city) == 0:
                raise Exception("pheromone = 0")
            val = graph.pheromone(current_city, city) / math.pow(graph.distance(current_city, city), self.Beta)
            if val > max_val:
                max_val = val
                max_city = city   
        return max_city
            
    def exploration(self, current_city):
        graph = self.colony.graph
        max_city = -1
        sum = 0
        city = -1
        for city in self.not_traveled_vector:
            if graph.pheromone(current_city, city) == 0:
                raise Exception("pheromone = 0")
            sum += graph.pheromone(current_city, city) / math.pow(graph.distance(current_city, city), self.Beta)
        if sum == 0:
            raise Exception("sum = 0")
        avg = sum / len(self.not_traveled_vector)
        #print "avg = %s" % (avg,)
        for city in reversed(self.not_traveled_vector):
            p = graph.pheromone(current_city, city) / math.pow(graph.distance(current_city, city), self.Beta)
            if p > avg:
                max_city = city
                break
        if max_city == -1:
            max_city = city
        return max_city
        
    def local_updating_rule(self, current_city, next_city):
        #Update the pheromones on the pheromone matrix to represent transitions of the ants
        graph = self.colony.graph
        val = (1 - self.Rho) * graph.pheromone(current_city, next_city) + (self.Rho * graph.pheromone0)
        graph.update_pheromone(current_city, next_city, val)

