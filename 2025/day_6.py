import math
from collections import defaultdict
from functools import reduce

from utils.inputs import get_inputs
from utils.operators import OPS


def mathit(l):
    nums = [int(n) for n in l[:-1]]
    return sum(nums) if l[-1] == '+' else math.prod(nums)


def part_one(data, _):
    matrix = []
    for line in data:
        matrix.append([item for item in line.split(' ') if item != ''])

    total = 0
    for i in range(len(matrix[0])):
        total += mathit([inner[i] for inner in matrix])
    return total


def part_two(data, m):
    nummies = defaultdict(list)
    for line in data[:-1]:
        for i, c in enumerate(line):
            nummies[i].append(c.strip())

    total = 0
    count = 0
    for op in [OPS[c] for line in data[-1] for c in line.split(' ') if c]:
        nums_for_this_op = []
        while True:
            as_str = "".join(nummies[count])
            count += 1
            if not as_str:
                # reached the end of numbers for this op
                total += reduce(op, nums_for_this_op)
                break
            else:
                nums_for_this_op.append(int(as_str))
    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data, 3)}")
        print(f"{f.__name__}:\n\t{f(real_data, 4)}")
