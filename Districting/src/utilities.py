import os
import gmplot
from entities import Instance, Node, Solution
from random import seed, randint, random, shuffle



def read_instance(filename, filepath =os.path.dirname(os.getcwd()) + "/data/"):
    """
    Read the data of the instances

    See the template doc file to understand the structure of the file

    Parameters:
        filename (str): name of the file to read including extension
        filepath (str, optional): path to the directory
            default is "data" folder in project env
    """

    # Creates instance object
    instance = Instance()
    f = open(filepath + filename, "r")
    # Read first line -> name
    f1 = f.readline()
    splitted_line = f1.split()
    instance.name = splitted_line[1]
    # Omit second line
    f1 = f.readline()
    # Read third line -> number of nodes
    f1 = f.readline()
    splitted_line = f1.split()
    instance.nNodes = int(splitted_line[1])
    # Omit next line
    f1 = f.readline()
    # Read nodes information
    for i in range(instance.nNodes):
        f1 = f.readline()
        splitted_line = f1.split()
        node = Node(int(splitted_line[0]),
                    float(splitted_line[1]),
                    float(splitted_line[2]),
                    float(splitted_line[3]),)
        instance.nodes.append(node)

    return instance


class RandGenerator:
    """
     Pythonic Singleton to generate random numbers

     See the template doc file to understand the structure of the file
    """

    class __impl:
        random = random

        def set_seed(self, seedr):
            """
            A method that fixes the seed of the random generator

            Args:
                seedr (int): random seed
            """
            seed(seedr)

        def generate_float(self):
            """
            A method that generates a random float number

            Returns:
                value (long): random number
            """

            value = random()
            return value

        def gen_int(self, up_value):
            """
            A method that generates a random float number

            Args:
                up_value (int): uper limit for the random generation function

            Returns:
                value (int): random integer number between 0 and up_value
            """

            value = randint(0, up_value)
            return value

        def shuffle_list(self, list):
            return shuffle(list)

    # The private class attribute holding the "one and only instance"
    __instance = __impl(  )

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


class MapVisualiser:
    """
        A class that display a solution in a map

        Attributes:
            gmap_key (string): Key to be used in google API
    """

    def __init__(self):
        self.gmap_key = " "

    def set_gmapkey(self, key):
        """
            Method to set the key to be used by google API

            Args:
                key (string): google API key
        """
        self.gmap_key = key

    def draw_cluster(self, solution):
        """
            Method to display cluster on the map

            Args:
                solution (:obj:'Solution'): solution to be displayed on the map
        """
        # get the coordinates of the first cluster to center the map on it
        focus_lat = solution.clusters_list[0].center.lat
        focus_long = solution.clusters_list[0].center.long

        # Creates a map object
        gmap3 = gmplot.GoogleMapPlotter(focus_lat, focus_long, 12.9)
        gmap3.apikey = self.gmap_key

        # Prints clusters
        count_colors = 0
        for cluster in solution.clusters_list:
            color_id = count_colors % len(colors)
            latitude_list = []
            longitude_list = []
            for node in cluster.node_list:
                latitude_list.append(node.lat)
                longitude_list.append(node.long)
            gmap3.scatter(latitude_list, longitude_list, colors[color_id], size=90, marker=False)
            count_colors += 1

        gmap3.draw(os.path.dirname(os.getcwd()) + "/maps/map.html")

# Pallet of colours
colors =["#6495ED",
"#228B22",
"#B22222",
"#D2691E",
"#4169E1",
"#0000CD",
"#9ACD32",
"#7B68EE",
"#FF69B4",
"#800000",
"#FFFF00",
"#008000",
"#00FFFF",
"#BC8F8F",
"#FF00FF",
"#696969",
"#D2B48C",
"#FFB6C1",
"#A9A9A9",
"#32CD32",
"#FFD700",
"#DAA520",
"#CD5C5C",
"#DB7093",
"#FF7F50",
"#808000",
"#FFFFE0",
"#6A5ACD",
"#BA55D3",
"#8B4513",
"#A52A2A",
"#FF1493",
"#00FA9A",
"#006400",
"#EEE8AA",
"#FFEFD5",
"#FAF0E6",
"#8B008B",
"#F0F8FF",
"#A0522D",
"#87CEEB",
"#808080",
"#5F9EA0",
"#2F4F4F",
"#FFA07A",
"#BDB76B",
"#FFFFF0",
"#483D8B",
"#DEB887",
"#6B8E23",
"#FFFAF0",
"#B8860B",
"#FFF8DC",
"#00BFFF",
"#DC143C",
"#B0C4DE",
"#F5FFFA",
"#00CED1",
"#FDF5E6",
"#FFFF00",
"#F5DEB3",
"#9932CC",
"#8B0000",
"#FFC0CB",
"#87CEFA",
"#F0FFFF",
"#FA8072",
"#00008B",
"#FAFAD2",
"#ADD8E6",
"#008080",
"#FF6347",
"#FFFAFA",
"#00FF7F",
"#AFEEEE",
"#9370DB",
"#7FFF00",
"#00FF00",
"#778899",
"#98FB98",
"#4682B4",
"#FFFACD",
"#9400D3",
"#FF8C00",
"#FF0000",
"#8FBC8F",
"#CD853F",
"#708090",
"#F5F5F5",
"#F4A460",
"#1E90FF",
"#FFEBCD",
"#2E8B57",
"#8A2BE2",
"#20B2AA",
"#FFA500",
"#191970",
"#F08080",
"#E0FFFF",
"#EE82EE",
"#90EE90",
"#F5F5DC",
"#FF4500",
"#3CB371",
"#40E0D0",
"#800080",
"#556B2F",
"#FFF5EE",
"#008B8B",
"#C71585",
"#F0E68C",
"#0000FF",
"#C0C0C0",
"#4B0082",
"#D8BFD8",
"#48D1CC"]