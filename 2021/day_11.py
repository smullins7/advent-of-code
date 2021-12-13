#!/usr/bin/env python3

from lib_inputs import to_grid


def increase(grid, cell):
    cell.value += 1
    if cell.value == 10:
        for adjancent_cell in grid.find_all_adjacency(cell.x, cell.y):
            increase(grid, adjancent_cell)


def reset_and_count(grid):
    flashes = 0
    for row in grid:
        for cell in row:
            if cell.value >= 10:
                cell.value = 0
                flashes += 1
    return flashes


def one_step(grid):
    for row in grid:
        for cell in row:
            increase(grid, cell)

    return reset_and_count(grid)


def part_one(grid):
    return sum([one_step(grid) for _ in range(100)])


def part_two(grid):
    target = len(grid.rows) * len(grid.rows[0])
    step = 1
    while True:
        if one_step(grid) == target:
            return step
        step += 1


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            grid = to_grid(__file__, puzzle=puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(grid)}")
