from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def find_start(grid: Grid):
    for cell in grid:
        if cell.value == "^":
            return cell


directions = {
    "U": lambda g, c: g.walk_up(c),
    "D": lambda g, c: g.walk_down(c),
    "L": lambda g, c: g.walk_left(c),
    "R": lambda g, c: g.walk_right(c),
}

next_dir = {
    "U": "R",
    "R": "D",
    "D": "L",
    "L": "U"
}


def walk(grid: Grid, cell: Cell, seen: set[Cell], direction="U"):
    seen.add(cell)
    prev_cell = cell
    for next_cell in directions[direction](grid, cell):
        if next_cell.value != "#":
            seen.add(next_cell)
            if grid.is_on_border(next_cell):
                return
            else:
                prev_cell = next_cell
        else:
            break
    walk(grid, prev_cell, seen, next_dir[direction])


def part_one(grid: Grid):
    seen = set()
    starting_cell = find_start(grid)
    walk(grid, starting_cell, seen)
    return len(seen)


# return True if loop found, False otherwise
def walk_loop(grid: Grid, cell: Cell, seen_dir: set[tuple[Cell, str]], direction="U"):
    if (cell, direction) in seen_dir:
        return True
    seen_dir.add((cell, direction))
    prev_cell = cell
    for next_cell in directions[direction](grid, cell):
        if next_cell.value != "#":
            if (next_cell, direction) in seen_dir:
                return True
            seen_dir.add((next_cell, direction))
            if grid.is_on_border(next_cell):
                return False
            else:
                prev_cell = next_cell
        else:
            break
    return walk_loop(grid, prev_cell, seen_dir, next_dir[direction])


def part_two(grid: Grid):
    starting_cell = find_start(grid)
    total = 0
    for cell in grid:
        if cell.value != ".":
            continue
        cell.value = "#"
        seen = set()
        if walk_loop(grid, starting_cell, seen):
            total += 1
        cell.value = "."
    return total


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
