#!/usr/bin/env python3

from lib_inputs import get_input

BY_LENGTH = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}


def parse(line):
    signals, nums = line.split(" | ")

    return [frozenset(s) for s in signals.split(" ")], [frozenset(n) for n in nums.split(" ")]


def part_one(data):
    return sum([len([num for num in nums if len(num) in {2, 3, 4, 7}])
                for _, nums in data])


def partial_solve(signals, mapping, reverse):
    for signal in signals:
        if signal in mapping:
            continue

        # 1, 4, 7, 8
        if len(signal) in BY_LENGTH:
            mapping[signal] = BY_LENGTH[len(signal)]
            reverse[mapping[signal]] = signal

        # 0, 6, 9
        elif len(signal) == 6 and len(reverse) >= 4:
            four = reverse[4]
            seven = reverse[7]
            if set(signal).issuperset(four) and set(signal).issuperset(seven):
                mapping[signal] = 9
            elif set(signal).issuperset(seven):
                mapping[signal] = 0
            else:
                mapping[signal] = 6
                reverse[6] = signal

        # 2, 3, 5
        elif len(signal) == 5 and len(reverse) == 5:
            one = reverse[1]
            six = reverse[6]
            if set(signal).issuperset(one):
                mapping[signal] = 3
            elif set(signal).issubset(six):
                mapping[signal] = 5
            else:
                mapping[signal] = 2


def part_two(data):
    total = 0
    for signals, nums in data:
        mapping, reverse = {}, {}
        while len(mapping) != len(signals):
            partial_solve(signals, mapping, reverse)

        total += int("".join([str(mapping[n]) for n in nums]))
    return total


for puzzle in ("sample", 1):
    data = get_input(__file__, puzzle=puzzle, coerce=parse)
    print(f"Part 1: Input {puzzle}, {part_one(data)}")
    print(f"Part 2: Input {puzzle}, {part_two(data)}")
