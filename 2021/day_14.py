#!/usr/bin/env python3
from collections import Counter, defaultdict
from copy import copy
from dataclasses import dataclass
from typing import List

from lib_inputs import get_input


@dataclass
class PolymerTemplate:
    as_str: str
    rules: List[str]

    def apply_rules(self):
        as_list = list(self.as_str)
        for rule in self.rules:
            target, insert = rule.split(" -> ")
            start = 0
            while self.as_str.count(target, start):
                found = self.as_str.index(target, start)
                as_list[found] += insert
                start = found + 1
        self.as_str = "".join(as_list)


def to_input(data):
    return PolymerTemplate(data[0], data[2:])


def part_one(data):
    polymer = to_input(data)
    for step in range(10):
        polymer.apply_rules()

    counts = Counter(polymer.as_str).most_common()
    return counts[0][1] - counts[-1][1]


def min_max(pairs, template):
    counts = defaultdict(int)
    for k in pairs:
        for c in k:
            counts[c] += pairs[k]

    minny, maxxy = None, None
    for c, count in counts.items():
        actual = (count // 2) + 1 if c in (template[0], template[-1]) else count // 2
        if minny is None or actual < minny:
            minny = actual

        if maxxy is None or actual > maxxy:
            maxxy = actual
    return maxxy - minny


def part_two(data):
    template, rules = data[0], data[2:]
    pairs = defaultdict(int)
    for i, c in enumerate(template[:-1]):
        pairs[c + template[i + 1]] += 1

    for i in range(40):
        updated = copy(pairs)
        for rule in rules:
            target, insert = rule.split(" -> ")
            if target in pairs:
                count = pairs[target]
                updated[target[0] + insert] += count
                updated[insert + target[1]] += count
                updated[target] -= count
                if updated[target] == 0:
                    updated.pop(target)
        pairs = copy(updated)

    return min_max(pairs, template)


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=str)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
