from utils.algos import dijkstra_algorithm
from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def print_path(grid: Grid, previous_nodes: dict, end):
    print(end)
    selected = set()
    cell = previous_nodes[end]
    while cell:
        selected.add(cell[0])
        cell = previous_nodes.get(cell, None)

    buff = []
    for row in grid.rows:
        buff.append("".join([str(cell.value) if cell not in selected else "." for cell in row]))
    print("\n".join(buff))



def part_one(input_grid: Grid):
    start, end = input_grid.cell_at(0, 0), input_grid.cell_at(-1, -1)
    previous_nodes, sp = dijkstra_algorithm(input_grid, start)
    # print_path(previous_nodes, end)

    best = None
    for bits, cost in sp.items():
        if bits[0] == end:
            if best is None:
                best = bits
            elif cost < sp[best]:
                best = bits
    print_path(input_grid, previous_nodes, best)
    return sp[best]


def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__, coerce=int)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
