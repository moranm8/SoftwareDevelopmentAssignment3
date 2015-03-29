#This module contains important matrices which are used in ant colony optimistaions

class GraphBit:
    def __init__(self, num_cities, city_distance, pheromone_matrix=None):
        #print len(city_distance)
        if len(city_distance) != num_cities:
            raise Exception("len(city_distance) != num_cities")
        self.num_cities = num_cities
        self.city_distance = city_distance 
        if pheromone_matrix is None:
            self.pheromone_matrix = []
            for i in range(0, num_cities):
                self.pheromone_matrix.append([0] * num_cities)

    def distance(self, r, s):
        return self.city_distance[r][s]

    def pheromone(self, r, s):
        return self.pheromone_matrix[r][s]

    def etha(self, r, s):
        return 1.0 / self.distance(r, s)

    def update_pheromone(self, r, s, val):
        self.pheromone_matrix[r][s] = val

    def reset_pheromone(self):
        avg = self.average_distance()
        self.pheromone0 = 1.0 / (self.num_cities * 0.5 * avg)
        for r in range(0, self.num_cities):
            for s in range(0, self.num_cities):
                self.pheromone_matrix[r][s] = self.pheromone0


    def average_distance(self):
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