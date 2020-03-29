import os
import numpy as np
from geopy.distance import distance, geodesic, great_circle
import utilities


class Instance:
    """
    A class used that keeps all the information of the instance

    Attributes:
        name (str): Name of the instance including extension
        nNodes (int): Number of nodes
        nodes (:obj:`list` of :obj:`Nodes`): List of nodes
        distances (:obj:`dict` of :obj:`Nodes`): Dictionary of distances
    """

    def __init__(self):
        self.name = " " # name of the instance
        self.nNodes = 0 # Number of nodes
        self.nodes = []  # List of nodes
        self.distances = {}  # Matrix of distances

    def compute_dist(self, dist_function):
        """
        A method to compute the distances between each pair of nodes

        It uses a dictionary of distance functions.
        The user chooses one function type

        Args:
            dist_function (str): Define the type of distance to be computed
                default
                geodesic

        Attributes:
            functions: (:obj:'dict' of :obj:'Node'): Dictionary of type of distance functions
        """

        def default_dist(coord1, coord2):
            """
            A function to compute the distances between each pair of nodes
            using the default distance type

            Args:
                coord1 (long): latitude
                coord2 (long): longitude

            Returns:
                d (long): distance
            """

            d = distance((node1.lat, node1.long), (node2.lat, node2.long)).m
            return d

        def geodesic_dist(coord1, coord2):
            """
            A function to compute the distances between each pair of nodes
            using the geodesic type

            Args:
                coord1 (long): latitude
                coord2 (long): longitude

            Returns:
                d (long): distance
            """

            d = geodesic((node1.lat, node1.long), (node2.lat, node2.long)).m
            return d

        functions = {
            'default':  default_dist,
            'geodesic': geodesic_dist
        }

        # computes the distance for each pair of nodes
        for node1 in self.nodes:
            for node2 in self.nodes:
                d = functions[dist_function]((node1.lat, node1.long), (node2.lat, node2.long))
                key = (node1.id, node2.id)
                self.distances[key] = d

    def read_dist(self, filename, filepath =os.path.dirname(os.getcwd()) + "/data/"):
        """
            Write code  here to read distances from file
        """


class Node:
    """
    A class used that represent a node or point of demand

    Attributes:
        id (int): Consecutive number that identify the nodes
        lat (int): Latitude
        long (int): Longitude
        demand (long): demand or load parameter of the node
    """

    def __init__(self, id, lat=0, long=0, demand = 0):
        self.id = id
        self.lat = lat
        self.long = long
        self.demand = demand


class Cluster:
    """
    A class used that represent a node or point of demand

    Attributes:
        center (:obj:'Node'): Center of the cluster
        node_list (:obj:'list' of :obj:'Node'): list of nodes assigned to the cluster
        distAllToAll (:obj:'list' of :obj:'long'): list of distances between each pair
            of nodes in the cluster
        distAllToCent (:obj:'list' of :obj:'long'): list of distances between each node
            and the center
        load (int): sum of demand or load of all nodes in the cluster
    """

    def __init__(self, center):
        self.center = center
        self.node_list = []
        self.node_list.append(center)
        self.distAllToAll = []
        self.distAllToCent = []
        self.load = 0

    def get_measures(self, distances):
        """
        Method that computes performance measures of the cluster

        Args:
            distances (:obj:`dict` of :obj:`Nodes`): Dictionary of distances
        """
        # Distances all to center
        for node_id in self.node_list:
            self.distAllToCent.append(distances[(self.center.id, node_id.id)])

        # Distances all pair of nodes
        # It assumes non symmetric distances but also work for symmetric
        for node1 in self.node_list:
            for node2 in self.node_list:
                self.distAllToAll.append(distances[(node1.id, node2.id)])

        # get cluster load
        for node in self.node_list:
            self.load += node.demand
        # Same but using np
        # self.load = np.sum([node.demand for node in self.node_list])


class Solution:
    """
    A class used that represent a solution of the problem

    Attributes:
        instance (:obj:'Instance'): instance to wich the solution belongs
        nClusters (int): number of clusters
        clusters_list (:obj:'list' of :obj:'Cluster'): list of clusters
        objectiveValue (long): Objective value of the solution.
            Different objective functions can be evaluated
            sum_alltocenter: sum of all paired distances
            sum_alltoall: sum of distances from center to all nodes
            load_range: Maximum load - minimum load
    """
    def __init__(self, instance):
        self.instance = instance
        self.nClusters = 0
        self.clusters_list =[]
        self.objectiveValue = 0

    def get_objvalue(self, obj_function):
        """
        Method that computes performance measures of the cluster

        Args:
            obj_function (str): Define the type of function to be computed
        """

        def sum_alltocenter():
            """
            A function that sums the distances between the center and each node

            Returns:
                s (long): sum of distance
            """

            # TODO: use numpy to compute it
            s = 0
            for cluster in self.clusters_list:
                s += np.sum(cluster.distAllToCent)
            return s

        def sum_alltoall():
            """
            A function that sums distances between each pair of nodes of the cluster

            Returns:
                s (long): sum of distance
            """

            # TODO: use numpy to compute it
            s = 0
            for cluster in self.clusters_list:
                s += np.sum(cluster.distAllToAll)
            return s

        def load_range():
            """
            A function computes the difference between the maximum and minimum load

            Returns:
                load_range (long): difference between the maximum and minimum load
            """

            load_max = self.load = np.max([cluster.load for cluster in self.clusters_list])
            load_min = self.load = np.min([cluster.load for cluster in self.clusters_list])
            return load_max - load_min

        # Dictionary that compiles options for the objective function
        functions = {
            'sumAllToCenter': sum_alltocenter,
            'sumAllToAll': sum_alltoall,
            'loadRange': load_range
        }

        # computes the objective with the given objective function
        obj = functions[obj_function]()

        return obj




