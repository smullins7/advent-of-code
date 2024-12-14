from collections import defaultdict
from dataclasses import dataclass, field
from functools import reduce
from operator import mul

from utils.inputs import get_inputs

@dataclass(unsafe_hash=True)
class Robot:
    v_x: int
    v_y: int

    def __eq__(self, other):
        return self.v_x == other.v_x and self.v_y == other.v_y

@dataclass
class TileGrid:
    max_x: int = 11
    max_y: int = 7
    positions: dict[tuple[int, int],list[Robot]] = field(default_factory=lambda: defaultdict(list))

    def add_robot(self, x, y, v_x, v_y):
        self.positions[(x, y)].append(Robot(v_x, v_y))

    def move_robots(self):
        new_positions = defaultdict(list)
        for (x, y), robots in self.positions.items():
            for robot in robots:
                new_positions[((x + robot.v_x) % self.max_x, (y + robot.v_y) % self.max_y)].append(robot)

        self.positions = new_positions

    def quadrants(self) -> int:
        half_x = int(self.max_x / 2)
        half_y = int(self.max_y / 2)
        #        TL, TR, BR, BL
        quads = [0, 0, 0, 0]
        for (x, y) in self.positions:
            if x < half_x and y < half_y:
                quads[0] += len(self.positions[(x, y)])
            elif x > half_x and y < half_y:
                quads[1] += len(self.positions[(x, y)])
            elif x < half_x and y > half_y:
                quads[2] += len(self.positions[(x, y)])
            elif x > half_x and y > half_y:
                quads[3] += len(self.positions[(x, y)])

        print(quads)
        return reduce(mul, quads)

    def __str__(self):
        buf = []
        for y in range(0, self.max_y):
            for x in range(0, self.max_x):
                robots = self.positions[(x, y)]
                buf.append(str(len(robots)) if robots else ".")
            buf.append("\n")
        return "".join(buf)

def part_one(data, wide, tall):
    tile_grid = TileGrid(wide, tall)
    for line in data:
        p, v = line.split(" ")
        x, y = p.split("=")[1].split(",")
        v_x, v_y = v.split("=")[1].split(",")
        tile_grid.add_robot(int(x), int(y), int(v_x), int(v_y))

    for _ in range(100):
        tile_grid.move_robots()
    #print(tile_grid)
    return tile_grid.quadrants()


def maybe_tree(tile_grid: TileGrid):
    half_x = int(tile_grid.max_x / 2)
    for y in range(0, tile_grid.max_y):
        for left_x in range(0, half_x):
            left_robots = tile_grid.positions[(left_x, y)]
            right_robots = tile_grid.positions[(tile_grid.max_x - left_x - 1, y)] # off by one errors amiright???
            if len(left_robots) != len(right_robots):
                return False
    return True


def maybe_tree2(tile_grid: TileGrid, y):
    half_x = int(tile_grid.max_x / 2)
    for left_x in range(0, half_x):
        left_robots = tile_grid.positions[(left_x, y)]
        right_robots = tile_grid.positions[(tile_grid.max_x - left_x - 1, y)] # off by one errors amiright???
        if bool(len(left_robots)) != bool(len(right_robots)):
            return False
    return True

def no_overlaps(tile_grid: TileGrid):
    for robots in tile_grid.positions.values():
        if len(robots) > 1:
            return False
    return True

def part_two(data, wide, tall):
    tile_grid = TileGrid(wide, tall)
    for line in data:
        p, v = line.split(" ")
        x, y = p.split("=")[1].split(",")
        v_x, v_y = v.split("=")[1].split(",")
        tile_grid.add_robot(int(x), int(y), int(v_x), int(v_y))

    i = 1
    while True:
        tile_grid.move_robots()
        if no_overlaps(tile_grid):
            print(tile_grid)
            print(i)
            break
        i += 1

    return 0


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        #print(f"{f.__name__} sample:\n\t{f(sample_data, 11, 7)}")
        print(f"{f.__name__}:\n\t{f(real_data, 101, 103)}")