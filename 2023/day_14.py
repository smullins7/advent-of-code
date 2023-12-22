from collections import defaultdict

from utils.graphs import Grid
from utils.inputs import get_grids


def part_one(grid: Grid):
    total = 0
    for cell in grid:
        if cell.value != 'O':
            continue
        for above in grid.walk_up(cell):
            if above.value != '.':
                break
            cell.value = '.'
            above.value = 'O'
            cell = above
        total += grid.max_y - cell.y + 1

    return total

def move_via(iter, func):
    for cell in iter():
        if cell.value != 'O':
            continue
        for neighbor in func(cell):
            if neighbor.value != '.':
                break
            cell.value = '.'
            neighbor.value = 'O'
            cell = neighbor

def spin_cycle(grid: Grid):
    # NORTH
    move_via(lambda: grid, grid.walk_up)
    # WEST
    move_via(grid.iter_from_left, grid.walk_left)
    # SOUTH
    move_via(grid.iter_from_bottom, grid.walk_down)
    # EAST
    move_via(grid.iter_from_right, grid.walk_right)

def calculate_load(grid: Grid):
    total = 0
    for cell in grid:
        if cell.value != 'O':
            continue
        total += grid.max_y - cell.y + 1

    return total

def part_two(grid: Grid):
    hashes = {}
    end = 1000000000
    for i in range(end):
        spin_cycle(grid)
        _hash = hash(grid)
        if _hash in hashes:
            break
        hashes[_hash] = i
    # TODO this feels like it should be in a utility for ranges/intervals
    more = (end - i) % (i - hashes[_hash])
    for _ in range(more - 1):
        spin_cycle(grid)

    return calculate_load(grid)


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_two, ):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}") # 97,146 too low
