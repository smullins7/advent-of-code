from collections import defaultdict
from itertools import cycle

from utils.inputs import get_input

ROCKS = [
    # horizontal line
    lambda y: ((3, y), (4, y), (5, y), (6, y)),
    # plus sign
    lambda y: ((4, y), (3, y + 1), (4, y + 1), (5, y + 1), (4, y + 2)),
    # backward L
    lambda y: ((3, y), (4, y), (5, y), (5, y + 1), (5, y + 2)),
    # vertical line
    lambda y: ((3, y), (3, y + 1), (3, y + 2), (3, y + 3)),
    # box
    lambda y: ((3, y), (4, y), (3, y + 1), (4, y + 1)),
]


def cycle_with_index(iterable):
    saved = []
    for i, element in enumerate(iterable):
        yield i, element
        saved.append((i, element))
    while saved:
        for pair in saved:
            yield pair


class Chamber:

    def __init__(self, jetstream, rocks):
        self.jetstream = cycle_with_index(jetstream)
        self.rocks = cycle_with_index(rocks)
        self.points = set([(x, 0) for x in range(1, 8)])  # initialize floor
        self.left_wall = 0
        self.right_wall = 8
        self.height = 0
        self.fallen_rocks = 0
        self.jet_index = -1
        self.rock_index = -1

    def next_rock_at(self):
        return self.height + 4  # problem says 3 units above but picture shows 4...

    def rock_settled(self, rock):
        return any([(x, y - 1) in self.points for (x, y) in rock])

    def apply_jetstream(self, rock):
        jet_index, move_right = next(self.jetstream)
        self.jet_index = jet_index
        if move_right:
            for x, y in rock:
                if (x + 1, y) in self.points or x + 1 == self.right_wall:
                    return rock

            return [(x + 1, y) for (x, y) in rock]
        else:
            for x, y in rock:
                if (x - 1, y) in self.points or x - 1 == self.left_wall:
                    return rock

            return [(x - 1, y) for (x, y) in rock]

    @staticmethod
    def move_down(rock):
        return [(x, y - 1) for x, y in rock]

    def next_rock(self):
        rock_index, rock_func = next(self.rocks)
        self.rock_index = rock_index
        rock = rock_func(self.next_rock_at())
        rock = self.apply_jetstream(rock)
        while not self.rock_settled(rock):
            rock = self.move_down(rock)
            rock = self.apply_jetstream(rock)
        for point in rock:
            self.points.add(point)
        self.height = max(self.height, max([y for x, y in rock]))
        self.fallen_rocks += 1

    def top_rocks(self):
        for x in range(self.left_wall + 1, self.right_wall):
            for y in range(self.height - 301, self.height + 1):
                if (x, y) in self.points:
                    yield x, 300 - (self.height - y)


def parse(line):
    return [c == ">" for c in line]


def print_chamber(chamber: Chamber):
    height = chamber.height
    print("Chamber:")
    for y in reversed(range(height + 3)):
        for x in range(chamber.left_wall, chamber.right_wall + 1):
            if (x == chamber.left_wall and y == 0) or (x == chamber.right_wall and y == 0):
                print("+", end="")
            elif x in (chamber.left_wall, chamber.right_wall):
                print("|", end="")
            elif y == 0:
                print("-", end="")
            elif (x, y) in chamber.points:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def part_one(jetstream):
    chamber = Chamber(jetstream, ROCKS)
    while chamber.fallen_rocks < 2022:
        chamber.next_rock()
    return chamber.height


def part_two(jetstream):
    chamber = Chamber(jetstream, ROCKS)

    # run plenty of times to "warm up"
    [chamber.next_rock() for _ in range(5000)]

    cache = dict()
    while True:
        chamber.next_rock()
        key = (chamber.jet_index, chamber.rock_index, tuple(chamber.top_rocks()))
        if key in cache:
            break
        else:
            cache[key] = chamber.fallen_rocks, chamber.height

    prev_fallen_rocks, prev_height = cache[key]

    adjusted_rock = prev_fallen_rocks
    rock_rate = chamber.fallen_rocks - prev_fallen_rocks
    height_rate = chamber.height - prev_height
    t = 1000000000000
    while (t - adjusted_rock) % rock_rate != 0:
        adjusted_rock += 1
        chamber.next_rock()

    return int(chamber.height + (height_rate * (t - chamber.fallen_rocks) / rock_rate))


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")
