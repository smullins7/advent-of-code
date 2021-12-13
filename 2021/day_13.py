#!/usr/bin/env python3

from lib_inputs import Grid, day_filename, Cell


def print_grid(grid):
    print("Grid:")
    for row in grid:
        print("".join(["#" if cell.value else "." for cell in row]))


def to_grid(puzzle=1):
    grid = Grid([])
    lines = open(day_filename(__file__, puzzle)).readlines()
    for y, line in enumerate(lines):
        line = line.strip()
        if not line:
            break
        x, y = map(int, line.split(","))
        cell = Cell(x, y, 1)
        while y > len(grid.rows) - 1:
            grid.rows.append([])
        while x > len(grid.rows[y]) - 1:
            grid.rows[y].append(Cell(len(grid.rows[y]), y, 0))
        grid.rows[y][x] = cell

    folds = [line.strip().split("fold along ")[-1] for line in lines[y+1:]]

    target_x = (max([int(cmd.split("=")[-1]) for cmd in folds if cmd.startswith("x=")]) * 2) + 1

    for y, row in enumerate(grid.rows):
        while len(row) != target_x:
            row.append(Cell(len(row), y, 0))
    return grid, folds


def fold(grid, cmd):
    folded_grid = Grid([])
    if cmd.startswith("y"):
        for y in range(len(grid.rows) // 2):
            row = []
            for up, down in zip(grid.rows[y], grid.rows[len(grid.rows) - 1 - y]):
                row.append(Cell(up.x, up.y, max(up.value, down.value)))
            folded_grid.rows.append(row)
    else:
        for row in grid.rows:
            length = int(cmd.split("=")[-1])
            new_row = []
            for left, right in zip(row[:length], reversed(row[length + 1:])):
                new_row.append(Cell(left.x, left.y, max(left.value, right.value)))
            folded_grid.rows.append(new_row)
    return folded_grid


def part_one(data):
    grid, fold_cmds = data
    for cmd in fold_cmds[:1]:
        folded_grid = fold(grid, cmd)
        grid = folded_grid
    dots = 0
    for row in folded_grid.rows:
        for cell in row:
            if cell.value == 1:
                dots += 1
    return dots


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
