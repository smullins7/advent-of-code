#!/usr/bin/env python3

from lib_inputs import day_filename


def print_grid(grid):
    print("Grid:")
    max_x = max([c[0] for c in grid])
    max_y = max([c[1] for c in grid])
    for y in range(max_y + 1):
        print("".join(["#" if (x, y) in grid else "." for x in range(max_x + 1)]))


def to_grid(puzzle=1):
    grid = set()
    lines = open(day_filename(__file__, puzzle)).readlines()
    for y, line in enumerate(lines):
        line = line.strip()
        if not line:
            break
        cx, cy = map(int, line.split(","))
        grid.add((cx,cy))

    folds = [line.strip().split("fold along ")[-1] for line in lines[y+1:]]
    return grid, folds


def fold(grid, cmd):
    folded_grid = set()
    direction, length = cmd.split("=")
    length = int(length)
    for (x, y) in grid:
        if direction == "x":
            if x == length:
                continue
            if x < length:
                folded_grid.add((x, y))
            else:
                folded_grid.add((2 * length - x, y))

        else:
            if y == length:
                continue
            if y < length:
                folded_grid.add((x, y))
            else:
                folded_grid.add((x, 2 * length - y))

    return folded_grid


def part_one(data):
    grid, fold_cmds = data
    for cmd in fold_cmds[:1]:
        folded_grid = fold(grid, cmd)
        grid = folded_grid
    return len(folded_grid)


def part_two(data):
    grid, fold_cmds = data
    for cmd in fold_cmds:
        folded_grid = fold(grid, cmd)
        grid = folded_grid
    print_grid(folded_grid)


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = to_grid(puzzle=puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
