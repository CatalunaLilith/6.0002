# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge
import pdb

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
    # the nodes represent buildings
    # the edges represent a path between two nodes/buildings
    # a weighted edge represents the path with weights of (total distance, outside distance)
    # this is a digraph; each edge is unidirectional 
    # (of course there can be edges from a to b AND b to a.
    #  Those two edges ab and ba may have diffrent weights.)
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    
    print("Loading map from file...")
    #load file
    map_file = open(map_filename, "r")
    #split file into list of strings for eachline, which is 4 numbers seperated by space
    lines = []
    for line in map_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    map_file.close()
    # print(lines) #TODO delete
    adigraph = Digraph()
    #make values_list of line.split() at space
    map_values = []
    for elem in lines:
        an_elem = elem.split()
        map_values.append(an_elem)
    for elem in map_values:
        if adigraph.has_node(elem[0]) == False:
            adigraph.add_node(elem[0])
        if adigraph.has_node(elem[1]) == False:
            adigraph.add_node(elem[1])
        if elem:
            adigraph.add_edge(WeightedEdge(elem[0], elem[1], elem[2], elem[3]))
    return adigraph 

# load_map("mit_map.txt")
 

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# print(load_map("test_load_map.txt"))
# a->b (10, 9) 
# a->c (12, 2)
# b->c (1, 1) 

# print(load_map("mit_map.txt"))

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#     the objective us the find the shortest valid path between two given nodes. 
#     A valid path is a series of nodes, such that there exists an edge connecting each consecutive node
#     Each path has two weights, the TDT(total distance traveled) and DO (distance outdoors)
#     The shortest valid path is the valid path with the lowest TDT.
#     This is constrained by a maximum DO (an arbitrary number). 

agraph = Digraph()
agraph.add_node("a")
agraph.add_node("b")
agraph.add_node("c")
agraph.add_node("d")
agraph.add_node("e")

an_edge = WeightedEdge("a", "b", 15, 10)
an_edge2 = WeightedEdge("a", "c", 20, 12)
an_edge3 = WeightedEdge("a", "d", 40, 20)
# an_edge4 = WeightedEdge("b", "d", 40, 20)
# an_edge5 = WeightedEdge("d", "e", 10, 7)
# an_edge6 = WeightedEdge("b", "e", 55, 20)
agraph.add_edge(an_edge)
agraph.add_edge(an_edge2)
agraph.add_edge(an_edge3)
# agraph.add_edge(an_edge4)
# agraph.add_edge(an_edge5)
# agraph.add_edge(an_edge6)

def total_distance_of_path(graph, path):
    """assummes path is a list of nodes
    returns an int, the sum of the distance of the edges connecting the nodes
    """
    if not path:
        return 0
    apath = path.copy()
    sum = 0 
    while len(apath) > 1:
        node1 = apath[0]
        node2 = apath[1]
        edges= graph.edges.values()
        for elem in edges:
            for edge in elem:
                edge_source = edge.src
                edge_dest = edge.dest
                if (edge_source == node1) and (edge_dest == node2):
                    sum += edge.total_distance
        del apath[0]
    return sum

def outdoor_distance_of_path(graph, path):
    """assummes path is a list of nodes
    returns an int, the sum of the distance of the edges connecting the nodes
    """
    if not path:
        return 0
    apath = path.copy()
    sum = 0 
    while len(apath) > 1:
        node1 = apath[0]
        node2 = apath[1]
        edges= graph.edges.values()
        for elem in edges:
            for edge in elem:
                edge_source = edge.src
                edge_dest = edge.dest
                if (edge_source == node1) and (edge_dest == node2):
                    sum += edge.outdoor_distance
        del apath[0]
    return sum

    
# distance_of_path(agraph, ['a','b','d'])


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    pdb.set_trace()
    path = path + [start]
    if start == end:
        return path
    try:
        start_edges = digraph.get_edges_for_node(start)
    except:
        print("you are at end point in graph ")
        return path
    #TODO add case where no valid path exists 
    for edge in start_edges: #edges associated with node 
        node = edge.get_destination()
        if node not in path: #avoid cycles
            if (best_path == None) or (total_distance_of_path(digraph, path) < total_distance_of_path(digraph, best_path)): #starts recursive calling with updated path
                new_path = get_best_path(digraph, node, end, path, max_dist_outdoors, best_dist, best_path)
                if (new_path != None) and (outdoor_distance_of_path(digraph, new_path) <= max_dist_outdoors) and (total_distance_of_path(digraph, new_path) <= total_distance_of_path(digraph, best_path)):
                    best_path = new_path
                    best_dist = total_distance_of_path(digraph, new_path)
        else:
            print('Already visited', node)
            #raise an error?
    print(best_path)
    return best_path


