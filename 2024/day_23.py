from collections import defaultdict
from itertools import combinations

from utils.inputs import get_inputs

def find_triplets(d: dict[str,set[str]]) -> set[tuple]:
    threes = set()
    for k, v in d.items():
        for item in v:
            for third in d[item].intersection(v):
                threes.add(tuple(sorted([k, item, third])))
    return threes

def part_one(data):
    d = defaultdict(set)
    for line in data:
        left, right = line.split("-")
        d[left].add(right)
        d[right].add(left)

    threes = find_triplets(d)


    return sum([1 for triplet in threes if any([value.startswith("t") for value in triplet])])


def part_two(data):
    d = defaultdict(set)
    for line in data:
        left, right = line.split("-")
        d[left].add(right)
        d[right].add(left)

    groups = []
    for k, others in d.items():
        for other in others:
            pair = {k, other}
            if pair not in groups:
                groups.append(pair)

    for k, others in d.items():
        for group in groups:
            if len(others & group) == len(group):
                group.add(k)


    mlen = max(len(group) for group in groups)
    print('\n'.join(set(','.join(sorted(group)) for group in groups if len(group) == mlen)))


# too slow never finished after k=5
def k_cliques(data):
    pairs = set()
    for line in data:
        left, right = line.split("-")
        pairs.add((left, right))

    cliques = [set(line.split("-")) for line in data]
    k = 2

    while cliques:
        next_set = set()
        for u, v in combinations(cliques, 2):
            w = u ^ v
            if len(w) == 2 and tuple(w) in pairs:
                next_set.add(tuple(u | w))

        if not next_set:
            return k, cliques
        # remove duplicates
        cliques = list(map(set, next_set))
        print("Found", len(cliques), "cliques of size", k)
        k += 1


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")