from collections import deque, defaultdict

from utils.inputs import get_inputs
from utils.numbers import digits


def parse(line):
    return deque([int(s) for s in line.split(" ")])


def blink(stones: deque[int]):
    ops = []
    for i, stone in enumerate(stones):
        if stone == 0:
            ops.append(("r", i, 1))
        elif digits(stone) % 2 == 0:
            mid = int(digits(stone) / 2)
            as_str = str(stone)
            left, right = as_str[:mid], as_str[mid:]
            ops.append(("r", i, int(left)))
            ops.append(("i", i + 1, int(right)))
        else:
            ops.append(("r", i, stone * 2024))

    for op, index, value in reversed(ops):
        if op == "r":
            stones[index] = value
        elif op == "i":
            stones.insert(index, value)

def part_one(data):
    stones = parse(data)
    for _ in range(25):
        blink(stones)
    return len(stones)


def part_two(data):
    stones = defaultdict(int)
    for n in data.split(" "):
        stones[int(n)] += 1

    for _ in range(75):
        processed = defaultdict(int)
        for n, count in stones.items():
            if n == 0:
                processed[1] += count
            elif digits(n) % 2 == 0:
                mid = int(digits(n) / 2)
                as_str = str(n)
                left, right = as_str[:mid], as_str[mid:]
                processed[int(left)] += count
                processed[int(right)] += count
            else:
                processed[n * 2024] += count
        stones = processed

    return sum(stones.values())

if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")