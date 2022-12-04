from lib_inputs import get_input

"""
A Y
B X
C Z

A/X = rock = 1
B/Y = paper = 2
C/Z = scissors = 3

B/Y > A/X
C/Z > B/Y
A/X > C/Z

2 > 1
3 > 2
1 > 3
"""
def convert(c):
    if c in ("A", "X"):
        return 1
    if c in ("B", "Y"):
        return 2
    return 3

def part_one(data):
    total = 0
    for line in data:
        first, second = line.split(" ")
        f = convert(first)
        s = convert(second)
        total += s
        if f == s:
            total += 3
        if (f == 1 and s == 2) or (f == 2 and s == 3) or (f == 3 and s == 1):
            total += 6

    return total


def choose(c, outcome):
    if outcome == "X":
        # lose
        if c == "A":
            return 3
        elif c == "B":
            return 1
        return 2
    if outcome == "Y":
        # draw
        if c == "A":
            return 1
        if c == "B":
            return 2
        return 3
    if c == "A":
        return 2
    elif c == "B":
        return 3
    return 1

def part_two(data):
    total = 0
    for line in data:
        first, second = line.split(" ")
        total += choose(first, second)
        if second == "Y":
            total += 3
        elif second == "Z":
            total += 6

    return total


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=False)
        print(f"{f.__name__}:\n\t{f(data)}")

