from lib_inputs import get_input

import string


def to_priority(dupped):
    if dupped.islower():
        return string.ascii_lowercase.index(dupped) + 1
    return string.ascii_uppercase.index(dupped) + 27


def part_one(data):
    total = 0
    for line in data:
        split = int(len(line) / 2)
        total += to_priority(set(line[:split]).intersection(line[split:]).pop())
    return total


def part_two(data):
    groups = []
    i = 0
    temp = []
    for line in data:
        if i < 3:
            temp.append(line)
            i += 1
        else:
            groups.append(temp)
            temp = [line]
            i = 1
    groups.append(temp)
    total = 0
    for group in groups:
        total += to_priority((set(group[0]).intersection(set(group[1]))).intersection(set(group[2])).pop())

    return total


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
