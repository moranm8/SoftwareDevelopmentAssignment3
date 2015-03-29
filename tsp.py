#Exam No. B067718
#This program solves the travelling salesman problem using ant colony optimisation


import pickle
import sys
import traceback
import graphBit
import bigGroup
import variables


def main(argv):  

    if len(argv) >= 3:              #Take command line arguments as variables if they are provided
        num_cities = int(argv[0])
        input_file = argv[1]
        output_file = argv[2]
        print "Using command line options\nNumber of cities: %s\nInput file: %s\nOutput file: %s" % (num_cities, input_file, output_file)
    else:
        num_cities = variables.default_num_cities                       #Otherwise take variables from file
        input_file = variables.default_input_file
        output_file = variables.default_output_file
        print "Not enough command line options \nUsing values from variables.py: \nNumber of cities: %s\nInput file: %s\nOutput file: %s" % (num_cities, input_file, output_file)
    if num_cities <= 1:
        raise Exception("Specified too few cities")

    if num_cities <= 10:                                #Variables chosen depends on the number of cities in simulation
        num_ants = variables.small_num_ants                               
        num_iterations = variables.small_num_iterations
        num_repetitions = variables.small_num_repetitions                               
    else:
        num_ants = variables.large_num_ants
        num_iterations = variables.large_num_iterations
        num_repetitions = variables.large_num_repetitions
        

    cities = pickle.load(open(input_file, "r"))     #The input file should contain the names of the cities as well as the distances between them
    city_name = cities[0]                           
    city_distance = cities[1]                               
    #why are we doing this?
    if num_cities < len(city_distance):                            #Remove unnecessary data of cities which are not included
        city_distance = city_distance[0:num_cities]
        for i in range(0, num_cities):
            city_distance[i] = city_distance[i][0:num_cities]


    try:                                        
        graph = graphBit.GraphBit(num_cities, city_distance)                
        best_path_vector = None
        best_path_cost = sys.maxint
        for i in range(0, num_repetitions):
            graph.reset_pheromone()
            workers = bigGroup.BigGroup(graph, num_ants, num_iterations, num_repetitions, i)
            workers.start()
            if workers.best_path_cost < best_path_cost:
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
        pickle.dump(results, open(output_file, 'w+'))
        return best_path_cost
    except Exception, e:
        print "exception: " + str(e)            #Print exception name
        traceback.print_exc()                   #Print out exception again in more detail


if __name__ == "__main__":
    main(sys.argv[1:])
