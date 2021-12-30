#!/usr/bin/env python3

from lib_inputs import to_sparse_grid, SparseGrid

EMPTY = "."
EAST = ">"
SOUTH = "v"


def move(grid, x, y, direction):
    val = grid.get(x, y)
    if direction == "east" and val == EAST:
        # check to my right, or the x=0 if i'm at the edge
        if grid.get((x + 1) % (grid.max_x + 1), y, EMPTY) == EMPTY:
            return (x + 1) % (grid.max_x + 1), y, EAST
    elif direction == "south" and val == SOUTH:
        if grid.get(x, (y + 1) % (grid.max_y + 1), EMPTY) == EMPTY:
            return x, (y + 1) % (grid.max_y + 1), SOUTH
    return x, y, val


def half_step(grid, direction):
    updated = SparseGrid({})
    moved = set()
    for x, y, _ in grid:
        if (x, y) in moved:
            continue
        new_x, new_y, v = move(grid, x, y, direction)
        updated.set(new_x, new_y, v)
        if new_x != x or new_y != y:
            updated.set(x, y, EMPTY)
            moved.add((new_x, new_y))
    return updated


def step(grid):
    #p(grid)
    updated = half_step(grid, "east")
    updated = half_step(updated, "south")
    #p(updated)
    return updated


def p(grid):
    print("GRID:")
    row = []
    for x, y, v in grid:
        row.append(v)
        if len(row) == grid.max_x + 1:
            print("".join(row))
            row = []


def part_one(grid):
    prev = None
    count = 0
    while grid != prev:
        prev = grid
        grid = step(grid)
        count += 1
        if count == 600:
            break
    return count


def part_two(grid):
    return 0


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            grid = to_sparse_grid(__file__, puzzle=puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(grid)}")
