
import random
import sys
import work
import variables


class BigGroup:
    def __init__(self, graph, num_ants, num_iterations, num_repetitions, completed_repetitions):            #graph = GraphBit; num_ants = na, num_iterations = num_iterations
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

    def number_of_ants(self):                                         
        return len(self.ants)

    def number_of_iterations(self):
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
            print "%s %%" % ((float(self.iter_counter)/(self.num_iterations*self.num_repetitions)+float(self.completed_repetitions)/self.num_repetitions)*100)
            #print "Best: %s, %s, %s, %s" % (self.best_path_vector, self.best_path_cost, self.iter_counter, self.avg_path_cost,)


    def done(self):                                                             #Never used. Consider removing
        return self.iter_counter == self.num_iterations

    def c_workers(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = work.Work(i, random.randint(0, self.graph.num_cities - 1), self)    #Initializes Work multiple times[with different randint]. Should change to initializing once and calling a function multiple times?
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
