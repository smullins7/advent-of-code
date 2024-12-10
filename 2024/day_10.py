from itertools import product

from utils.algos import shortest_path, accumulate_paths
from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def can_step(from_cell: Cell, to_cell: Cell, path):
    return from_cell.value + 1 == to_cell.value


def is_possible(grid: Grid, start: Cell, end: Cell):
    path = shortest_path(grid, start, lambda cell: cell == end, can_traverse=can_step)
    return int(bool(path))

def part_one(grid: Grid):
    trailheads = grid.find_all_with(0)
    peaks = grid.find_all_with(9)

    return sum(map(lambda pair: is_possible(grid, *pair), product(trailheads, peaks)))


def rating(grid: Grid, start: Cell, end: Cell):
    paths = accumulate_paths(grid, start, lambda cell: cell == end, can_traverse=can_step)
    return len(paths)

def part_two(grid: Grid):
    trailheads = grid.find_all_with(0)
    peaks = grid.find_all_with(9)

    return sum(map(lambda pair: rating(grid, *pair), product(trailheads, peaks)))


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__, coerce=int)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")