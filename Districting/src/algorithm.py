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
        #r.shuffle_list(nodes_copy)

        # Create clusters assigned the first n_cluster as centers
        for i in range(self.n_cluster):
            dmax = 0
            for j in range(len(nodes_copy)):
                dnode = nodes_copy[j].demand
                if dmax < dnode:
                    dmax=dnode
                    centro=j
            node = nodes_copy.pop(centro)    #Lo elimina
            cluster = Cluster(node)
            self.solution.clusters_list.append(cluster)

        while len(nodes_copy)>0:
            for cluster in self.solution.clusters_list:
                node_remove_id = -99
                if len(nodes_copy)>0:
                    dmin=1000000000
                    contador = 0
                    for node in nodes_copy:
                        center_id = cluster.center.id
                        node_id = node.id
                        distancia = self.solution.instance.distances[(center_id, node_id)]
                        if distancia<dmin:
                            dmin=distancia
                            node_remove_id = contador
                        contador += 1
                    cluster.node_list.append(nodes_copy.pop(node_remove_id))


        for cluster in self.solution.clusters_list:
             print("Cluster")
             for node in cluster.node_list:
                 print(node.id)

        # Computes cluster measurements (for each cluster)yony.ceballos@udea.edu.coyony.ceballos@udea.edu.co
        for cluster in self.solution.clusters_list:
            cluster.get_measures(self.solution.instance.distances)
