#!/usr/bin/env python3

from lib_inputs import get_input


def part_one(data):
    prev = data[0]
    asc_count = 0
    for value in data[1:]:
        asc_count += bool(value - prev > 0)
        prev = value

    return asc_count


def part_two(data):
    prev = data[0:3]
    asc_count = 0
    for value in data[3:]:
        current = prev[1:] + [value]
        asc_count += bool(sum(current) - sum(prev) > 0)
        prev = current

    return asc_count


for puzzle in ("sample", 1):
    data = get_input(1, puzzle=puzzle, coerce=int)
    print(f"Part 1: Input {puzzle}, {part_one(data)}")
    print(f"Part 2: Input {puzzle}, {part_two(data)}")
