from utils.inputs import get_inputs


def is_invalid(n):
    s = str(n)
    if len(s) % 2 != 0:
        return False
    mid = int(len(s) / 2)
    return s[0:mid] == s[mid:]


def part_one(data):
    total = 0
    for line in data.split(','):
        first, last = [int(n) for n in line.split('-')]
        for n in range(first, last + 1):
            if is_invalid(n):
                total += n
    return total


def is_invalid2(n):
    s = str(n)
    return s in (s + s)[1:-1]


def part_two(data):
    total = 0
    for line in data.split(','):
        first, last = [int(n) for n in line.split('-')]
        for n in range(first, last + 1):
            if is_invalid2(n):
                total += n
    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
