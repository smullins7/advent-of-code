#!/usr/bin/env python3
import itertools
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from typing import List, Dict

from lib_inputs import get_input

ROTATIONS = [
    lambda p: p.rotate(p.x, p.y, p.z),  #
    lambda p: p.rotate(-p.x, -p.y, p.z),  #
    lambda p: p.rotate(p.x, -p.y, -p.z),  #
    lambda p: p.rotate(-p.x, p.y, -p.z),  #

    lambda p: p.rotate(p.x, -p.z, p.y),  #
    lambda p: p.rotate(-p.x, -p.z, -p.y),  #
    lambda p: p.rotate(p.x, p.z, -p.y),  #
    lambda p: p.rotate(-p.x, p.z, p.y),  #

    lambda p: p.rotate(p.y, p.x, -p.z),  #
    lambda p: p.rotate(p.y, -p.x, p.z),  #
    lambda p: p.rotate(p.y, p.z, p.x),  #
    lambda p: p.rotate(p.y, -p.z, -p.x),  #
    lambda p: p.rotate(-p.y, p.x, p.z),  #
    lambda p: p.rotate(-p.y, -p.x, -p.z),  #
    lambda p: p.rotate(-p.y, -p.z, p.x),  #
    lambda p: p.rotate(-p.y, p.z, -p.x),  #

    lambda p: p.rotate(p.z, -p.y, p.x),  #
    lambda p: p.rotate(p.z, p.x, p.y),  #
    lambda p: p.rotate(p.z, -p.x, -p.y),  #
    lambda p: p.rotate(p.z, p.y, -p.x),  #
    lambda p: p.rotate(-p.z, p.y, p.x),  #
    lambda p: p.rotate(-p.z, -p.y, -p.x),  #
    lambda p: p.rotate(-p.z, p.x, -p.y),  #
    lambda p: p.rotate(-p.z, -p.x, p.y),  #
]


def make_scanner(scan_id, beacons):
    distances = defaultdict(list)
    for pair in itertools.permutations(beacons, 2):
        distances[pair[0]].append(pair[0].vector(pair[1]))
    return Scanner(scan_id, distances)


def to_scanners(data):
    scanners = []
    scan_id = None
    beacons = []
    for line in data:
        if not line:
            scanners.append(make_scanner(scan_id, beacons))
            beacons = []
        elif line.count("scanner"):
            scan_id = int(line.split(" ")[2])
        else:
            beacons.append(Point3D(*[int(v) for v in line.split(",")]))

    if beacons:
        scanners.append(make_scanner(scan_id, beacons))
    return scanners


@dataclass(unsafe_hash=True)
class Point3D:
    x: int
    y: int
    z: int = 0

    def vector(self, other):
        return self.x - other.x, self.y - other.y, self.z - other.z

    def __repr__(self):
        return f"P({self.x},{self.y},{self.z})"

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def rotate(self, new_x, new_y, new_z):
        self.x = new_x
        self.y = new_y
        self.z = new_z

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z


@dataclass(unsafe_hash=True)
class Distance:
    p1: Point3D
    p2: Point3D


@dataclass
class Scanner:
    sid: int
    points: Dict[Point3D, List[Distance]]

    def get_points(self) -> List[Point3D]:
        return list(self.points.keys())


def compare_distance_sets(d1, d2):
    return len(set(d1).intersection(set(d2)))


def point_offset(p1, p2):
    return p1.x - p2.x, p1.y - p2.y, p1.z - p2.z


def detect_scanner_overlap(target_scanner, other_scanner):
    for potential_same_point, distances in target_scanner.points.items():
        for other_point, other_distances in other_scanner.points.items():
            if compare_distance_sets(distances, other_distances) >= 11:
                print(f"Scanners {target_scanner.sid} and {other_scanner.sid} appear to overlap")
                return potential_same_point, other_point
    return None


def part_one(data):
    scanners = to_scanners(data)
    scanner_zero = scanners.pop(0)
    while scanners:
        other_scanner = scanners.pop(0)
        found = False
        for i, rotation in enumerate(ROTATIONS):
            print(f"{other_scanner.sid}, {i}")
            temp_points = [copy(point) for point in other_scanner.points]
            for p in temp_points:
                rotation(p)
            rotated_scanner = make_scanner(other_scanner.sid, temp_points)
            overlaps = detect_scanner_overlap(scanner_zero, rotated_scanner)
            if overlaps:
                found = True
                offsets = point_offset(*overlaps)
                for point in rotated_scanner.points:
                    point.move(*offsets)
                print(len(scanner_zero.get_points()))
                scanner_zero = make_scanner(scanner_zero.sid,
                                            list(set(scanner_zero.get_points() + rotated_scanner.get_points())))
                print(len(scanner_zero.get_points()))
                break
        if not found:
            scanners.append(other_scanner)

    return len(scanner_zero.points)


def part_two(data):

    scanners = to_scanners(data)
    scanner_zero = scanners.pop(0)
    scanner_coordinates = {
        0: (0, 0, 0)
    }
    while scanners:
        other_scanner = scanners.pop(0)
        found = False
        for i, rotation in enumerate(ROTATIONS):
            #print(f"{other_scanner.sid}, {i}")
            temp_points = [copy(point) for point in other_scanner.points]
            for p in temp_points:
                rotation(p)
            rotated_scanner = make_scanner(other_scanner.sid, temp_points)
            overlaps = detect_scanner_overlap(scanner_zero, rotated_scanner)
            if overlaps:
                found = True
                offsets = point_offset(*overlaps)
                for point in rotated_scanner.points:
                    point.move(*offsets)
                #print(len(scanner_zero.get_points()))
                scanner_zero = make_scanner(scanner_zero.sid,
                                            list(set(scanner_zero.get_points() + rotated_scanner.get_points())))
                #print(len(scanner_zero.get_points()))
                scanner_coordinates[other_scanner.sid] = offsets
                break
        if not found:
            scanners.append(other_scanner)

    m = 0
    for left, right in itertools.combinations(scanner_coordinates.values(), 2):
        m = max(m, manhattan_d(left, right))
    return m


def manhattan_d(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1]) + abs(p0[2] - p1[2])


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
