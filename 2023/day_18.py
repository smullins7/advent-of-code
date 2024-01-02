import re
from dataclasses import dataclass

from utils.algos import shoelace_area
from utils.binary import hex_to_int
from utils.graphs import SparseGrid
from utils.inputs import get_inputs

PAT = re.compile(r"^(?P<direction>[UDLR]) (?P<length>\d+) \(#(?P<hex>.*)\)$")


@dataclass
class Dig:
    direction: str
    length: int
    hex: str

    @staticmethod
    def parse(line):
        m = PAT.match(line)
        return Dig(m.group("direction"), int(m.group("length")), m.group("hex"))

    def parse_from_hex(self):
        DIRS = {
            "0": "R",
            "1": "D",
            "2": "L",
            "3": "U"
        }
        length = hex_to_int(self.hex[:-1])
        direction = DIRS[self.hex[-1]]
        return Dig(direction, length, self.hex)


def calculate_area(sparse_grid: SparseGrid) -> int:
    area = 0
    buf = []
    for y in reversed(range(sparse_grid.min_y, sparse_grid.max_y + 1)):
        include = False
        for x in range(sparse_grid.min_x, sparse_grid.max_x + 1):
            if sparse_grid.has(x, y):
                area += 1
                if sparse_grid.has(x, y + 1):
                    include = not include
                buf.append("#")
            elif include:
                area += 1
                buf.append("#")
            else:
                buf.append(".")
        buf.append("\n")

    # print("".join(buf))
    return area


def part_one(data):
    space = SparseGrid()
    x, y = 0, 0
    space.set(x, y)
    for dig in data:
        if dig.direction == "R":
            for i in range(x, x + dig.length):
                space.set(i + 1, y)
            x = i + 1
        elif dig.direction == "L":
            for i in reversed(range(x - dig.length, x)):
                space.set(i, y)
            x = i
        if dig.direction == "U":
            for i in range(y, y + dig.length):
                space.set(x, i + 1)
            y = i + 1
        elif dig.direction == "D":
            for i in reversed(range(y - dig.length, y)):
                space.set(x, i)
            y = i

    return calculate_area(space)


def part_two(data):
    space = SparseGrid()
    x, y = 0, 0
    space.set(x, y)
    border = 1
    for dig in data:
        dig = dig.parse_from_hex()
        direction, length = dig.direction, dig.length
        border += length
        if direction == "R":
            space.set(x + length, y)
            x += length
        elif direction == "L":
            space.set(x - length, y)
            x -= length
        if direction == "U":
            space.set(x, y + length)
            y += length
        elif direction == "D":
            space.set(x, y - length)
            y -= length
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return int(abs(shoelace_area(space.values.keys())) + int(border / 2) + 1)


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=Dig.parse)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
