import re

ZEROS = re.compile("[FL]")
ONES = re.compile("[BR]")


def part1(inputs):
    return [int(ONES.sub("1", ZEROS.sub("0", assignment)), 2) for assignment in inputs]


def part2(inputs):
    prev = None
    for seat_id in sorted(part1(inputs)):
        if not prev:
            prev = seat_id
            continue
        if seat_id - 1 != prev:
            return seat_id - 1
        prev = seat_id


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(max(part1(inputs)))
    print(part2(inputs))
