from collections import defaultdict
from typing import List

from utils.inputs import get_input


def as_grid(data):
    grid = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "#":
                grid.add((x, -y))

    return grid


MASKS = (-1, 0, 1)
ALL_MASKS = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
]


def is_empty(grid, x, y, direction=None) -> bool:
    if direction == "n":
        return not any([(x + mask, y + 1) in grid for mask in MASKS])
    if direction == "s":
        return not any([(x + mask, y - 1) in grid for mask in MASKS])
    if direction == "w":
        return not any([(x - 1, y + mask) in grid for mask in MASKS])
    if direction == "e":
        return not any([(x + 1, y + mask) in grid for mask in MASKS])

    return not any([(x + x_mask, y + y_mask) in grid for (x_mask, y_mask) in ALL_MASKS])


def get_moves(grid, directions):
    moves = defaultdict(list)
    for (x, y) in grid:
        if is_empty(grid, x, y):
            continue

        for direction in directions:
            if direction == "n":
                if is_empty(grid, x, y, "n"):
                    moves[(x, y + 1)].append((x, y))
                    break
            elif direction == "s":
                if is_empty(grid, x, y, "s"):
                    moves[(x, y - 1)].append((x, y))
                    break
            elif direction == "w":
                if is_empty(grid, x, y, "w"):
                    moves[(x - 1, y)].append((x, y))
                    break
            else:  # east
                if is_empty(grid, x, y, "e"):
                    moves[(x + 1, y)].append((x, y))
                    break
    return moves


def part_one(data: List[str]):
    directions = ["n", "s", "w", "e"]
    grid = as_grid(data)
    for _ in range(10):
        moves = get_moves(grid, directions)
        # advance directions
        directions = directions[1:] + [directions[0]]
        for move, currents in moves.items():
            if len(currents) == 1:
                grid.remove(currents[0])
                grid.add(move)

    first_x, first_y = next(iter(grid))
    min_x, min_y, max_x, max_y = first_x, first_y, first_x, first_y

    for x, y in grid:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return (abs(max_x - min_x) + 1) * (abs(max_y - min_y) + 1) - len(grid)


def part_two(data):
    directions = ["n", "s", "w", "e"]
    grid = as_grid(data)
    rounds = 0
    moved_this_round = True
    while moved_this_round:
        moved_this_round = False
        moves = get_moves(grid, directions)
        # advance directions
        directions = directions[1:] + [directions[0]]
        for move, currents in moves.items():
            if len(currents) == 1:
                moved_this_round = True
                grid.remove(currents[0])
                grid.add(move)
        rounds += 1

    return rounds


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
