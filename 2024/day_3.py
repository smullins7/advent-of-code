import math
import re
from itertools import chain, product

from utils.inputs import get_inputs


mul_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
dont_re = re.compile(r"(don't\(\))")
do_re =  re.compile(r"(do\(\))")

def part_one(data):
    return sum(map(lambda s: int(s[0]) * int(s[1]),re.findall(mul_re, "".join(data))))


def part_two(data):
    data = "".join(data)
    donts = re.finditer(dont_re, data)
    dos = re.finditer(do_re, data)
    mults = re.finditer(mul_re, data)
    sums = 0
    enabled = True
    for match in sorted(list(chain(mults, dos, donts)), key=lambda m: m.span()[0]):
        if match.group() == "don't()":
            enabled = False
        elif match.group() == "do()":
            enabled = True
        elif enabled:
            sums += math.prod([int(n) for n in match.groups()])

    return sums


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")