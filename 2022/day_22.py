from dataclasses import dataclass
from typing import Tuple, Dict, List

from utils.inputs import get_grouped_input


def parse_instructions(line: str):
    parsed = []
    current_num = ""
    for c in line:
        if c.isnumeric():
            current_num += c
        else:
            if current_num:
                parsed.append(int(current_num))
                current_num = ""
            parsed.append(c)
    if current_num:
        parsed.append(int(current_num))
    return parsed


def parse_map(_map) -> Dict[Tuple[int, int], str]:
    grid = {}
    for y, line in enumerate(_map):
        for x, c in enumerate(line):
            if c in (".", "#"):
                grid[(x + 1, y + 1)] = c

    return grid


def find_leftmost(grid, y=1):
    x = 1
    while True:
        if (x, y) in grid:
            return x, y
        x += 1


def find_rightmost(grid, y=1):
    x = find_leftmost(grid, y)[0]
    while True:
        if (x, y) in grid:
            x += 1
        else:
            return x - 1, y


def find_topmost(grid, x=1):
    y = 1
    while True:
        if (x, y) in grid:
            return x, y
        y += 1


def find_bottommost(grid, x=1):
    y = find_topmost(grid, x)[1]
    while True:
        if (x, y) in grid:
            y += 1
        else:
            return x, y - 1


def move(grid: Dict[Tuple[int, int], str], position: Tuple[int, int], facing: str, spaces: int) -> Tuple[int, int]:
    new_position = position
    for _ in range(spaces):
        if facing == "right":
            # try to move one to the right
            if grid.get((new_position[0] + 1, new_position[1])) == ".":
                new_position = new_position[0] + 1, new_position[1]
            elif grid.get((new_position[0] + 1, new_position[1])) == "#":
                return new_position
            else:
                # wrap back to the left
                leftmost = find_leftmost(grid, new_position[1])
                if grid[leftmost] == ".":
                    new_position = leftmost
                else:
                    return new_position
        elif facing == "down":
            # try to move one down
            if grid.get((new_position[0], new_position[1] + 1)) == ".":
                new_position = new_position[0], new_position[1] + 1
            elif grid.get((new_position[0], new_position[1] + 1)) == "#":
                return new_position
            else:
                # wrap back to the top
                topmost = find_topmost(grid, new_position[0])
                if grid[topmost] == ".":
                    new_position = topmost
                else:
                    return new_position
        elif facing == "left":
            # try to move one to the left
            if grid.get((new_position[0] - 1, new_position[1])) == ".":
                new_position = new_position[0] - 1, new_position[1]
            elif grid.get((new_position[0] - 1, new_position[1])) == "#":
                return new_position
            else:
                # wrap back to the right
                rightmost = find_rightmost(grid, new_position[1])
                if grid[rightmost] == ".":
                    new_position = rightmost
                else:
                    return new_position
        else:  # up
            # try to move one up
            if grid.get((new_position[0], new_position[1] - 1)) == ".":
                new_position = new_position[0], new_position[1] - 1
            elif grid.get((new_position[0], new_position[1] - 1)) == "#":
                return new_position
            else:
                # wrap back to the bottom
                bottommost = find_bottommost(grid, new_position[0])
                if grid[bottommost] == ".":
                    new_position = bottommost
                else:
                    return new_position
    return new_position


def wrap_around(position: Tuple[int, int], facing: str, box_size: int) -> Tuple[
    Tuple[int, int], str]:
    if facing == "up":
        # E, B, A
        if position[1] == 2 * box_size + 1:  # E, C
            x = box_size + 1
            y = position[0] + box_size
            facing = "right"
        elif box_size < position[0] <= 2 * box_size:  # B, F
            x = 1
            y = position[0] + 2 * box_size
            facing = "right"
        else:  # A, F
            x = position[0] - 2 * box_size
            y = 4 * box_size
            facing = "up"
    elif facing == "left":
        # B, C, E, F
        if position[1] <= box_size:  # B, E
            x = 1
            y = 3 * box_size + 1 - position[1]
            facing = "right"
        elif position[1] <= 2 * box_size:  # C, E
            x = position[1] - box_size
            y = 2 * box_size + 1
            facing = "down"
        elif position[1] <= 3 * box_size:  # E, B
            x = box_size + 1
            y = (box_size + 1) - (position[1] - 2 * box_size)
            facing = "right"
        else:  # F, B
            x = position[1] - 2 * box_size
            y = 1
            facing = "down"
    elif facing == "right":
        # A, C, D, F
        if position[0] == 3 * box_size:  # A, D
            x = 2 * box_size
            y = 3 * box_size + 1 - position[1]
            facing = "left"
        elif position[0] == 2 * box_size and box_size < position[1] <= 2 * box_size:  # C, A
            x = position[1] + box_size
            y = box_size
            facing = "up"
        elif position[0] == 2 * box_size:  # D, A
            x = 3 * box_size
            y = (box_size + 1) - (position[1] - 2 * box_size)
            facing = "left"
        else:  # F, D
            x = position[1] - 2 * box_size
            y = 3 * box_size
            facing = "up"
    else:  # down
        # A, D, F
        if position[1] == box_size:  # A, C
            x = 2 * box_size
            y = position[0] - box_size
            facing = "left"
        elif position[1] == 3 * box_size:  # D, F
            x = box_size
            y = position[0] + 2 * box_size
            facing = "left"
        else:  # F, A
            x = position[0] + 2 * box_size
            y = 1
            facing = "down"

    return (x, y), facing


