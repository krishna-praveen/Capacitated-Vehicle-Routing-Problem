import unittest
import math
from nsga_vrp.utils import calculate_distance
from nsga_vrp.NSGA2_vrp import load_instance, routeToSubroute, getRouteCost


class TestRoute(unittest.TestCase):

    # Run test_distance function which will calculate distance between two
    #   customers we have selected.

    def test_route(self):
        # To test if the route given is being divided into correct subroutes
        loaded_instance = load_instance('./data/json/Input_Data.json')
        sample_individual = [19, 5, 24, 7, 16, 23, 22, 2, 12, 8, 20, 25, 21, 18, 11, 15, 1, 14, 17, 6, 4, 13, 10, 3, 9]
        # Route of sample_individual should be like this
        sample_individual_subroutes = [[19, 5, 24, 7], [16, 23, 22], [2, 12, 8], [20, 25, 21], [18, 11, 15], [1, 14, 17, 6, 4], [13, 10, 3, 9]]
        calculated_subroute = routeToSubroute(sample_individual, loaded_instance)
        self.assertEqual(sample_individual_subroutes, calculated_subroute)



    def test_subroute_distance(self):
        # To test if for given sub route distance is being calculated correctly
        loaded_instance = load_instance('./data/json/Input_Data.json')
        sample_individual = [19, 5, 24, 7, 16, 23, 22, 2, 12, 8, 20, 25, 21, 18, 11, 15, 1, 14, 17, 6, 4, 13, 10, 3, 9]
        sample_individual_subroutes = routeToSubroute(sample_individual, loaded_instance)
        # Getting the first subroute divided by routeToSubroute
        first_subroute = sample_individual_subroutes[0]
        # Our first subroute is [19,5,24,7]
        # Calculating the distance of the route 0 -> 19 -> 5 -> 24 -> 7 -> 0
        # Getting coordinates of each of these customer places and finding Euclidean distance
        manual_calculation = math.sqrt((40 - 15) ** 2 + (50 - 80) ** 2) + \
                             math.sqrt((15 - 42) ** 2 + (80 - 65) ** 2) + \
                             math.sqrt((42 - 25) ** 2 + (65 - 50) ** 2) + \
                             math.sqrt((25 - 40) ** 2 + (50 - 66) ** 2) + \
                             math.sqrt((40 - 40) ** 2 + (66 - 50) ** 2)

        calculated_distance = getRouteCost(first_subroute, loaded_instance, unit_cost=1)
        self.assertEqual(manual_calculation, calculated_distance)


    def test_route_distance(self):
        # To test if given route distance is being calculated correctly
        # Now to test multiple subroutes
        loaded_instance = load_instance('./data/json/Input_Data.json')
        sample_individual = [19, 5, 24, 7, 16, 23, 22, 2, 12, 8, 20, 25, 21, 18, 11, 15, 1, 14, 17, 6, 4, 13, 10, 3, 9]
        sample_individual_subroutes = routeToSubroute(sample_individual, loaded_instance)
        # Getting the first subroute divided by routeToSubroute
        first_subroute = sample_individual_subroutes[0]
        second_subroute = sample_individual_subroutes[1]
        # Our first subroute is [19,5,24,7]
        # Our second subroute is [16,23,22]

        # Calculating the distance of the route 0 -> 19 -> 5 -> 24 -> 7 -> 0
        # Getting coordinates of each of these customer places and finding Euclidean distance
        manual_first_dist =  math.sqrt((40 - 15) ** 2 + (50 - 80) ** 2) + \
                             math.sqrt((15 - 42) ** 2 + (80 - 65) ** 2) + \
                             math.sqrt((42 - 25) ** 2 + (65 - 50) ** 2) + \
                             math.sqrt((25 - 40) ** 2 + (50 - 66) ** 2) + \
                             math.sqrt((40 - 40) ** 2 + (66 - 50) ** 2)

        # Calculating the distance of the route 0 -> 16 -> 23 -> 22 ->0
        manual_second_dist = math.sqrt((40 - 20) ** 2 + (50 - 85) ** 2) + \
                             math.sqrt((20 - 28) ** 2 + (85 - 55) ** 2) + \
                             math.sqrt((28 - 28) ** 2 + (55 - 52) ** 2) + \
                             math.sqrt((28 - 40) ** 2 + (52 - 50) ** 2)

        Total_manual_dist = manual_first_dist + manual_second_dist
        calculated_distance = getRouteCost(first_subroute+second_subroute, loaded_instance, unit_cost=1)
        self.assertEqual(Total_manual_dist, calculated_distance)



if __name__ == '__main__':
    unittest.main()