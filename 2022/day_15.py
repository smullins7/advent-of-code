from dataclasses import dataclass

from utils.graphs import SparseValueGrid
from utils.inputs import get_input

import re

PAT = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


def coerce(line):
    m = PAT.match(line)
    return [int(g) for g in m.groups()]


def find_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def part_one(data):
    grid = SparseValueGrid({})
    for (x, y, bx, by) in data:
        grid.set(x, y, "S")
        grid.set(bx, by, "B")

        distance = find_distance(x, y, bx, by)

        if y == 2000000:
            # fill in current line
            for new_x in range(x - distance, x + distance + 1):
                if not grid.has(new_x, y):
                    grid.set(new_x, y, "#")

        # iterate up and down subtracting two each time
        for i in range(distance):
            if y + i + 1 == 2000000:
                # fill in row above
                for new_x in range(x - distance + i + 1, x + distance - i) or [x + distance - i]:
                    if not grid.has(new_x, y + i + 1):
                        grid.set(new_x, y + i + 1, "#")

            if y - i - 1 == 2000000:
                # fill in row below
                for new_x in range(x - distance + i + 1, x + distance - i) or [x + distance - i]:
                    if not grid.has(new_x, y - i - 1):
                        grid.set(new_x, y - i - 1, "#")

    c = 0
    for x, y in grid.values:
        if y == 2000000 and grid.get(x, y) == "#":
            c += 1
    return c


@dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int
    distance: int = 0

    def __post_init__(self):
        self.distance = find_distance(self.x, self.y, self.beacon_x, self.beacon_y)

    def within_range(self, x, y):
        return find_distance(self.x, self.y, x, y) <= self.distance

    def border_range(self):
        """Return all the points just outside the range of the sensor"""
        points = []

        for i in range(self.distance + 1):
            # add N -> E
            points.append((self.x + i, self.y + self.distance + 1 - i))

            # add E -> S
            points.append((self.x + self.distance + 1 - i, self.y - i))

            # add S -> W
            points.append((self.x - i, self.y - self.distance - 1 + i))

            # add W -> N
            points.append((self.x - self.distance - 1 + i, self.y + i))

        return points


def part_two(data):
    sensors = []
    for (x, y, bx, by) in data:
        sensors.append(Sensor(x, y, bx, by))

    for sensor in sensors:
        for point in sensor.border_range():
            if not 0 <= point[0] <= 4000000 or not 0 <= point[1] <= 4000000:
                continue
            viable = True
            for other_sensor in sensors:
                if sensor.x == other_sensor.x and sensor.y == other_sensor.y:
                    continue

                if other_sensor.within_range(*point):
                    viable = False
                    break
            if viable:
                return point[0] * 4000000 + point[1]


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=coerce)
        print(f"{f.__name__}:\n\t{f(data)}")
