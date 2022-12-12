import string

from utils.algos import shortest_path
from utils.graphs import Cell, Grid
from utils.inputs import to_grid


def part_one(grid: Grid):
    start = Cell(0, 20, 1)
    at_E = lambda cell: cell.value == 27
    path = shortest_path(grid, start, at_E,
                         lambda cell, neighbor: cell.value + 1 >= neighbor.value)
    return len(path) - 1


def part_two(grid: Grid):
    start = Cell(55, 20, 27)  # start at E
    at_a = lambda cell: cell.value == 1
    path = shortest_path(grid, start, at_a,
                         lambda cell, neighbor: cell.value <= neighbor.value + 1)
    return len(path) - 1


def alpha(c: str):
    if c.islower():
        return string.ascii_lowercase.index(c) + 1
    elif c == "A":
        return 1
    else:
        return 27


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = to_grid(__file__, is_sample=0, coerce=alpha)
        print(f"{f.__name__}:\n\t{f(data)}")
