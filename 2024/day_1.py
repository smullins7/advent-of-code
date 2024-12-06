from collections import defaultdict

from utils.inputs import get_inputs, to_numbers


def part_one(data):
    first, second = list(zip(*data))
    return sum(map(lambda n: abs(n[0] - n[1]), zip(sorted(first), sorted(second))))


def part_two(data):
    first, second = list(zip(*data))
    second_counts = defaultdict(int)
    for n in second:
        second_counts[n] += 1
    return sum(map(lambda n: n * second_counts[n], first))


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=to_numbers)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")