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


import random
import sys



class BigGroup:
    def __init__(self, graph, num_ants, num_iterations):            #graph = GraphBit; num_ants = na, num_iterations = num_iterations
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1
        self.reset()

    def reset(self):
        self.best_path_cost = sys.maxint
        self.best_path_vector = None
        self.best_path_matrix = None
        self.last_best_path_iteration = 0

    def start(self):
        self.ants = self.c_workers()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()
            # Note that this will help refine the results future iterations.
            self.global_updating_rule()

    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.run()

    def num_ants(self):
        return len(self.ants)

    def num_iterations(self):
        return self.num_iterations

    def iteration_counter(self):
        return self.iter_counter

    def update(self, ant):                                                      #Only called by Work, but must be in this class
        #print "Update called by %s" % (ant.ID,)
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.best_path_cost:
            self.best_path_cost = ant.path_cost
            self.best_path_matrix = ant.path_matrix
            self.best_path_vector = ant.path_vector
            self.last_best_path_iteration = self.iter_counter                   #Never used. Consider removing
        if self.ant_counter == len(self.ants):                                  #Could make more sense if we move this to global_update_rule
            self.avg_path_cost /= len(self.ants)
            print "Best: %s, %s, %s, %s" % (
                self.best_path_vector, self.best_path_cost, self.iter_counter, self.avg_path_cost,)


    def done(self):                                                             #Never used. Consider removing
        return self.iter_counter == self.num_iterations

    def c_workers(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Work(i, random.randint(0, self.graph.num_cities - 1), self)    #Initializes Work multiple times[with different randint]. Should change to initializing once and calling a function multiple times?
            ants.append(ant)

        return ants
 
    def global_updating_rule(self):
        #can someone explain this
        evaporation = 0                                                         #Unnecessary to reset to 0. Not sure if evaporation and deposition is the correct name for these
        deposition = 0
        for r in range(0, self.graph.num_cities):
            for s in range(0, self.graph.num_cities):
                if r != s:
                    delt_pheromone = self.best_path_matrix[r][s] / self.best_path_cost
                    evaporation = (1 - self.Alpha) * self.graph.pheromone(r, s)
                    deposition = self.Alpha * delt_pheromone                          #Consider removing delt_pheromone, only time used here
                    self.graph.update_pheromone(r, s, evaporation + deposition)

class GraphBit:
    def __init__(self, num_cities, city_distance, pheromone_matrix=None):     #num_cities = num_cities =number of cities; city_distance = city_distance = 2d array of distances between cities
        print len(city_distance)
        if len(city_distance) != num_cities:
            raise Exception("len(delta) != num_cities")
        self.num_cities = num_cities
        self.city_distance = city_distance 
        if pheromone_matrix is None:
            self.pheromone_matrix = []                                   #Sets the size of 2d array pheromone_matrix to the number of cities
            for i in range(0, num_cities):
                self.pheromone_matrix.append([0] * num_cities)
            print "\npheromone_matrix was called" 
            print self.pheromone_matrix

    def delta(self, r, s):
        return self.city_distance[r][s]

    def pheromone(self, r, s):
        return self.pheromone_matrix[r][s]

    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    def update_pheromone(self, r, s, val):
        self.pheromone_matrix[r][s] = val

    def reset_pheromone(self):
        avg = self.average_delta()
        self.pheromone0 = 1.0 / (self.num_cities * 0.5 * avg)           #Does this even do anything useful
        print "Average = %s" % (avg,)
        print "pheromone0 = %s" % (self.pheromone0)
        for r in range(0, self.num_cities):
            for s in range(0, self.num_cities):
                self.pheromone_matrix[r][s] = self.pheromone0


    def average_delta(self):
        return self.average(self.city_distance)


    def average_pheromone(self):
        return self.average(self.pheromone_matrix)

    def average(self, matrix):
        sum = 0
        for r in range(0, self.num_cities):
            for s in range(0, self.num_cities):
                sum += matrix[r][s]

        avg = sum / (self.num_cities * self.num_cities)
        return avg

import pickle
import sys
import traceback


def main(argv):  
    
    num_cities = 10                                     #Want to set default of num_cities to 10 [However the program crashes if the zeroth argument is not num_cities]

    if len(argv) >= 3 and argv[0]:              #If arguments are more than 3 take the zeroth argument as the number of cities request
        num_cities = int(argv[0])                       #num_cities = number of cities

    if num_cities <= 10:                                #If number of cities is 10 or less set variables na,num_iterations and num_repetitions
        num_ants = 20                                 #num_ants = number of ants?
        num_iterations = 12                                 #num_iterations = number of iterations
        num_repetitions = 1                                  #num_repetitions = number of repetitions
    else:
        num_ants = 28
        num_iterations = 20
        num_repetitions = 1

    stuff = pickle.load(open(argv[1], "r"))     #Load city info from filename(first argument) into stuff [we load unnecessary data]
    city_name = stuff[0]                           #city_name = 1d array of names of cities?
    city_distance = stuff[1]                               #city_distance = 2d array of distances between cities
    #why are we doing this?
    if num_cities < len(city_distance):                            #Remove unnecessary data of cities which are not included [note: we do not do this with city names]
        city_distance = city_distance[0:num_cities]
        for i in range(0, num_cities):
            city_distance[i] = city_distance[i][0:num_cities]


    try:                                        #If there is a exception in this section go to "except"
        graph = GraphBit(num_cities, city_distance)                #Initializes the Graphbit class
        best_path_vector = None
        best_path_cost = sys.maxint
        for i in range(0, num_repetitions):
            print "Repetition %s" % i
            graph.reset_pheromone()
            workers = BigGroup(graph, num_ants, num_iterations)   #Initializes the BigGroup class
            print "Colony Started"
            workers.start()
            if workers.best_path_cost < best_path_cost:
                print "Colony Path"
                best_path_vector = workers.best_path_vector
                best_path_cost = workers.best_path_cost

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (best_path_vector,)
        city_vector = []
        for city in best_path_vector:
            print city_name[city] + " ",
            city_vector.append(city_name[city])
        print "\nBest path cost = %s\n" % (best_path_cost,)
        results = [best_path_vector, city_vector, best_path_cost]
        pickle.dump(results, open(argv[2], 'w+'))
        return best_path_cost
    except Exception, e:
        print "exception: " + str(e)            #Print exception name
        traceback.print_exc()                   #Print out exception again in more detail


if __name__ == "__main__":                      #Only run this if it is the main program
    main(sys.argv[1:])
