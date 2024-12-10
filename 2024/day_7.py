from functools import reduce
from itertools import product

from utils.inputs import get_inputs


def to_eq(line):
    result, parts = line.split(": ")
    return int(result), [int(n) for n in parts.split(" ")]


def part_one(data):
    total = 0
    for (result, parts) in data:
        for ops in product([lambda a, b: a + b, lambda a, b: a * b], repeat=len(parts) - 1):
            ops = list(ops)
            if reduce(lambda a, b: ops.pop(0)(a, b), parts) == result:
                total += result
                break

    return total


def part_two(data):
    total = 0
    for (result, parts) in data:
        for ops in product([lambda a, b: a + b, lambda a, b: a * b, lambda a, b: int(str(a) + str(b))],
                           repeat=len(parts) - 1):
            ops = list(ops)
            if reduce(lambda a, b: ops.pop(0)(a, b), parts) == result:
                total += result
                break

    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=to_eq)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
