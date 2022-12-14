from utils.graphs import SparseGrid
from utils.inputs import get_input

SAND_START = 500, 0


def parse(line):
    return [pair.split(",") for pair in line.split(" -> ")]


def points_between(x, y, x2, y2):
    min_x, max_x = min(x, x2), max(x, x2)
    min_y, max_y = min(y, y2), max(y, y2)
    if min_x == max_x:
        return [(x, v) for v in range(min_y, max_y + 1)]
    else:
        return [(v, y) for v in range(min_x, max_x + 1)]


def fill_in(data) -> SparseGrid:
    grid = SparseGrid()
    for row in data:
        for i, (x, y) in enumerate(row[:-1]):
            next_x, next_y = row[i + 1]
            for point in points_between(int(x), int(y), int(next_x), int(next_y)):
                grid.set(*point)
    return grid


def sand_fall(grid: SparseGrid, sand_x, sand_y, end_condition, end_return):
    # right below is solid
    if grid.has(sand_x, sand_y + 1):
        # down left is solid
        if grid.has(sand_x - 1, sand_y + 1):
            # down right is solid
            if grid.has(sand_x + 1, sand_y + 1):
                return sand_x, sand_y
            return sand_fall(grid, sand_x + 1, sand_y, end_condition, end_return)
        return sand_fall(grid, sand_x - 1, sand_y, end_condition, end_return)

    if end_condition(grid, sand_y + 1):
        return end_return(sand_x, sand_y)

    return sand_fall(grid, sand_x, sand_y + 1, end_condition, end_return)


def process(grid: SparseGrid, end: (), end_value: (), terminator=lambda *args: False):
    sand = 0
    new_pos = sand_fall(grid, *SAND_START, end, end_value)
    while new_pos:
        grid.set(*new_pos)
        sand += 1
        if terminator(new_pos):
            break
        new_pos = sand_fall(grid, 500, 0, end, end_value)
    return sand


def part_one(data):
    return process(fill_in(data), lambda _grid, next_sand_y: next_sand_y > _grid.max_y, lambda *args: None)


def part_two(data):
    grid = fill_in(data)
    floor = grid.max_y + 2
    return process(grid, lambda _grid, next_sand_y: next_sand_y == floor, lambda _sand_x, _sand_y: (_sand_x, _sand_y),
                   lambda new_pos: new_pos == SAND_START)


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")
