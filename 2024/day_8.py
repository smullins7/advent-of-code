from collections import defaultdict
from itertools import combinations

from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def possible_locations(first: Cell, second: Cell) -> tuple[Cell, Cell]:
    if first.x > second.x or (first.x == second.x and first.y > second.y):
        first, second = second, first

    x = abs(first.x - second.x)
    y = abs(first.y - second.y)

    if first.y > second.y:
        return Cell(first.x - x, first.y + y), Cell(second.x + x, second.y - y)

    return Cell(first.x - x, first.y - y), Cell(second.x + x, second.y + y)


def part_one(grid: Grid):
    signals = defaultdict(set)
    for cell in grid:
        if cell.value == ".":
            continue
        signals[cell.value].add(cell)

    antinodes = set()
    for cells in signals.values():
        for (first, second) in combinations(cells, 2):
            for cell in possible_locations(first, second):
                if grid.has_cell(cell):
                    antinodes.add((cell.x, cell.y))

    return len(antinodes)


def possible_distances(first: Cell, second: Cell):
    x = abs(first.x - second.x)
    y = abs(first.y - second.y)

    if first.y > second.y:
        yield first.x, first.y, -x, y
        yield second.x, second.y, x, -y
    else:
        yield first.x, first.y, -x, -y
        yield second.x, second.y, x, y


def part_two(grid: Grid):
    signals = defaultdict(set)
    for cell in grid:
        if cell.value == ".":
            continue
        signals[cell.value].add(cell)

    antinodes = set()
    for cells in signals.values():
        for (first, second) in combinations(cells, 2):
            if first.x > second.x or (first.x == second.x and first.y > second.y):
                first, second = second, first
            antinodes.add((first.x, first.y))
            antinodes.add((second.x, second.y))

            for (x, y, delta_x, delta_y) in possible_distances(first, second):
                while grid.has(x + delta_x, y + delta_y):
                    antinodes.add((x + delta_x, y + delta_y))
                    x = x + delta_x
                    y = y + delta_y

    buff = []
    for row in grid.rows:
        l = []
        for cell in row:
            if (cell.x, cell.y) in antinodes:
                l.append("#")
            else:
                l.append(cell.value)
        buff.append("".join(l))
    print("\n".join(buff))
    return len(antinodes)


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
