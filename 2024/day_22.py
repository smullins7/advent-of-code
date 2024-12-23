from collections import defaultdict

from utils.inputs import get_inputs


def evolve(incoming: int) -> int:
    step_one = (incoming ^ (incoming * 64)) % 16777216
    step_two = (int(step_one / 32) ^ step_one) % 16777216
    return ((step_two * 2048) ^ step_two) % 16777216


def evolve_to(n: int, times: int) -> int:
    for _ in range(times):
        n = evolve(n)
    return n


def part_one(data):
    total = 0
    for n in data:
        total += evolve_to(n, 2000)
    return total


def evolve_sequence(n: int, times: int) -> list[tuple[int,int]]:
    results = [(n % 10, None)]
    for _ in range(times):
        n = evolve(n)
        ones = n % 10
        results.append((ones, ones - results[-1][0]))
    return results


def process_sequence(index: int, sequence: list[tuple[int,int]], scores: dict):
    for i in range(1, len(sequence) - 3):
        key = (
            sequence[i][1],
            sequence[i + 1][1],
            sequence[i + 2][1],
            sequence[i + 3][1],
        )
        if index in scores[key]:
            continue
        scores[key][index] = sequence[i + 3][0]

def part_two(data):
    scores = defaultdict(dict)
    for i, n in enumerate(data):
        sequence = evolve_sequence(n, 2000)
        process_sequence(i, sequence, scores)

    best = 0
    for d in scores.values():
        best = max(best, sum(d.values()))
    return best


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=int)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
        # 1923 too low