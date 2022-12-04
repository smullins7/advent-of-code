from lib_inputs import get_input


def parse_lines(data):
    cals = []
    temp = 0
    for line in data:
        if not line.strip():
            cals.append(temp)
            temp = 0
            continue
        temp += int(line.strip())
    return cals + [temp]


def part_one(data):
    return max(parse_lines(data))


def part_two(data):
    return sum(sorted(parse_lines(data), reverse=True)[:3])


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=False)
        print(f"{f.__name__}:\n\t{f(data)}")
