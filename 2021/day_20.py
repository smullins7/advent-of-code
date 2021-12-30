#!/usr/bin/env python3
import math

from lib_inputs import get_input, bin_to_int


def parse(data):
    algo = data[0]
    grid = {}
    for y, row in enumerate(data[2:]):
        for x, c in enumerate(row):
            grid[(x, y)] = c

    return algo, grid


def add_border(grid):
    keys = sorted(grid)
    _min, _max = keys[0][0], keys[-1][-1]
    for x in range(_min - 1, _max + 2):
        grid[(x, _min - 1)] = "."
        grid[(x, _max + 1)] = "."
    for y in range(_min, _max + 1):
        grid[(_min - 1, y)] = "."
        grid[(_max + 1, y)] = "."


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


def pos_to_b(image, x, y):
    def _to_i(c):
        return "1" if c == "#" else "0"

    return bin_to_int("".join([_to_i(image.get(n, ".")) for n in neighbors_in_order(x, y)]))


def enhance(algo, image):
    enhanced = {}
    for x, y in image:
        index = pos_to_b(image, x, y)
        enhanced[(x, y)] = algo[index]
    return enhanced


def lit(grid):
    return len([v for v in grid.values() if v == "#"])


# 5518 too high, should be 5349
def part_one(data):
    algo, grid = parse(data)

    for _ in range(2):
        add_border(grid)
    grid = enhance(algo, grid)
    for _ in range(2):
        add_border(grid)
    grid = enhance(algo, grid)
    return lit(grid)


def part_two(data):
    return 0


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one,):
            data = get_input(__file__, puzzle=puzzle, coerce=str)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
