import sys
from itertools import pairwise
from typing import Tuple, Iterable

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

def accumulate_paths(grid: Grid, start: Cell, at_end: (), can_traverse=lambda node, neighbor, path: True):
    """
    This function is modeled off the above shortest path algorithm, however it accumulates all possible
    valid paths and returns them
    """
    valid_paths = []

    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        neighbors = grid.find_neighbors(node)

        for neighbor in neighbors:
            if can_traverse(node, neighbor, path):
                new_path = list(path) + [neighbor]
                queue.append(new_path)

                if at_end(neighbor):
                    valid_paths.append(new_path)
    return valid_paths


def dijkstra_algorithm(grid: Grid, start_node):
    unvisited_nodes = [(start_node, "X", 0)]
    for cell in grid:
        if cell == start_node:
            continue
        for direction in ("U", "D", "L", "R"):
            for i in range(1, 4):
                if direction == "U":
                    if len(list(grid.walk_down(cell))) < i:
                        continue

                if direction == "D":
                    if len(list(grid.walk_up(cell))) < i:
                        continue

                if direction == "L":
                    if len(list(grid.walk_right(cell))) < i:
                        continue

                if direction == "R":
                    if len(list(grid.walk_left(cell))) < i:
                        continue
                unvisited_nodes.append((cell, direction, i))

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[(start_node, "X", 0)] = 0

    def get_direction(a: Cell, b: Cell) -> str:
        if a.x == b.x and a.y > b.y:
            return "U"
        if a.x == b.x:
            return "D"
        if a.x > b.x:
            return "L"
        return "R"

    def is_legal_dir(previous, current) -> bool:
        d = {"U": "D", "D": "U", "L": "R", "R": "L", "X": ""}
        return d[previous] != current

    print(len(unvisited_nodes))
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        node, direction, steps = current_min_node
        for neighbor in grid.find_neighbors(node):
            # skip if neighbor is in same direction and steps is already at 3
            next_direction = get_direction(node, neighbor)
            if not is_legal_dir(direction, next_direction) or neighbor == start_node or (next_direction == direction and steps == 3):
                continue
            steps_in_direction = 1 if next_direction != direction else steps + 1
            tentative_value = shortest_path[current_min_node] + neighbor.value
            _next = (neighbor, next_direction, steps_in_direction)
            if tentative_value < shortest_path[_next]:
                shortest_path[_next] = tentative_value
                # We also update the best path to the current node
                previous_nodes[_next] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
        if len(unvisited_nodes) % 1000 == 0:
            print(len(unvisited_nodes))

    return previous_nodes, shortest_path


# https://en.wikipedia.org/wiki/Shoelace_formula
def shoelace_area(ordered_points: Iterable[Tuple[int, int]]) -> float:
    area = 0
    for (first_x, first_y), (second_x, second_y) in pairwise(ordered_points):
        area += (first_x * second_y) - (first_y * second_x)
    return area / 2
