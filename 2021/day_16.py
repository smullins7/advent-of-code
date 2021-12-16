#!/usr/bin/env python3
from dataclasses import field, dataclass
from typing import List
from operator import mul
from functools import reduce

from lib_inputs import input_to_binary

LENGTH_TYPE_ID = 1
VERSION = 3
TYPE_ID = 3
LITERAL = 5
TOTAL_LENGTH_IN_BITS = 15
NUM_SUB_PACKETS = 11

OP = {
    0: sum,
    1: lambda v: reduce(mul, v),
    2: min,
    3: max,
    5: lambda v: 1 if v[0] > v[1] else 0,
    6: lambda v: 1 if v[0] < v[1] else 0,
    7: lambda v: 1 if v[0] == v[1] else 0
}


@dataclass
class BitsReader:
    binary_input: str
    cursor: int = 0
    versions: List[int] = field(default_factory=list)

    def read_packet(self):
        version = self.read_int(VERSION)
        self.versions.append(version)
        type_id = self.read_int(TYPE_ID)
        if type_id == 4:
            return self.read_literal()
        else:
            return self.read_operator(type_id)

    def read(self, length) -> str:
        data = self.binary_input[self.cursor:self.cursor + length]
        self.cursor += length
        return data

    def read_int(self, length) -> int:
        return int(self.read(length), 2)

    def read_literal(self) -> int:
        value = ""
        v = None
        while not v or v[0] == "1":
            v = self.read(LITERAL)
            value += v[1:]
        return int(value, 2)

    def read_operator(self, type_id):
        values = []
        length_type_id = self.read_int(LENGTH_TYPE_ID)
        if length_type_id == 0:
            total_length_in_bits = self.read_int(TOTAL_LENGTH_IN_BITS)
            stop_at = self.cursor + total_length_in_bits
            while self.cursor < stop_at:
                values.append(self.read_packet())
        else:
            for _ in range(self.read_int(NUM_SUB_PACKETS)):
                values.append(self.read_packet())

        return OP[type_id](values)


def part_one(data):
    bits_reader = BitsReader(data)
    bits_reader.read_packet()
    return sum(bits_reader.versions)


def part_two(data):
    bits_reader = BitsReader(data)
    return bits_reader.read_packet()


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = input_to_binary(__file__, puzzle=puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