def move_cube(grid: Dict[Tuple[int, int], str], position: Tuple[int, int], facing: str, spaces: int, box_size: int) -> \
        Tuple[Tuple[int, int], str]:
    new_position = position
    for _ in range(spaces):
        if facing == "right":
            # try to move one to the right
            if grid.get((new_position[0] + 1, new_position[1])) == ".":
                new_position = new_position[0] + 1, new_position[1]
            elif grid.get((new_position[0] + 1, new_position[1])) == "#":
                return new_position, facing
            else:
                wrapped_position, wrapped_facing = wrap_around(new_position, facing, box_size)
                if grid[wrapped_position] == ".":
                    new_position, facing = wrapped_position, wrapped_facing
                else:
                    return new_position, facing
        elif facing == "down":
            # try to move one down
            if grid.get((new_position[0], new_position[1] + 1)) == ".":
                new_position = new_position[0], new_position[1] + 1
            elif grid.get((new_position[0], new_position[1] + 1)) == "#":
                return new_position, facing
            else:
                wrapped_position, wrapped_facing = wrap_around(new_position, facing, box_size)
                if grid[wrapped_position] == ".":
                    new_position, facing = wrapped_position, wrapped_facing
                else:
                    return new_position, facing
        elif facing == "left":
            # try to move one to the left
            if grid.get((new_position[0] - 1, new_position[1])) == ".":
                new_position = new_position[0] - 1, new_position[1]
            elif grid.get((new_position[0] - 1, new_position[1])) == "#":
                return new_position, facing
            else:
                wrapped_position, wrapped_facing = wrap_around(new_position, facing, box_size)
                if grid[wrapped_position] == ".":
                    new_position, facing = wrapped_position, wrapped_facing
                else:
                    return new_position, facing
        else:  # up
            # try to move one up
            if grid.get((new_position[0], new_position[1] - 1)) == ".":
                new_position = new_position[0], new_position[1] - 1
            elif grid.get((new_position[0], new_position[1] - 1)) == "#":
                return new_position, facing
            else:
                wrapped_position, wrapped_facing = wrap_around(new_position, facing, box_size)
                if grid[wrapped_position] == ".":
                    new_position, facing = wrapped_position, wrapped_facing
                else:
                    return new_position, facing

    return new_position, facing


FACING = ["right", "down", "left", "up"]


def part_one(data):
    _map, instructions = data
    grid = parse_map(_map)
    instructions = parse_instructions(instructions[0])
    position = find_leftmost(grid)
    facing = "right"
    for action in instructions:
        if action == "R":
            facing = FACING[(FACING.index(facing) + 1) % len(FACING)]
        elif action == "L":
            facing = FACING[(FACING.index(facing) - 1) % len(FACING)]
        else:
            position = move(grid, position, facing, action)

    return 1000 * position[1] + (4 * position[0]) + FACING.index(facing)


def part_two(data):
    _map, instructions = data
    box_size = 50
    grid = parse_map(_map)
    instructions = parse_instructions(instructions[0])
    position = find_leftmost(grid)
    facing = "right"
    for action in instructions:
        if action == "R":
            facing = FACING[(FACING.index(facing) + 1) % len(FACING)]
        elif action == "L":
            facing = FACING[(FACING.index(facing) - 1) % len(FACING)]
        else:
            position, facing = move_cube(grid, position, facing, action, box_size)

    return 1000 * position[1] + (4 * position[0]) + FACING.index(facing)


# 200164, 97352
# 13236 is too low, 132144 is too high
if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_grouped_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
