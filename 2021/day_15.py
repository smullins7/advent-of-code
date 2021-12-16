#!/usr/bin/env python3
import sys  # Library for INT_MAX
from collections import defaultdict

from lib_inputs import to_grid, Grid, Cell


def grow_row(existing_row, start):
    offset = len(existing_row)
    existing_row.extend(
        [Cell(i + offset, c.y, 1 if c.value == 9 else c.value + 1) for i, c in enumerate(existing_row[start:])])


def part_two(input_grid):
    new_grid = Grid([])

    for row in input_grid.rows:
        length = len(row)
        for i in range(4):
            grow_row(row, i * length)

        new_grid.rows.append(row)

    length = len(new_grid.rows)
    for i in range(4):
        for row in new_grid.rows[length * i:]:
            new_grid.rows.append([Cell(c.x, len(new_grid.rows), 1 if c.value == 9 else c.value + 1) for c in row])

    class Graph:
        def __init__(self, adjac_lis):
            self.adjac_lis = adjac_lis

        def get_neighbors(self, v):
            return self.adjac_lis[v]

        def a_star_algorithm(self, start, stop):
            # In this open_lst is a lisy of nodes which have been visited, but who's
            # neighbours haven't all been always inspected, It starts off with the start
            # node
            # And closed_lst is a list of nodes which have been visited
            # and who's neighbors have been always inspected
            open_lst = set([start])
            closed_lst = set([])

            # poo has present distances from start to all other nodes
            # the default value is +infinity
            poo = {}
            poo[start] = 0

            # par contains an adjac mapping of all nodes
            par = {}
            par[start] = start

            while len(open_lst) > 0:
                n = None

                # it will find a node with the lowest value of f() -
                for v in open_lst:
                    if n == None or poo[v] < poo[n]:
                        n = v;

                if n == None:
                    print('Path does not exist!')
                    return None

                # if the current node is the stop
                # then we start again from start
                if n == stop:
                    reconst_path = []

                    while par[n] != n:
                        reconst_path.append(n)
                        n = par[n]

                    reconst_path.append(start)

                    reconst_path.reverse()

                    # print('Path found: {}'.format(reconst_path))
                    return reconst_path

                # for all the neighbors of the current node do
                for m in self.get_neighbors(n):
                    # if the current node is not presentin both open_lst and closed_lst
                    # add it to open_lst and note n as it's par
                    if m not in open_lst and m not in closed_lst:
                        open_lst.add(m)
                        par[m] = n
                        poo[m] = poo[n] + m.value

                    # otherwise, check if it's quicker to first visit n, then m
                    # and if it is, update par data and poo data
                    # and if the node was in the closed_lst, move it to open_lst
                    else:
                        if poo[m] > poo[n] + m.value:
                            poo[m] = poo[n] + m.value
                            par[m] = n

                            if m in closed_lst:
                                closed_lst.remove(m)
                                open_lst.add(m)

                # remove n from the open_lst, and add it to closed_lst
                # because all of his neighbors were inspected
                open_lst.remove(n)
                closed_lst.add(n)

            print('Path does not exist!')
            return None

    adjacency_list = defaultdict(list)
    for row in new_grid.rows:
        for cell in row:
            adjacency_list[cell].extend(new_grid.find_neighbors(cell))
    graph1 = Graph(adjacency_list)
    the_path = graph1.a_star_algorithm(new_grid.rows[0][0], new_grid.rows[-1][-1])
    return sum([c.value for c in the_path[1:]])


def part_one(input_grid):
    class Graph(object):
        def __init__(self, my_grid, nodes, init_graph):
            self.my_grid = my_grid
            self.nodes = nodes
            self.graph = init_graph  # self.construct_graph(nodes, init_graph)

        def construct_graph(self, nodes, init_graph):
            '''
            This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
            '''
            graph = {}
            for node in nodes:
                graph[node] = {}

            graph.update(init_graph)

            for node, edges in graph.items():
                for adjacent_node, value in edges.items():
                    if graph[adjacent_node].get(node, False) == False:
                        graph[adjacent_node][node] = value

            return graph

        def get_nodes(self):
            "Returns the nodes of the graph."
            return self.nodes

        def get_outgoing_edges(self, node):
            "Returns the neighbors of a node."

            # connections = []
            # for out_node in self.nodes:
            #    if self.graph[node].get(out_node, False) != False:
            #        connections.append(out_node)
            # return connections

            return

        def value(self, node1, node2):
            "Returns the value of an edge between two nodes."
            return self.graph[node1][node2]

    def dijkstra_algorithm(graph, start_node):
        unvisited_nodes = list(graph.get_nodes())

        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        shortest_path = {}

        # We'll use this dict to save the shortest known path to a node found so far
        previous_nodes = {}

        # We'll use max_value to initialize the "infinity" value of the unvisited nodes
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        # However, we initialize the starting node's value with 0
        shortest_path[start_node] = 0

        # The algorithm executes until we visit all nodes
        while unvisited_nodes:
            # The code block below finds the node with the lowest score
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = graph.my_grid.find_neighbors(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + neighbor.value  # (current_min_node, neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

            # After visiting its neighbors, we mark the node as "visited"
            unvisited_nodes.remove(current_min_node)

        return previous_nodes, shortest_path

    def print_result(previous_nodes, shortest_path, start_node, target_node):
        path = []
        node = target_node

        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        # Add the start node manually
        path.append(start_node)

        # print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
        return sum([cell.value for cell in path])

    nodes = [cell for row in input_grid.rows for cell in row]
    # nodes = ["Reykjavik", "Oslo", "Moscow", "London", "Rome", "Berlin", "Belgrade", "Athens"]

    init_graph = {}
    for node in nodes:
        init_graph[node] = {}
        for neighbor in input_grid.find_neighbors(node):
            init_graph[node][neighbor] = neighbor.value

    """
    init_graph["Reykjavik"]["Oslo"] = 5
    init_graph["Reykjavik"]["London"] = 4
    init_graph["Oslo"]["Berlin"] = 1
    init_graph["Oslo"]["Moscow"] = 3
    init_graph["Moscow"]["Belgrade"] = 5
    init_graph["Moscow"]["Athens"] = 4
    init_graph["Athens"]["Belgrade"] = 1
    init_graph["Rome"]["Berlin"] = 2
    init_graph["Rome"]["Athens"] = 2
    """

    graph = Graph(input_grid, nodes, init_graph)
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=input_grid.rows[0][0])
    return shortest_path[input_grid.rows[-1][-1]]
    # return print_result(previous_nodes, shortest_path, input_grid.rows[0][0], target_node=input_grid.rows[-1][-1])


if __name__ == "__main__":

    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = to_grid(__file__, puzzle=puzzle)

            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
