import sys
from collections import defaultdict

from utils.inputs import get_grouped_inputs


def is_possible(pattern, towels):
    options = set()
    for i, c in enumerate(pattern):
        if i == 0:
            for towel in towels:
                if pattern.startswith(towel):
                    options.add(towel)
        elif options:
            updates = set()
            for option in options:
                if len(option) == i: #
                    for towel in towels:
                        if pattern.startswith(option + towel):
                            updates.add(option + towel)
                elif option[i] == c:
                    updates.add(option)
            options = updates
    return bool(options)

def part_one(data: list[list[str]]):
    towels_lines, patterns = data
    towels = towels_lines[0].split(", ")
    return sum(1 for pattern in patterns if is_possible(pattern, towels))

def longest_towel(towels) -> int:
    most = 0
    for towel in towels:
        l = len(towel)
        most = max(most, l)

    return most


def part_two(data):
    towels_lines, patterns = data
    towels = towels_lines[0].split(", ")
    possible = 0
    longest = longest_towel(towels)

    """
    brute force does not work, options gets into the millions and the for loops kill it
    ideas:
    - use dicts instead of for loops
    - break pattern into substring patterns, then multiple the options -> don't know how to handle boundary though
    - pre-compute options counts then just apply them to the substring patterns
    - remove the one letter towels, add them back in somehow later
    """

    for pattern in patterns:
        if not is_possible(pattern, towels):
            continue

    return possible


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")