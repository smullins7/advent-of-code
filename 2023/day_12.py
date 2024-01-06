from typing import List

from utils.inputs import get_inputs


def parse_line(line):
    springs, sizes = line.split(" ")
    return springs, [int(n) for n in sizes.split(",")]


def is_valid(springs, sizes):
    spring_groups = [s for s in springs.split(".") if s]
    if len(spring_groups) != len(sizes):
        return False
    for spring, size in zip(spring_groups, sizes):
        if len(spring) != size:
            return False
    return True


# TODO cache
def q(n: int):
    # 2 ** n possibilities to check
    for i in range(2 ** n):
        as_binary = bin(i)[2:]  # chop off the 0b prefix
        yield as_binary.rjust(n, '.').replace("0", ".").replace("1", "#")


def convert(springs, binary_str):
    buffer, subs = [], list(binary_str)
    for c in springs:
        buffer.append(c if c != "?" else subs.pop(0))
    return "".join(buffer)


def part_one(data):
    total = 0
    for springs, sizes in data:
        print("Processing", springs, sizes)
        unknowns = springs.count("?")
        binaries = q(unknowns)
        for binary_string in binaries:
            possible = convert(springs, binary_string)
            if is_valid(possible, sizes):
                total += 1
    return total


def unfold(data):
    for springs, sizes in data:
        yield "?".join([springs] * 5), [int(n) for n in ",".join([str(s) for s in sizes] * 5).split(",")]


def replace(s: str, index: int, c: str):
    return s[:index] + c + s[index + 1:]


def groups_count(springs: str):
    return len([g for g in springs.split(".") if g])


def prune(springs: str, sizes: List[int]):
    total = sum(sizes)
    most = springs.count("?") + springs.count("#")
    least = springs.count("#")
    return most < total or least > total


def recurse(springs: str, sizes):
    wildcard = springs.find("?")
    if wildcard == -1:
        return int(is_valid(springs, sizes))
    elif prune(springs, sizes):
        return 0
    with_dot = replace(springs, wildcard, ".")
    with_hash = replace(springs, wildcard, "#")
    return recurse(with_dot, sizes) + recurse(with_hash, sizes)


def part_two(data):
    total = 0
    for springs, sizes in unfold(data):
        print("Processing", springs, sizes)
        total += recurse(springs, sizes)
        print(total)
    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=parse_line)
    for f in (part_two,):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        # print(f"{f.__name__}:\n\t{f(real_data)}")
