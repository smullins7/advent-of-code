import sys
from itertools import pairwise
from typing import List, Dict, Tuple, Iterable

from utils.graphs import Grid, Cell


def shortest_path(grid: Grid, start: Cell, at_end: (), can_traverse=lambda node, neighbor, path: True):
    """
    Given a grid and a starting node, find the shortest path to some "end".

    If there are rules for when a node can traverse to a neighbor use `can_traverse`
    `at_end` takes a node and should return `True` if that node represents the end of the search.
    Not doing `end: Cell` because sometimes you have multiple possible end states you can reach
    and not just a particular cell
    """

    explored = []

    queue = [[start]]

    if at_end(start):
        return

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            neighbors = grid.find_neighbors(node)

            for neighbor in neighbors:
                if can_traverse(node, neighbor, path):
                    new_path = list(path) + [neighbor]
                    queue.append(new_path)

                    if at_end(neighbor):
                        return new_path
            explored.append(node)


def f(p, n, item):
    l = []
    for _ in range(n):
        back = p[item]
        l.append(back)
        item = back
    return l


def dijkstra_algorithm(adjacency: Dict[Cell, List[Cell]], start_node,
                       can_traverse=lambda cell, neighbor, previous_nodes: True):
    unvisited_nodes = list(adjacency.keys())

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        for neighbor in adjacency[current_min_node]:
            tentative_value = shortest_path[current_min_node] + neighbor.value
            if tentative_value < shortest_path[neighbor]:
                if not can_traverse(current_min_node, neighbor, previous_nodes):
                    backup = f(previous_nodes, 3, current_min_node)

                    # compare that to...backing up to the start of the straight line?
                    # then somehow fix my previous nodes and shortest paths if backing up is shorter
                    continue
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


# https://en.wikipedia.org/wiki/Shoelace_formula
def shoelace_area(ordered_points: Iterable[Tuple[int, int]]) -> float:
    area = 0
    for (first_x, first_y), (second_x, second_y) in pairwise(ordered_points):
        area += (first_x * second_y) - (first_y * second_x)
    return area / 2
