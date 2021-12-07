#!/usr/bin/env python3

import statistics

from lib_inputs import get_input


def parse(line):
    return [int(v) for v in line.split(",")]


def part_one(data):
    m = int(statistics.median(data))
    return sum(map(lambda v: abs(v - m), data))


def part_two(data):
    m = int(statistics.mean(data))
    return sum(map(lambda v: sum(range(1, abs(v - m) + 1)), data))


for puzzle in ("sample", 1):
    data = get_input(__file__, puzzle=puzzle, coerce=parse)
    print(f"Part 1: Input {puzzle}, {part_one(data)}")
    print(f"Part 2: Input {puzzle}, {part_two(data)}")