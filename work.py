
import math
import random

class Work():
    def __init__(self, ID, start_city, colony):             #ID = i; start_city=random; colony = BigGroup
        self.ID = ID
        self.start_city = start_city
        self.colony = colony
        self.current_city = self.start_city
        self.graph = self.colony.graph                    #graph = GraphBit
        self.path_vector = []                               #Could combine these two lines
        self.path_vector.append(self.start_city)
        self.path_cost = 0
        self.Beta = 1.0
        self.Q0 = 0.5
        self.Rho = 0.99
        self.not_traveled_vector = {}                                       #empty dictionary[a data structure that maps one value to another]
        for i in range(0, self.graph.num_cities):
            if i != self.start_city:
                self.not_traveled_vector[i] = i                             #Changes not_traveled_vector into a 1d array? Includes all city index other than stating city
        self.path_matrix = []
        for i in range(0, self.graph.num_cities):
           self.path_matrix.append([0] * self.graph.num_cities)    #Creates path_matrix as a num_city*num_city 2d array of 0s

    #could this be simpler?
    def run(self):
        graph = self.colony.graph                         #graph = GraphBit. No need to redefine, could just refence as self.graph
        while not self.end():
            new_city = self.state_transition_rule(self.current_city)
            self.path_cost += graph.delta(self.current_city, new_city)
            self.path_vector.append(new_city)
            self.path_matrix[self.current_city][new_city] = 1 
            self.local_updating_rule(self.current_city, new_city)
            self.current_city = new_city
        self.path_cost += graph.delta(self.path_vector[-1], self.path_vector[0])
        self.colony.update(self)
        self.__init__(self.ID, self.start_city, self.colony)                    #Consider removing. Affects RNG? Resets not_traveled vector

    def end(self):
        return not self.not_traveled_vector                                 #self.not_traveled_vector always equals 0? Returns 1?


    def state_transition_rule(self, current_city):
        graph = self.colony.graph
        q = random.random()
        max_city = -1
        if q < self.Q0:                                     #Is true half the time when Q0 is 0.5
            #print "Exploitation"                           #This takes the city where the val is max
            max_val = -1                                    #Want the first val to be always bigger than max_val
            val = None
            for city in self.not_traveled_vector.values():
                if graph.pheromone(current_city, city) == 0:
                    raise Exception("pheromone = 0")
                val = graph.pheromone(current_city, city) * math.pow(graph.etha(current_city, city), self.Beta)
                if val > max_val:
                    max_val = val
                    max_city = city
        else:
            #Bob was here
            #print "Exploration"
            sum = 0
            city = -1
            for city in self.not_traveled_vector.values():
                if graph.pheromone(current_city, city) == 0:
                    raise Exception("pheromone = 0")
                sum += graph.pheromone(current_city, city) * math.pow(graph.etha(current_city, city), self.Beta)  #Smae as line 54
            if sum == 0:
                raise Exception("sum = 0")
            avg = sum / len(self.not_traveled_vector)
            #print "avg = %s" % (avg,)
            for city in self.not_traveled_vector.values():
                p = graph.pheromone(current_city, city) * math.pow(graph.etha(current_city, city), self.Beta)     #Same as line 54
                if p > avg:
                    #print "p = %s" % (p,)
                    max_city = city             #We keep reassigning max city. Last city where p > avg will be max_city
            if max_city == -1:
                max_city = city                 #If none satisfy p>avg then this, which will produce an exception in the next line
        if max_city < 0:
            raise Exception("max_city < 0")
        del self.not_traveled_vector[max_city]                  #Delete from not_traveled_vector in either case
        return max_city

    def local_updating_rule(self, current_city, next_city):
        #Update the pheromones on the pheromone matrix to represent transitions of the ants
        graph = self.colony.graph
        val = (1 - self.Rho) * graph.pheromone(current_city, next_city) + (self.Rho * graph.pheromone0)
        graph.update_pheromone(current_city, next_city, val)

