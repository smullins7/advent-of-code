from itertools import combinations

from utils.graphs import Grid
from utils.inputs import to_grid


def safe_range(a: int, b: int):
    if a > b:
        return range(b, a)
    return range(a, b)


def do(grid: Grid, multiplier: int):
    # don't bother physically expanding the graph
    # make set of index of empty rows and columns
    # make combinations of all pairs
    # take manhattan distance of each pair
    # for each instance of crossing an empty row or column add one to manhattan distance
    # sum up
    empty_rows = set(range(0, grid.max_y))
    empty_columns = set(range(0, grid.max_x))
    galaxies = []
    for cell in grid:
        if cell.value != ".":
            empty_rows.discard(cell.y)
            empty_columns.discard(cell.x)
            galaxies.append(cell)

    total = 0
    for first, second in combinations(galaxies, 2):
        distance = (abs(first.x - second.x) + abs(first.y - second.y) +
                    (multiplier * len(set(safe_range(first.x, second.x)).intersection(empty_columns))) +
                    (multiplier * len(set(safe_range(first.y, second.y)).intersection(empty_rows))))
        # print(first.value, second.value, distance)
        total += distance
    return total

def part_one(grid: Grid):
    return do(grid, 1)


def part_two(grid: Grid):
    return do(grid, 1000000 - 1)


if __name__ == "__main__":
    sample_data = to_grid(__file__, coerce=str)
    real_data = to_grid(__file__, is_sample=False, coerce=str)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")

