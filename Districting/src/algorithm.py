import copy
from entities import Cluster
from utilities import RandGenerator


class Algorithm:
    """
    A class that compiles the algorithms to build a solution

    Attributes:
        n_cluster (int): Number of cluster that the solution must have
        solution (:obj:'Solution'): solution to be built by the algorithm

    Args:
        n_cluster (int): Number of cluster that the solution must have
        solution (:obj:'Solution'): solution to be built by the algorithm
    """

    def __init__(self, n_cluster, solution):
        self.solution = solution
        self.n_cluster = n_cluster

    def random_sol(self):
        """
        A method to compute a random solution
        """
        # TODO: this can be done simpler but needs to take into account
        #    that the solution has to replicable

        # Fetch instance of random generator
        r = RandGenerator()

        # Creates a deep copy of list of nodes
        nodes_copy = copy.deepcopy(self.solution.instance.nodes)
        # order the copied list randomly
        r.shuffle_list(nodes_copy)

        # Create clusters assigned the first n_cluster as centers
        for i in range(self.n_cluster):
            node = nodes_copy.pop(0)
            cluster = Cluster(node)
            self.solution.clusters_list.append(cluster)

        # Assigns the remaining nodes to the clusters
        count = 0
        while len(nodes_copy) > 0:
            node = nodes_copy.pop(0)
            id_cluster = count % self.n_cluster
            self.solution.clusters_list[id_cluster].node_list.append(node)
            count += 1

        # Computes cluster measurements
        for cluster in self.solution.clusters_list:
            cluster.get_measures(self.solution.instance.distances)

