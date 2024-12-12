from collections import defaultdict, deque
from itertools import cycle

from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def explore(grid: Grid, start: Cell) -> frozenset[Cell]:
    garden = {start}
    to_explore = deque(grid.find_neighbors(start))
    while to_explore:
        neighbor = to_explore.popleft()
        if neighbor.value != start.value or neighbor in garden:
            continue
        garden.add(neighbor)
        to_explore.extend(grid.find_neighbors(neighbor))

    return frozenset(garden)

def part_one(grid: Grid):
    gardens = []
    for cell in grid:
        found = False
        for garden in gardens:
            if cell in garden:
                found = True
                break
        if found:
            continue

        gardens.append(explore(grid, cell))

    total = 0
    for garden in gardens:
        area = len(garden)
        perimeter = 0
        for cell in garden:
            for neighbor in grid.find_neighbors(cell):
                if neighbor.value != cell.value:
                    perimeter += 1
            perimeter += grid.border_count(cell)
        total += len(garden) * perimeter

    return total


def part_two_no_good(grid: Grid):

    gardens = []
    for cell in grid:
        found = False
        for garden in gardens:
            if cell in garden:
                found = True
                break
        if found:
            continue

        gardens.append(explore(grid, cell))

    total = 0
    for garden in gardens:
        sides = 4 # must have at least 4 at a minimum
        missing = defaultdict(set)
        for cell in garden:
            for neighbor in grid.find_neighbors(cell):
                if neighbor.value == cell.value:
                    continue
                missing[neighbor].add(cell)
        for cells in missing.values():
            if len(cells) == 1:
                continue
            sides += len(cells)
        print(len(garden), sides, cell.value)
        total += len(garden) * sides

    return total

def walk_around(grid: Grid, garden: set[Cell]) -> int:
    sides = defaultdict(list) # ("U|D|L|R", x|y): [x|y]
    for cell in garden:
        neighbors = grid.find_neighbors(cell)
        if set(neighbors).issubset(garden) and not grid.is_on_border(cell):
            continue # insulated, won't contain any sides
        if cell.x == 0 or grid.find_neighbor(cell, "L").value != cell.value:
            sides[("L", cell.x)].append(cell.y)
        if cell.x == grid.max_x or grid.find_neighbor(cell, "R").value != cell.value:
            sides[("R", cell.x)].append(cell.y)
        if cell.y == 0 or grid.find_neighbor(cell, "U").value != cell.value:
            sides[("U", cell.y)].append(cell.x)
        if cell.y == grid.max_y or grid.find_neighbor(cell, "D").value != cell.value:
            sides[("D", cell.y)].append(cell.x)

    incremental = 0
    for xs in sides.values():
        prev = None
        for x in sorted(xs):
            if prev is None:
                incremental += 1
                prev = x
            elif x - 1 == prev:
                prev = x
            else:
                incremental += 1
                prev = x
    return incremental

def part_two(grid: Grid):
    gardens = []
    for cell in grid:
        found = False
        for garden in gardens:
            if cell in garden:
                found = True
                break
        if found:
            continue

        gardens.append(explore(grid, cell))

    total = 0
    for garden in gardens:
        total += walk_around(grid, garden) * len(garden)



    return total

if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")