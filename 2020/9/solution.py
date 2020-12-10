WINDOW = 25


def combinations(l):
    s = set()
    for i in l:
        for j in l:
            if i != j:
                s.add(i+j)
    return s


def part1(inputs):
    q = []
    for n in inputs:
        if len(q) < WINDOW:
            q.append(n)
            continue
        sums = combinations(q)
        if n not in sums:
            return n
        q.pop(0)
        q.append(n)


def part2(inputs):
    invalid = part1(inputs)
    q = []
    for n in inputs:
        q.append(n)
        if len(q) > 1 and sum(q) == invalid:
            return min(q) + max(q)
        while sum(q) > invalid:
            q.pop(0)
            if len(q) > 1 and sum(q) == invalid:
                return min(q) + max(q)


if __name__ == "__main__":
    inputs = [int(line.strip()) for line in open("./input.txt")]
    print(part1(inputs))
    print(part2(inputs))

