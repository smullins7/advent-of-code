from collections import defaultdict

def has_same(s):
    prev = None
    for c in s:
        if not prev:
            prev = c
            continue
        if prev == c:
            return True
        prev = c
    return False


def has_same2(s):
    prev = None
    same = defaultdict(int)
    for c in s:
        if not prev:
            prev = c
            continue
        if prev == c:
            same[c] += 1
        prev = c
    for count in same.values():
        if count == 1:
            return True
    return False


def has_increase(s):
    prev = None
    for c in s:
        i = int(c)
        if not prev:
            prev = i
            continue
        if prev > i:
            return False
        prev = i
    return True


def is_valid(i):
    s = str(i)
    return has_same(s) and has_increase(s)


def is_valid2(i):
    s = str(i)
    return has_same2(s) and has_increase(s)


def part1(lower, upper):
    return sum([is_valid(n) for n in range(int(lower), int(upper) + 1)])


def part2(lower, upper):
    return sum([is_valid2(n) for n in range(int(lower), int(upper) + 1)])


if __name__ == "__main__":
    lower, upper = [line.strip() for line in open("./input.txt")][0].split("-")
    print(part1(lower, upper))
    # not 49563 too high
    print(part2(lower, upper))
