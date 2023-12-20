from utils.graphs import Grid, Cell
from utils.inputs import get_grouped_inputs


def range_equality(first, second, max_allowed_differences):
    unequal = 0
    for a, b in zip(first, second):
        if a == b:
            continue
        if a != b:
            unequal += 1
            if unequal > max_allowed_differences:
                return False
    return unequal

def as_grid(group):
    grid = Grid()
    for y, line in enumerate(group):
        grid.add_row([Cell(x, y, c) for x, c in enumerate(line.strip())])
    return grid

def does_reflect_vertically(grid: Grid, left: int, right: int, diffs: int) -> bool:
    total = 0
    while left > 0 and right < grid.max_x:
        left -= 1
        right += 1
        unequal_count = range_equality(grid.slice_column_values(left), grid.slice_column_values(right), diffs - total)
        if unequal_count is False:
            return False
        total += unequal_count
        if total > diffs:
            return False

    return total == diffs

def does_reflect_horizontally(grid: Grid, top: int, bottom: int, diffs: int) -> bool:
    total = 0
    while top > 0 and bottom < grid.max_y:
        top -= 1
        bottom += 1
        unequal_count = range_equality(grid.slice_row_values(top), grid.slice_row_values(bottom), diffs - total)
        if unequal_count is False:
            return False
        total += unequal_count
        if total > diffs:
            return False
    return total == diffs

def find_vertical(grid: Grid, diffs: int):
    for i in range(grid.max_x):
        unequal_count = range_equality(grid.slice_column_values(i), grid.slice_column_values(i+1), diffs)
        if unequal_count is False:
            continue
        # compare outwards
        if does_reflect_vertically(grid, i, i + 1, diffs - unequal_count):
            return i + 1
    return None

def find_horizontal(grid: Grid, max_allowed_differences: int):
    for i in range(grid.max_y):
        unequal_count = range_equality(grid.slice_row_values(i), grid.slice_row_values(i + 1), max_allowed_differences)
        if unequal_count is False:
            continue
        # compare outwards
        if does_reflect_horizontally(grid, i, i + 1, max_allowed_differences - unequal_count):
            return 100 * (i+1)
    return None

def run(data, count):
    total = 0
    for group in data:
        grid = as_grid(group)
        vertical = find_vertical(grid, count)
        horizontal = find_horizontal(grid, count)
        if vertical:
            total += vertical
        else:
            total += horizontal
    return total

def part_one(data):
    return run(data, 0)


def part_two(data):
    return run(data, 1)


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")

