#!/usr/bin/env python3

from lib_inputs import get_input

from collections import defaultdict


def parse(line):
    return [int(v) for v in line.split(",")]


def part(data, days):
    by_day = defaultdict(int)
    for fish in data:
        by_day[fish] += 1

    def advance(some_dict):
        new_day = defaultdict(int)
        for fish, count in some_dict.items():
            fish -= 1
            if fish == -1:
                new_day[8] += count
                fish = 6
            new_day[fish] += count

        return new_day

    for day in range(days):
        by_day = advance(by_day)

    return sum(by_day.values())


for puzzle in ("sample", 1):
    data = get_input(__file__, puzzle=puzzle, coerce=parse)
    print(f"Part 1: Input {puzzle}, {part(data, 80)}")
    print(f"Part 2: Input {puzzle}, {part(data, 256)}")
