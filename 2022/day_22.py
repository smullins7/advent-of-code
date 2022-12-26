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


@dataclass
class Box:
    min_x: int
    min_y: int
    max_x: int
    max_y: int


class Cube:
    pass


def parse_cube(_map: List[str], box_size: int):
    boxes = set()
    for y, line in enumerate(_map):
        for x, c in enumerate(line):
            if c in (".", "#"):
                pass


HARD_CODES = {
    (4, 6): 17,
    (5, 2): 5,
    #(3, 1): 5,
}

def transpose(value: int, box_size: int) -> int:
    return value % box_size or box_size


def wrap_around(grid: Dict[Tuple[int, int], str], position: Tuple[int, int], facing: str, box_size: int) -> Tuple[
    Tuple[int, int], str]:
    if facing == "up":
        # 1, 2, 3, 6
        if position[1] == 1:  # 1 -> 2
            y = position[1] + box_size
            #x =
            facing = "down"
        elif position[1] == box_size + 1 and position[0] <= box_size:  # 2 -> 1
            facing = "down"
        elif position[1] == box_size + 1:  # 3 -> 1
            facing = "right"
            x = 9
            y = transpose(position[0], box_size)
            return (x, y), facing
        else:  # 6 -> 4
            facing = "left"
    elif facing == "left":
        # 1, 2, 5
        if position[1] <= box_size:  # 1 -> 3
            facing = "down"
        elif position[0] == 1:  # 2 -> 6
            facing = "up"
        else:  # 5 -> 3
            facing = "up"
    elif facing == "right":
        # 1, 4, 6
        if position[1] <= box_size:  # 1 -> 6
            facing = "left"
        if box_size < position[1] <= box_size * 2:  # 4 -> 6
            y = 9
            x = HARD_CODES[(4, 6)] - transpose(position[1], box_size)
            facing = "down"
            return (x, y), facing
        else:  # 6 -> 1
            facing = "left"
    else:  # down
        # 2, 3, 5, 6
        if position[0] <= box_size:  # 2 -> 5
            facing = "up"
        elif position[0] <= box_size * 2:  # 3 -> 5
            facing = "right"
        elif position[0] <= box_size * 3:  # 5 -> 2
            y = 8
            x = HARD_CODES[(5, 2)] - transpose(position[0], box_size)
            facing = "up"
            return (x, y), facing
        else:  # 6 -> 2
            facing = "up"


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
                wrapped_position, wrapped_facing = wrap_around(grid, new_position, facing, box_size)
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
                wrapped_position, wrapped_facing = wrap_around(grid, new_position, facing, box_size)
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
                wrapped_position, wrapped_facing = wrap_around(grid, new_position, facing, box_size)
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
                wrapped_position, wrapped_facing = wrap_around(grid, new_position, facing, box_size)
                if grid[wrapped_position] == ".":
                    new_position, facing = wrapped_position, wrapped_facing
                else:
                    return new_position, facing

    return new_position, facing


FACING = ["right", "down", "left", "up"]


def part_one(data, **kwargs):
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


def part_two(data, is_sample=True):
    _map, instructions = data
    box_size = 4 if is_sample else 50
    # cube = parse_cube(_map, box_size)
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
if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_grouped_input(__file__, is_sample=1)
        print(f"{f.__name__}:\n\t{f(data)}")
