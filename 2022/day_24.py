from collections import defaultdict
from typing import Tuple

from utils.inputs import get_input


MOVES = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

class BlizzardGrid:

    def __init__(self):
        self.grid = defaultdict(list)
        self.max_x = 0
        self.max_y = 0
        self.round = 0

    def set(self, x, y, c):
        self.grid[(x, y)].append(c)
        self.max_x = max(x, self.max_x)
        self.max_y = max(y, self.max_y)

    def print(self, expedition):
        to_print = ""
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                values = [c for c in self.grid[(x, y)] if c != "."]
                if expedition == (x, y):
                    to_print += "E"
                elif len(values) == 0:
                    to_print += "."
                elif len(values) == 1:
                    to_print += values[0]
                else:
                    to_print += str(len(values))
            to_print += "\n"
        print(to_print)

    def move_blizzard(self):
        removes = []
        appends = []
        for y in range(1, self.max_y):
            for x in range(1, self.max_x):
                for c in self.grid[(x, y)]:
                    move_x, move_y = MOVES.get(c, (0, 0))
                    new_x = x + move_x
                    new_y = y + move_y
                    if new_x == 0:
                        new_x = self.max_x - 1
                    elif new_x == self.max_x:
                        new_x = 1

                    if new_y == 0:
                        new_y = self.max_y - 1
                    elif new_y == self.max_y:
                        new_y = 1
                    if (x, y) != (new_x, new_y):
                        removes.append((x, y, c))
                        appends.append((new_x, new_y, c))
        for x, y, c in removes:
            self.grid[(x, y)].remove(c)
        for x, y, c in appends:
            self.grid[(x, y)].append(c)

        self.round += 1
    def snow_count(self, x, y):
        return len([c for c in self.grid[(x, y)] if c != "."])

    def possible_expedition_moves(self, current, goal):
        moves = []
        x, y = current
        if not self.snow_count(x, y):
            moves.append((x, y))
        for move_x, move_y in MOVES.values():
            new_x = x + move_x
            new_y = y + move_y
            if (new_x, new_y) == goal:
                return [(new_x, new_y)]

            if 0 < new_x < self.max_x and 0 < new_y < self.max_y and not self.snow_count(new_x, new_y):
                moves.append((new_x, new_y))
        return moves

    def fingerprint(self):
        data = set()
        for (x, y), values in self.grid.items():
            for v in values:
                if v != ".":
                    data.add((x, y, v))
        return frozenset(data)


def blizzard_grid(data) -> BlizzardGrid:
    grid = BlizzardGrid()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            grid.set(x, y, c)
    return grid


def fingerprints(bliz_grid: BlizzardGrid):
    starting_fingerprint = bliz_grid.fingerprint()
    count = 0
    cache = {}
    while True:
        bliz_grid.move_blizzard()
        count += 1
        cache[count] = bliz_grid.fingerprint()
        if cache[count] == starting_fingerprint:
            return cache


def shortest_distance(bliz_grid: BlizzardGrid, start, end, fingies):
    cycle_count = len(fingies)
    to_check = [
        # blizzard level
        [
            # paths
            [start]
        ]

    ]
    cache = set()
    while to_check:
        blizzard_level = to_check.pop(0)
        next_blizzard = []
        bliz_grid.move_blizzard()
        fingerprint = fingies[(bliz_grid.round % cycle_count) or cycle_count]
        for path in blizzard_level:
            exp = path[-1]
            for new_expedition in bliz_grid.possible_expedition_moves(exp, end):
                if new_expedition == end:
                    return len(path)

                key = (fingerprint, new_expedition)
                if key not in cache:
                    cache.add(key)
                    next_blizzard.append(path + [new_expedition])
        if next_blizzard:
            to_check.append(next_blizzard)


def part_one(data):
    bliz_grid = blizzard_grid(data)
    fingies = fingerprints(bliz_grid)
    return shortest_distance(bliz_grid, (1, 0), (bliz_grid.max_x - 1, bliz_grid.max_y), fingies)


def part_two(data):
    bliz_grid = blizzard_grid(data)
    fingies = fingerprints(bliz_grid)
    start = (1, 0)
    goal = (bliz_grid.max_x - 1, bliz_grid.max_y)
    there = shortest_distance(bliz_grid, start, goal, fingies)
    back = shortest_distance(bliz_grid, goal, start, fingies)
    again = shortest_distance(bliz_grid, start, goal, fingies)
    return sum([there, back, again])


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")

