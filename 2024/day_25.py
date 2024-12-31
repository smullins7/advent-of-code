from itertools import product

from utils.graphs import Grid, Cell
from utils.inputs import get_grouped_inputs


def to_grid(lines: list[str]) -> Grid:
    grid = Grid()
    for y, line in enumerate(lines):
        grid.add_row([Cell(x, y, c) for x, c in enumerate(line.strip())])
    return grid

def fits(lock: Grid, key: Grid) -> bool:
    for column_index in range(lock.max_y - 1):
        lock_pins = sum([1 for v in lock.slice_column_values(column_index) if v == "#"])
        key_pins = sum([1 for v in key.slice_column_values(column_index) if v == "#"])
        if lock_pins + key_pins > lock.max_x + 3:
            return False
    return True

def part_one(data):
    keys = []
    locks = []
    for lines in data:
        grid = to_grid(lines)
        if all([v == "." for v in grid.slice_row_values(0)]):
            keys.append(grid)
        else:
            locks.append(grid)

    return sum([1 for lock, key in product(locks, keys) if fits(lock, key)])


def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")