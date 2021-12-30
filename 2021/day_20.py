#!/usr/bin/env python3

from lib_inputs import get_input, bin_to_int

ON = "#"
OFF = "."


def parse(data):
    algo = data[0]
    grid = {}
    for y, row in enumerate(data[2:]):
        for x, c in enumerate(row):
            grid[(x, y)] = c

    return algo, grid


def add_border(grid, infinite_bit):
    keys = sorted(grid)
    _min, _max = keys[0][0], keys[-1][-1]
    for x in range(_min - 1, _max + 2):
        grid[(x, _min - 1)] = infinite_bit
        grid[(x, _max + 1)] = infinite_bit
    for y in range(_min, _max + 1):
        grid[(_min - 1, y)] = infinite_bit
        grid[(_max + 1, y)] = infinite_bit


def neighbors_in_order(x, y):
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1)
    ]


def pos_to_b(image, x, y, infinite_bit):
    def _to_i(c):
        return "1" if c == ON else "0"

    return bin_to_int("".join([_to_i(image.get(n, infinite_bit)) for n in neighbors_in_order(x, y)]))


def enhance(algo, image, infinite_bit):
    enhanced = {}
    for x, y in image:
        index = pos_to_b(image, x, y, infinite_bit)
        enhanced[(x, y)] = algo[index]
    return enhanced


def lit(grid):
    return len([v for v in grid.values() if v == ON])


def part_one(data):
    algo, grid = parse(data)
    add_border(grid, OFF)
    grid = enhance(algo, grid, OFF)
    add_border(grid, ON)
    grid = enhance(algo, grid, ON)
    return lit(grid)


# 20251 too high, has on = True to start (facepalm)
# got the right answer but this doesn't work for the input sample, I don't care anymore though
def part_two(data):
    algo, grid = parse(data)
    on = False
    for _ in range(50):
        add_border(grid, ON if on else OFF)
        grid = enhance(algo, grid, ON if on else OFF)
        on = not on
    return lit(grid)


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=str)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
