#!/usr/bin/env python3

from lib_inputs import get_input


def parse(line):
    return str(line)


def part_one(data):
    return 0


def part_two(data):
    return 0


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=parse)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")

