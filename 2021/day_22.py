#!/usr/bin/env python3
import itertools
from dataclasses import dataclass

from lib_inputs import get_input


# on x=10..12,y=10..12,z=10..12
def parse(line):
    on_off_s, ranges_s = line.split(" ")
    return on_off_s == "on", [[int(x) for x in r[2:].split("..")] for r in ranges_s.split(",")]


def _range(inclusive_list):
    min_v, max_v = inclusive_list[0], inclusive_list[1]
    return range(max(min_v, -50), min(max_v, 50) + 1)


def _len(inclusive_list):
    return inclusive_list[1] - inclusive_list[0] + 1


def part_one(data):
    sparse_points = {}
    for (is_on, ranges) in data:
        if len([item for sublist in ranges for item in sublist if -50 <= item <= 50]) != 6:
            continue
        x_r, y_r, z_r = ranges
        for x, y, z in itertools.product(_range(x_r), _range(y_r), _range(z_r)):
            sparse_points[(x, y, z)] = is_on
    return sum(sparse_points.values())


@dataclass(unsafe_hash=True)
class CubeRange:
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def overlap(self, other):
        if (other.min_x <= self.min_x <= other.max_x or other.min_x <= self.max_x <= other.max_x and
                other.min_y <= self.min_y <= other.max_y or other.min_y <= self.max_y <= other.max_y and
                other.min_z <= self.min_z <= other.max_z or other.min_z <= self.max_z <= other.max_z):
            return CubeRange(max(self.min_x, other.min_x), min(self.max_x, other.max_x),
                             max(self.min_y, other.min_y), min(self.max_y, other.max_y),
                             max(self.min_z, other.min_z), min(self.max_z, other.max_z))

    def size(self):
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1) * (self.max_z - self.min_z + 1)


def find_overlaps(on_ranges, incoming_range):
    overlaps = []
    for on_range in on_ranges:
        overlapping_range = incoming_range.overlap(on_range)
        if overlapping_range:
            overlaps.append(overlapping_range)

    return overlaps


def subtract(cube_range, removes):
    return []


def part_two(data):
    on_ranges = set()
    off_ranges = set()
    for (is_on, ranges) in data:
        x_r, y_r, z_r = ranges
        cube_range = CubeRange(x_r[0], x_r[1], y_r[0], y_r[1], z_r[0], z_r[1])
        overlaps = find_overlaps(on_ranges, cube_range)
        if is_on:
            if overlaps:
                [on_ranges.add(r) for r in overlaps]#subtract(cube_range, overlaps)]
            else:
                on_ranges.add(cube_range)
        else:
            [off_ranges.add(r) for r in overlaps]

    return sum([r.size() for r in on_ranges]) - sum([r.size() for r in off_ranges])


if __name__ == "__main__":
    for puzzle in ("sample",):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=parse)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
