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
    is_on: bool
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def overlap(self, other):
        min_x, max_x = max(self.min_x, other.min_x), min(self.max_x, other.max_x)
        min_y, max_y = max(self.min_y, other.min_y), min(self.max_y, other.max_y)
        min_z, max_z = max(self.min_z, other.min_z), min(self.max_z, other.max_z)
        if max_x >= min_x and max_y >= min_y and max_z >= min_z:
            return CubeRange(self._is_overlap_on(other), min_x, max_x, min_y, max_y, min_z, max_z)

    def _is_overlap_on(self, other):
        if self.is_on and other.is_on:
            return False
        return (not self.is_on and not other.is_on) or other.is_on

    def size(self) -> int:
        val = (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1) * (self.max_z - self.min_z + 1)
        return val if self.is_on else -val


def find_overlaps(on_ranges, incoming_range):
    overlaps = []
    for on_range in on_ranges:
        overlapping_range = incoming_range.overlap(on_range)
        if overlapping_range:
            overlaps.append(overlapping_range)

    return overlaps


def part_two(data):
    """
    first attempt....
    on_ranges = set()
    blah = set()
    for (is_on, ranges) in data:
        x_r, y_r, z_r = ranges
        cube_range = CubeRange(x_r[0], x_r[1], y_r[0], y_r[1], z_r[0], z_r[1])
        for overlapping_range in find_overlaps(on_ranges, cube_range):
            blah.add(overlapping_range)
        if is_on:
            on_ranges.add(cube_range)

    return sum([r.size() for r in on_ranges]) - sum([r.size() for r in blah])
    """
    """
    second attempt...
    total_size = 0
    prev = []
    for (is_on, ranges) in data:
        x_r, y_r, z_r = ranges
        cube_range = CubeRange(x_r[0], x_r[1], y_r[0], y_r[1], z_r[0], z_r[1])
        for prev_cube in prev:
            overlap = prev_cube.overlap(cube_range)
            if overlap:
                total_size -= overlap.size()
        if is_on:
            prev.append(cube_range)
            total_size += cube_range.size()
    return total_size
    """
    on_ranges = []
    for (is_on, ranges) in data:
        x_r, y_r, z_r = ranges
        cube_range = CubeRange(is_on, x_r[0], x_r[1], y_r[0], y_r[1], z_r[0], z_r[1])
        to_add = []
        for prev_cube in on_ranges:
            overlap = prev_cube.overlap(cube_range)
            if overlap:
                to_add.append(overlap)

        on_ranges.extend(to_add)
        if is_on:
            on_ranges.append(cube_range)

    return sum([r.size() for r in on_ranges])


def test(*args):
    data = [
        (True, [(10, 12), (10, 12), (10, 12)]),
        (False, [(10, 11), (10, 11), (10, 11)]),
        (True, [(10, 11), (10, 11), (10, 11)]),
    ]
    cube_range = CubeRange(True, 5, 7, 10, 11, 10, 11)
    other = CubeRange(True, 7, 9, 110, 111, 110, 111)
    return cube_range.overlap(other)


if __name__ == "__main__":
    for puzzle in ("sample", 1,):
        for f in (part_one, part_two,):
            data = get_input(__file__, puzzle=puzzle, coerce=parse)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
