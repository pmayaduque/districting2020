import os
import utilities
import gmplot
from entities import Instance, Solution
from algorithm import Algorithm


if __name__ == "__main__":
    # Create random generator and set seed
    r = utilities.RandGenerator()
    r.set_seed(22)

    # Read Instance
    instance = utilities.read_instance_csv("data_small.csv")
    #instance = utilities.read_instance("instance_small.txt") # Deprecated
    print("Instance has been read")

    # Compute distances
    instance.compute_dist("default")
    print("Distances have been calculated")

    # Create a random solution
    solution = Solution(instance)
    algorithm = Algorithm(6, solution)
    algorithm.random_sol()
    print("Solution has been created")

    # Get objective functions
    print(solution.get_objvalue("sumAllToCenter"))
    print(solution.get_objvalue("sumAllToAll"))
    print(solution.get_objvalue("loadRange"))
    print("Objective function has been calculated")

    # Print clusters
    map = utilities.MapVisualiser()
    # Set key google API
    # Read documentation of ggogle API to get your own key
    #map.set_gmapkey("1AIzaSyBrcChgM41NgYRy7FL4oXoxkz6KJbrKyJY")
    map.draw_cluster(solution)












