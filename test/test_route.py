import unittest
import math
from nsga_vrp.utils import calculate_distance
from nsga_vrp.NSGA2_vrp import load_instance


class TestRoute(unittest.TestCase):

    # Run test_distance function which will calculate distance between two
    #   customers we have selected.

    def test_distance(self):
        loaded_instance = load_instance("./data/json/Input_Data.json")
        cust7, cust8 = loaded_instance["customer_7"], loaded_instance["customer_8"]
        calculated_result = calculate_distance(cust7, cust8)
        math_result = math.sqrt((40-38)**2 + (66-68)**2)
        self.assertEqual(calculated_result, math_result)

    def test_route(self):
        # To test if the route given is being divided into correct subroutes
        pass

    def test_subroute_distance(self):
        # To test if for given sub route distance is being calculated correctly
        pass

    def test_route_distance(self):
        # To test if given route distance is being calculated correctly
        pass

if __name__ == '__main__':
    unittest.main()