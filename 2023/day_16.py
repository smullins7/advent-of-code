from itertools import chain

from utils.graphs import Grid, Cell
from utils.inputs import get_grids

REFLECTIONS = {
    ("|", "L"): ("U", "D"),
    ("|", "R"): ("U", "D"),
    ("-", "U"): ("L", "R"),
    ("-", "D"): ("L", "R"),
    ("/", "U"): ("R",),
    ("/", "D"): ("L",),
    ("/", "L"): ("D",),
    ("/", "R"): ("U",),
    ("\\", "U"): ("L",),
    ("\\", "D"): ("R",),
    ("\\", "L"): ("U",),
    ("\\", "R"): ("D",),
}
ITERS = {
    "U": lambda g, p: g.walk_up(p),
    "D": lambda g, p: g.walk_down(p),
    "L": lambda g, p: g.walk_left(p),
    "R": lambda g, p: g.walk_right(p),
}

def do(grid: Grid, start_pos: Cell, start_dir: str) -> int:
    beams = []
    if (start_pos.value, start_dir) in REFLECTIONS:
        for new_dir in REFLECTIONS[(start_pos.value, start_dir)]:
            beams.append((start_pos, new_dir))
    else:
        beams.append((start_pos, start_dir))
    loops = set()
    def _do(_iter, _dir):
        for cell in _iter:
            if (cell.value, _dir) not in REFLECTIONS:
                loops.add((cell, _dir))
                continue
            for reflected in REFLECTIONS[(cell.value, _dir)]:
                beams.append((cell, reflected))
            break
    while beams:
        position, direction = beams.pop(0)
        if (position, direction) in loops:
            continue
        loops.add((position, direction))
        _do(ITERS[direction](grid, position), direction)
    energized = set()
    for tile, _ in loops:
        energized.add(tile)
    return len(energized)

def part_one(grid: Grid):
    return do(grid, grid.cell_at(0, 0), "R")


def part_two(grid: Grid):
    best = 0
    for start in grid.rows[0]:
        best = max(best, do(grid, start, "D"))
    for start in grid.rows[-1]:
        best = max(best, do(grid, start, "U"))
    for row in grid.rows:
        best = max(best, do(grid, row[0], "R"))
        best = max(best, do(grid, row[-1], "L"))
    return best


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")

