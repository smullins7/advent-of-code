from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def advance_beam(grid: Grid, cell: Cell):
    under = grid.find_neighbor(cell, "D")
    while under and under.value == ".":
        under.value = "|"
        under = grid.find_neighbor(under, "D")
    next_beams = []
    if under and under.value == "^":
        left = grid.find_neighbor(under, "L")
        if left and left.value == ".":
            left.value = "|"
            next_beams.append(left)
        right = grid.find_neighbor(under, "R")
        if right and right.value == ".":
            right.value = "|"
            next_beams.append(right)
    return next_beams


def count_splits(grid: Grid):
    total = 0
    for cell in grid:
        if cell.value == "^":
            if (grid.find_neighbor(cell, "L").value == "|"
                    and grid.find_neighbor(cell, "R").value == "|"
                    and grid.find_neighbor(cell, "U").value == "|"):
                total += 1
    return total


def part_one(grid: Grid):
    s = grid.find("S")

    todo = advance_beam(grid, s)
    while todo:
        beam_cell = todo.pop(0)
        todo.extend(advance_beam(grid, beam_cell))
    return count_splits(grid)


def quantum(grid: Grid, cell: Cell, acc):
    if cell in acc:
        return acc[cell]

    cell = grid.find_neighbor(cell, "D")
    while cell and cell.value == ".":
        cell = grid.find_neighbor(cell, "D")

    if not cell:
        # reached the bottom row
        return 1

    left = grid.find_neighbor(cell, "L")
    acc[left] = quantum(grid, left, acc)

    right = grid.find_neighbor(cell, "R")
    acc[right] = quantum(grid, right, acc)
    return acc[left] + acc[right]


def part_two(grid: Grid):
    return quantum(grid, grid.find("S"), {})


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data.clone())}")
        print(f"{f.__name__}:\n\t{f(real_data.clone())}")
