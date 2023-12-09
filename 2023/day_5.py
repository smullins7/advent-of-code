import sys

from utils.inputs import get_inputs


def map_func(triplets, reverse=False):
    def f(n):
        for dest, src, count in triplets:
            if reverse:
                src, dest = dest, src
            if src <= n < (src + count):
                return dest + n - src
        return n

    return f


def to_mappings(data, reverse=False):
    seeds = [int(n) for n in data[0].split(": ")[1].split(" ")]
    mappings = []
    current = []
    for line in data[2:]:
        if not line:
            mappings.append(map_func(current, reverse))
            current = []
        elif not line.endswith("map:"):
            current.append([int(n) for n in line.split(" ")])

    if current:
        mappings.append(map_func(current, reverse))
    return seeds, mappings if not reverse else list(reversed(mappings))


def part_one(data):
    seeds, mappings = to_mappings(data)
    min_location = sys.maxsize
    for seed in seeds:
        for f in mappings:
            seed = f(seed)
        min_location = min(min_location, seed)
    return min_location


def seed_check_func(seeds):
    def f(seed):
        for i in range(0, len(seeds), 2):
            if seeds[i] <= seed < seeds[i] + seeds[i + 1]:
                return True
        return False

    return f


def print_initials(data):
    seeds, mappings = to_mappings(data)
    for i in range(0, len(seeds), 2):
        seed = seeds[i]
        for f in mappings:
            seed = f(seed)
        print(seed)


def parse_ranges(data):
    raw_values = [int(n) for n in data[0].split(": ")[1].split(" ")]
    seed_ranges = []
    for i in range(0, len(raw_values), 2):
        seed_ranges.append((raw_values[i], raw_values[i + 1]))
    seed_ranges = sorted(seed_ranges, key=lambda n: n[0])

    # is_seed = lambda n: any([raw_values[i] <= n < raw_values[i] + raw_values[i + 1] for i in
    #                         range(0, len(raw_values), 2)])
    mappings = []
    current = []
    for line in data[2:]:
        if not line:
            mappings.append(current)
            current = []
        elif not line.endswith("map:"):
            current.append([int(n) for n in line.split(" ")])

    if current:
        mappings.append(current)
    return seed_ranges, list(reversed(mappings))


def find_best_starting_seed(data):
    seed_ranges, map_ranges = parse_ranges(data)
    _, next_start, next_range = min(map_ranges[0], key=lambda n: n[0])
    for triplets in map_ranges[1:]:
        for src, dest, dest_range in triplets:
            if next_start < src <= next_start + next_range:
                break
        next_start, next_range = dest, dest_range

    print("seed range:", next_start, next_range)
    for seed_start, seed_count in seed_ranges:
        if seed_start <= next_start < seed_start + seed_count:
            print(seed_start, seed_count)
            return next_start
        if next_start <= seed_start < next_start + next_range:
            print(seed_start, seed_count)
            return seed_start


def part_two(data):
    seed = find_best_starting_seed(data)
    print(seed)
    _, mappings = to_mappings(data)
    for f in mappings:
        seed = f(seed)
    return seed


def part_two_slow(data):
    print_initials(data)  # min printed is 463 381 925 (~400M)
    seeds, mappings = to_mappings(data, reverse=True)
    seed_func = seed_check_func(seeds)
    value = 0
    while True:
        temp = value
        for f in mappings:
            temp = f(temp)
        # now we're back to a seed, see if it's viable
        if seed_func(temp):
            return value
        value += 1
        if value % 100000 == 0:
            print(value)


def part_two_hack(data):
    starting_location = 49632084  # from input file just outside lowest humidity mapping to location
    seeds, mappings = to_mappings(data, reverse=True)
    seed_func = seed_check_func(seeds)
    value = starting_location
    while True:
        temp = value
        for f in mappings:
            temp = f(temp)
        # now we're back to a seed, see if it's viable
        if seed_func(temp):
            return value
        value += 1
        if value % 100000 == 0:
            print(value)


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two_hack):
        #print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
        # 1121869540 too high
        # 1647100058
        # 1647100058
        # 1647100058
        # 79874951
