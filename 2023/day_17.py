from utils.algos import dijkstra_algorithm
from utils.graphs import Grid
from utils.inputs import get_grids

def print_path(previous_nodes, end):
    print(end)
    cell = previous_nodes[end]
    while cell:
        print(cell)
        cell = previous_nodes.get(cell, None)

def in_a_line(_iter):
    cells = [cell for cell in _iter]
    x = cells[0].x
    y = cells[0].y
    return all([c.x == x for c in cells]) or all([c.y == y for c in cells])

def part_one(input_grid: Grid):

    def no_more_than_three(cell, neighbor, previous):
        one_back = previous.get(cell, None)
        if one_back is None:
            return True
        if one_back == neighbor:
            return False
        two_back = previous.get(one_back, None)
        if two_back is None:
            return True
        three_back = previous.get(two_back, None)
        if three_back is None:
            return True
        if three_back.x == two_back.x == one_back.x == cell.x == neighbor.x or three_back.y == two_back.y == one_back.y == cell.y == neighbor.y:
            #print(f"At {cell} and not going to {neighbor}, this may indicate this path is not optimal")
            return False
        return True
    start, end = input_grid.cell_at(0, 0), input_grid.cell_at(-1, -1)
    previous_nodes, sp = dijkstra_algorithm(input_grid.as_adjacency_list(), start, no_more_than_three)
    print_path(previous_nodes, end)

    return sp[end]


def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__, coerce=int)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        #print(f"{f.__name__}:\n\t{f(real_data)}")

