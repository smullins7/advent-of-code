#!/usr/bin/env python3

from lib_inputs import get_input

from dataclasses import dataclass
from collections import defaultdict


def safe_range(a, b):
    if a < b:
        return range(a, b + 1)
    return reversed(range(b, a + 1))


@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def points(self, diagonal=False):
        p = []
        if self.x1 == self.x2:
            p.extend(map(lambda v: (self.x1, v), safe_range(self.y1, self.y2)))

        if self.y1 == self.y2:
            p.extend(map(lambda v: (v, self.y1), safe_range(self.x1, self.x2)))

        if diagonal and self.x1 != self.x2 and self.y1 != self.y2:
            p.extend(zip(safe_range(self.x1, self.x2), safe_range(self.y1, self.y2)))

        return p

    @staticmethod
    def from_str(s):
        return Line(*map(int, [item for sublist in [s2.split(",") for s2 in s.split(" -> ")] for item in sublist]))


def part_one_or_two(data, include_diagonal):
    points = defaultdict(int)
    for line in data:
        for point in line.points(diagonal=include_diagonal):
            points[point] += 1
    return len([v for v in points.values() if v >= 2])


for puzzle in ("sample", 1):
    data = get_input(5, puzzle=puzzle, coerce=Line.from_str)
    print(f"Part 1: Input {puzzle}, {part_one_or_two(data, False)}")
    print(f"Part 2: Input {puzzle}, {part_one_or_two(data, True)}")
