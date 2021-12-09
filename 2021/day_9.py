#!/usr/bin/env python3
import dataclasses
from functools import reduce

from lib_inputs import get_input


@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    x: int
    y: int
    value: int


def parse(line):
    return [int(c) for c in line]


def get_adjacent(x, y, grid):
    adjacents = []
    row = grid[y]
    if y != 0:
        adjacents.append(Cell(x, y - 1, grid[y - 1][x]))
    if y != len(grid) - 1:
        adjacents.append(Cell(x, y + 1, grid[y + 1][x]))
    if x != 0:
        adjacents.append(Cell(x - 1, y, row[x - 1]))
    if x != len(row) - 1:
        adjacents.append(Cell(x + 1, y, row[x + 1]))
    return adjacents


def part_one(data):
    lows = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            adjacents = get_adjacent(x, y, data)
            if cell < min([c.value for c in adjacents]):
                lows.append(cell)
    return sum([v + 1 for v in lows])


def explore_basin(cell, grid, seen):
    if cell.value == 9:
        return seen
    seen.add(cell)
    for adjacent in get_adjacent(cell.x, cell.y, grid):
        if adjacent not in seen:
            seen.update(explore_basin(adjacent, grid, seen))

    return seen


def part_two(data):
    basins = set()
    global_seen = set()
    for y, row in enumerate(data):
        for x, v in enumerate(row):
            cell = Cell(x, y, v)
            if cell in global_seen:
                continue
            basin = explore_basin(cell, data, set())
            if basin:
                basins.add(frozenset(basin))
                global_seen.update(basin)
    top_three = []
    for basin in basins:
        size = len(basin)
        if len(top_three) < 3:
            top_three.append(size)
        elif size > min(top_three):
            top_three.remove(min(top_three))
            top_three.append(size)

    return reduce(lambda a, b: a * b, top_three, 1)


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        data = get_input(__file__, puzzle=puzzle, coerce=parse)
        print(f"Part 1: Input {puzzle}, {part_one(data)}")
        print(f"Part 2: Input {puzzle}, {part_two(data)}")

