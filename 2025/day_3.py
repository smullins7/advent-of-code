from utils.inputs import get_inputs


def part_one(data):
    total = 0
    for line in data:
        ints = [int(n) for n in line]
        first = max(ints[:-1])
        start = ints.index(first)

        total += int(f'{first}{max(ints[start + 1:])}')
    return total


def largest_within(seq, digits, start):
    n = max(seq[start:-digits] if digits else seq[start:])
    return n, seq.index(n, start)


def part_two(data):
    total = 0
    for line in data:
        ints = [int(n) for n in line]
        index = -1
        numbers = []
        for i in reversed(range(12)):
            num, index = largest_within(ints, i, index + 1)
            numbers.append(str(num))

        total += int("".join(numbers))
    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