# TODO test case with no valid path
    # return None
# TODO test case with 2 valid paths, 
#     return shorter path
# TODO test case with 2 valid paths, shorter is over outside limit
#     return longer path that conforms to outside limit
# TODO test case with a loop
#     should go through loop exactly once
    
    
"""
if start and end are not valid nodes: raise an error 
elif start and end are the same node: update the global variables appropriately 
else: for all the child nodes of start construct a path including that node recursively solve the rest of the path, from the child node to the end node return the shortest path
"""


def innitiate_get_shortest_path(digraph, start, end, max_dist_outdoors):
    """used to start the get_shortest_path recursive function"""
    if (start not in digraph.nodes) or (end not in digraph.nodes):
        raise ValueError ("This node does not exist")
    return get_best_path(digraph, start, end, [], max_dist_outdoors, None, None)

# print(innitiate_get_shortest_path(agraph, "a", "b", 150))

innitiate_get_shortest_path(agraph, "a", "b", 150)



# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    pass


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

# class Ps2Test(unittest.TestCase):
#     LARGE_DIST = 99999

#     def setUp(self):
#         self.graph = load_map("mit_map.txt")

#     def test_load_map_basic(self):
#         self.assertTrue(isinstance(self.graph, Digraph))
#         self.assertEqual(len(self.graph.nodes), 37)
#         all_edges = []
#         for _, edges in self.graph.edges.items():
#             all_edges += edges  # edges must be dict of node -> list of edges
#         all_edges = set(all_edges)
#         self.assertEqual(len(all_edges), 129)

#     def _print_path_description(self, start, end, total_dist, outdoor_dist):
#         constraint = ""
#         if outdoor_dist != Ps2Test.LARGE_DIST:
#             constraint = "without walking more than {}m outdoors".format(
#                 outdoor_dist)
#         if total_dist != Ps2Test.LARGE_DIST:
#             if constraint:
#                 constraint += ' or {}m total'.format(total_dist)
#             else:
#                 constraint = "without walking more than {}m total".format(
#                     total_dist)

#         print("------------------------")
#         print("Shortest path from Building {} to {} {}".format(
#             start, end, constraint))

#     def _test_path(self,
#                    expectedPath,
#                    total_dist=LARGE_DIST,
#                    outdoor_dist=LARGE_DIST):
#         start, end = expectedPath[0], expectedPath[-1]
#         self._print_path_description(start, end, total_dist, outdoor_dist)
#         dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
#         print("Expected: ", expectedPath)
#         print("DFS: ", dfsPath)
#         self.assertEqual(expectedPath, dfsPath)

#     def _test_impossible_path(self,
#                               start,
#                               end,
#                               total_dist=LARGE_DIST,
#                               outdoor_dist=LARGE_DIST):
#         self._print_path_description(start, end, total_dist, outdoor_dist)
#         with self.assertRaises(ValueError):
#             directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

#     def test_path_one_step(self):
#         self._test_path(expectedPath=['32', '56'])

#     def test_path_no_outdoors(self):
#         self._test_path(
#             expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

#     def test_path_multi_step(self):
#         self._test_path(expectedPath=['2', '3', '7', '9'])

#     def test_path_multi_step_no_outdoors(self):
#         self._test_path(
#             expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

#     def test_path_multi_step2(self):
#         self._test_path(expectedPath=['1', '4', '12', '32'])

#     def test_path_multi_step_no_outdoors2(self):
#         self._test_path(
#             expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
#             outdoor_dist=0)

#     def test_impossible_path1(self):
#         self._test_impossible_path('8', '50', outdoor_dist=0)

#     def test_impossible_path2(self):
#         self._test_impossible_path('10', '32', total_dist=100)


# if __name__ == "__main__":
#     unittest.main()
