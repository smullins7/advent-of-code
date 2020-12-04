dest_offset = 3


def getop(l, i):
    if l[i] not in [1, 2]:
        return None, None

    op, a, b = l[i:i + dest_offset]
    return l[a] + l[b] if op == 1 else l[a] * l[b], l[i + dest_offset]


def part1(inputs):
    c = 0
    parts = list(inputs)
    new_val, dest = getop(parts, c)
    while new_val is not None:
        parts[dest] = new_val
        c += 4
        new_val, dest = getop(parts, c)
    return parts


def part2(inputs):
    for noun in range(0, 100):
        for verb in range(0, 100):
            l = list(inputs)
            l[1] = noun
            l[2] = verb
            possible = part1(l)
            if possible[0] == 19690720:
                return 100 * noun + verb


if __name__ == "__main__":
    inputs = [int(x) for x in open('./input.txt', 'r').read().split(",")]
    print(part1(inputs)[0])
    print(part2(inputs))
