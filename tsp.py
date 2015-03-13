import math
import random

class Work():
    def __init__(self, ID, start_node, colony):             #ID = i; start_node=random; colony = BigGroup
        self.ID = ID
        self.start_node = start_node
        self.grouping = colony
        self.curr_node = self.start_node
        self.graph = self.grouping.graph                    #graph = GraphBit
        self.path_vec = []
        self.path_vec.append(self.start_node)
        self.path_cost = 0
        self.Beta = 1.0
        self.Q0 = 0.5
        self.Rho = 0.99
        self.ntv = {}                                       #empty dictionary[a data structure that maps one value to another]
        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.ntv[i] = i                             #Changes ntv into a 1d array?
        self.path_mat = []
        for i in range(0, self.graph.num_nodes):
           self .path_mat.append([0] * self.graph.num_nodes)    #Creates path_mat as a num_node*num_node 2d array of 0s

    #could this be simpler?
    def run(self):
        graph = self.grouping.graph                         #graph = GraphBit. No need to redefine, could just refence as self.graph
        while not self.end():
            new_node = self.state_transition_rule(self.curr_node)
            self.path_cost += graph.delta(self.curr_node, new_node)
            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1 
            self.local_updating_rule(self.curr_node, new_node)
            self.curr_node = new_node
            print not self.end()
            print self.ntv
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])
        self.grouping.update(self)
        self.__init__(self.ID, self.start_node, self.grouping)

    def end(self):
        return not self.ntv                                 #self.ntv always equals 0? Returns 1?


    def state_transition_rule(self, curr_node):
        graph = self.grouping.graph
        q = random.random()
        max_node = -1
        if q < self.Q0:
            #print "Exploitation"
            max_val = -1
            val = None
            for node in self.ntv.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            #Bob was here
            #print "Exploration"
            sum = 0
            node = -1
            for node in self.ntv.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")
            avg = sum / len(self.ntv)
            #print "avg = %s" % (avg,)
            for node in self.ntv.values():
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if p > avg:
                    #print "p = %s" % (p,)
                    max_node = node
            if max_node == -1:
                max_node = node
        if max_node < 0:
            raise Exception("max_node < 0")
        del self.ntv[max_node]
        return max_node

    def local_updating_rule(self, curr_node, next_node):
        #Update the pheromones on the tau matrix to represent transitions of the ants
        graph = self.grouping.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)


import random
import sys



class BigGroup:
    def __init__(self, graph, num_ants, num_iterations):            #graph = GraphBit; num_ants = na, num_iterations = ni
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1
        self.reset()

    def reset(self):
        self.bpc = sys.maxint
        self.bpv = None
        self.bpm = None
        self.lbpi = 0

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

    def update(self, ant):
        print "Update called by %s" % (ant.ID,)
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.bpc:
            self.bpc = ant.path_cost
            self.bpm = ant.path_mat
            self.bpv = ant.path_vec
            self.lbpi = self.iter_counter
        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print "Best: %s, %s, %s, %s" % (
                self.bpv, self.bpc, self.iter_counter, self.avg_path_cost,)


    def done(self):
        return self.iter_counter == self.num_iterations

    def c_workers(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Work(i, random.randint(0, self.graph.num_nodes - 1), self)    #Initializes Work multiple times[with different randint]. Should change to initializing once and calling a function multiple times?
            ants.append(ant)

        return ants
 
    def global_updating_rule(self):
        #can someone explain this
        evaporation = 0
        deposition = 0
        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.bpm[r][s] / self.bpc
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau
                    self.graph.update_tau(r, s, evaporation + deposition)

class GraphBit:
    def __init__(self, num_nodes, delta_mat, tau_mat=None):     #num_nodes = nm =number of cities; delta_mat = cm = 2d array of distances between cities
        print len(delta_mat)
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")
        self.num_nodes = num_nodes
        self.delta_mat = delta_mat 
        if tau_mat is None:
            self.tau_mat = []                                   #Sets the size of 1d array tau_mat to the number of cities
            for i in range(0, num_nodes):
                self.tau_mat.append([0] * num_nodes)

    def delta(self, r, s):
        return self.delta_mat[r][s]

    def tau(self, r, s):
        return self.tau_mat[r][s]

    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    def update_tau(self, r, s, val):
        self.tau_mat[r][s] = val

    def reset_tau(self):
        avg = self.average_delta()
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)
        print "Average = %s" % (avg,)
        print "Tau0 = %s" % (self.tau0)
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0


    def average_delta(self):
        return self.average(self.delta_mat)


    def average_tau(self):
        return self.average(self.tau_mat)

    def average(self, matrix):
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

import pickle
import sys
import traceback


def main(argv):
    nm = 10                                     #Want to set default of nm to 10 [However the program crashes if the zeroth argument is not nm]

    if len(argv) >= 3 and argv[0]:              #If arguments are more than 3 take the zeroth argument as the number of cities request
        nm = int(argv[0])                       #nm = number of cities

    if nm <= 10:                                #If number of cities is 10 or less set variables na,ni and nr
        na = 20                                 #na = number of ants?
        ni = 12                                 #ni = number of iterations
        nr = 1                                  #nr = number of repetitions
    else:
        na = 28
        ni = 20
        nr = 1

    stuff = pickle.load(open(argv[1], "r"))     #Load city info from filename(first argument) into stuff [we load unnecessary data]
    cities = stuff[0]                           #cities = 1d array of names of cities?
    cm = stuff[1]                               #cm = 2d array of distances between cities
    #why are we doing this?
    if nm < len(cm):                            #Remove unnecessary data of cities which are not included [note: we do not do this with city names]
        cm = cm[0:nm]
        for i in range(0, nm):
            cm[i] = cm[i][0:nm]


    try:                                        #If there is a exception in this section go to "except"
        graph = GraphBit(nm, cm)                #Initializes the Graphbit class
        bpv = None
        bpc = sys.maxint
        for i in range(0, nr):
            print "Repetition %s" % i
            graph.reset_tau()
            workers = BigGroup(graph, na, ni)   #Initializes the BigGroup class
            print "Colony Started"
            workers.start()
            if workers.bpc < bpc:
                print "Colony Path"
                bpv = workers.bpv
                bpc = workers.bpc

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (bpv,)
        city_vec = []
        for node in bpv:
            print cities[node] + " ",
            city_vec.append(cities[node])
        print "\nBest path cost = %s\n" % (bpc,)
        results = [bpv, city_vec, bpc]
        pickle.dump(results, open(argv[2], 'w+'))
    except Exception, e:
        print "exception: " + str(e)            #Print exception name
        traceback.print_exc()                   #Print out exception again in more detail


if __name__ == "__main__":                      #Only run this if it is the main program
    main(sys.argv[1:])
