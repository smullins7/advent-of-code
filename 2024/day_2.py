import math
from itertools import pairwise

from utils.inputs import get_inputs, to_numbers

def is_safe(report):
    sign = None
    for first, second in pairwise(report):
        diff = first - second
        if not diff or abs(diff) > 3:
            return 0
        if sign is None:
            sign = math.copysign(1, diff)
        elif sign != math.copysign(1, diff):
            return 0
    return 1

def part_one(data):
    return sum(map(is_safe, data))


def part_two(data):
    safe = 0
    for report in data:
        if is_safe(report):
            safe += 1
            continue

        # check all possible combinations of removing each level from the report
        for i, _ in enumerate(report):
            if is_safe(report[:i] + report[i+1:]):
                safe += 1
                break
    return safe

if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=to_numbers)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")