#!/usr/bin/env python3

from lib_inputs import get_input


def part_one(data):
    m = len(data) / 2
    num_of_bits = len(data[0])

    g_s = "".join([str(int(sum([int(x[i]) for x in data]) >= m)) for i in range(num_of_bits)])

    return int(g_s, 2) * int("".join([str(int(not bool(int(x)))) for x in g_s]), 2)


def filter_data(data, bit_position, target):
    return [value for value in data if value[bit_position] == target]


def select_bit(bit_criteria, summed, m):
    if bit_criteria == "most":
        return "1" if summed >= m else "0"

    return "0" if summed >= m else "1"


def find_rating(data, bit_position, bit_criteria):
    if len(data) == 1:
        return int(data[0], 2)

    summed = sum([int(s[bit_position]) for s in data])
    return find_rating(filter_data(data, bit_position, select_bit(bit_criteria, summed, len(data) / 2)), bit_position + 1, bit_criteria)


def part_two(data):
    o = find_rating(data, 0, "most")
    c = find_rating(data, 0, "least")
    return o * c


for puzzle in ("sample", 1):
    data = get_input(3, puzzle=puzzle, coerce=str)
    print(f"Part 1: Input {puzzle}, {part_one(data)}")
    print(f"Part 2: Input {puzzle}, {part_two(data)}")
