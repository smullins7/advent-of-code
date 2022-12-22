from typing import Tuple, Dict

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
    return parsed


def parse_map(_map):
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
    return 0


# 200164, 97352
if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_grouped_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
