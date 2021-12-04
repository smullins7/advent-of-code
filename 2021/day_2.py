#!/usr/bin/env python3

from lib_inputs import get_input


def parse(line):
    direction, scalar = line.split(" ")
    return direction, int(scalar)


def part_one(data):
    pos, depth = 0, 0
    for direction, scalar in data:
        if direction == "forward":
            pos += scalar
        elif direction == "up":
            depth -= scalar
        else:
            depth += scalar

    return pos * depth


def part_two(data):
    pos, depth, aim = 0, 0, 0
    for direction, scalar in data:
        if direction == "forward":
            pos += scalar
            depth += aim * scalar
        elif direction == "up":
            aim -= scalar
        else:
            aim += scalar

    return pos * depth


for puzzle in ("sample", 1):
    data = get_input(2, puzzle=puzzle, coerce=parse)
    print(f"Part 1: Input {puzzle}, {part_one(data)}")
    print(f"Part 2: Input {puzzle}, {part_two(data)}")
