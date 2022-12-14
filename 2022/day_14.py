from utils.graphs import SparseGrid
from utils.inputs import get_input


def parse(line):
    return [pair.split(",") for pair in line.split(" -> ")]


def points_between(x, y, x2, y2):
    min_x, max_x = min(x, x2), max(x, x2)
    min_y, max_y = min(y, y2), max(y, y2)
    if min_x == max_x:
        return [(x, v) for v in range(min_y, max_y + 1)]
    else:
        return [(v, y) for v in range(min_x, max_x + 1)]


def part_one(data):
    grid = SparseGrid({})
    for row in data:
        for i, (x, y) in enumerate(row[:-1]):
            next_x, next_y = row[i + 1]
            for point in points_between(int(x), int(y), int(next_x), int(next_y)):
                grid.set(*point, "#")

    sand = 0
    new_pos = sand_fall(grid, 500, 0)
    while new_pos:
        grid.set(*new_pos, "o")
        sand += 1
        new_pos = sand_fall(grid, 500, 0)
    return sand


def sand_fall(grid: SparseGrid, sand_x, sand_y):
    # right below is solid
    if grid.has(sand_x, sand_y + 1):
        # down left is solid
        if grid.has(sand_x - 1, sand_y + 1):
            # down right is solid
            if grid.has(sand_x + 1, sand_y + 1):
                return sand_x, sand_y
            return sand_fall(grid, sand_x + 1, sand_y)
        return sand_fall(grid, sand_x - 1, sand_y)

    if sand_y + 1 > grid.max_y:
        return None

    return sand_fall(grid, sand_x, sand_y + 1)


def sand_fall_with_floor(grid: SparseGrid, sand_x, sand_y, floor):
    # right below is solid
    if grid.has(sand_x, sand_y + 1):
        # down left is solid
        if grid.has(sand_x - 1, sand_y + 1):
            # down right is solid
            if grid.has(sand_x + 1, sand_y + 1):
                return sand_x, sand_y
            return sand_fall_with_floor(grid, sand_x + 1, sand_y, floor)
        return sand_fall_with_floor(grid, sand_x - 1, sand_y, floor)

    if sand_y + 1 == floor:
        return sand_x, sand_y

    return sand_fall_with_floor(grid, sand_x, sand_y + 1, floor)


def part_two(data):
    grid = SparseGrid({})
    for row in data:
        for i, (x, y) in enumerate(row[:-1]):
            next_x, next_y = row[i + 1]
            for point in points_between(int(x), int(y), int(next_x), int(next_y)):
                grid.set(*point, "#")

    floor = grid.max_y + 2
    sand = 0
    new_pos = sand_fall_with_floor(grid, 500, 0, floor)
    while new_pos:
        grid.set(*new_pos, "o")
        sand += 1

        if new_pos == (500, 0):
            break
        new_pos = sand_fall_with_floor(grid, 500, 0, floor)
    return sand


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")

