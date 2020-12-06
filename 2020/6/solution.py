
from collections import defaultdict

def part1(inputs):
    total = 0
    for group in groups:
        answers = set()
        for passenger in group:
            for answer in passenger:
                answers.add(answer)
        total += len(answers)

    return total

def part2(inputs):
    total = 0
    for group in groups:
        answers = defaultdict(int)
        for passenger in group:
            for answer in passenger:
                answers[answer] += 1
        for k, v in answers.items():
            if v == len(group):
                total += 1

    return total


if __name__ == "__main__":
    groups = [[]]
    for line in open("./input.txt"):
        line = line.strip()
        if line:
            groups[-1].append(line)
        else:
            groups.append([])
    print(part1(groups))
    print(part2(groups))

