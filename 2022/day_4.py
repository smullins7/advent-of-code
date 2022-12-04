from lib_inputs import get_input


def part_one(data):
    total = 0
    for line in data:
        first, second = line.split(",")
        f1, f2 = first.split("-")
        s1, s2 = second.split("-")
        set_f = set(range(int(f1), int(f2)+1))
        set_s = set(range(int(s1), int(s2) + 1))
        if set_f.issubset(set_s) or set_f.issuperset(set_s):
            total += 1
    return total


def part_two(data):
    total = 0
    for line in data:
        first, second = line.split(",")
        f1, f2 = first.split("-")
        s1, s2 = second.split("-")
        set_f = set(range(int(f1), int(f2) + 1))
        set_s = set(range(int(s1), int(s2) + 1))
        if set_f.intersection(set_s):
            total += 1
    return total


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")

