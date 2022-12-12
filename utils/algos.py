from utils.graphs import Grid, Cell


def shortest_path(grid: Grid, start: Cell, at_end: (), can_traverse=lambda node, neighbor: True):
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
                if can_traverse(node, neighbor):
                    new_path = list(path) + [neighbor]
                    queue.append(new_path)

                    if at_end(neighbor):
                        return new_path
            explored.append(node)
