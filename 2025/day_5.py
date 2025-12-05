from utils.inputs import get_grouped_inputs


def parse_ranges(ranges):
    l = []
    for r in ranges:
        lower, upper = r.split('-')
        l.append((int(lower), int(upper)))
    return l


def part_one(data):
    ranges, ingredients = data
    checks = parse_ranges(ranges)
    total = 0
    for s in ingredients:
        for (lower, upper) in checks:
            if lower <= int(s) <= upper:
                total += 1
                break

    return total


def part_two(data):
    ranges, _ = data
    unordered = parse_ranges(ranges)
    ordered = sorted(unordered, key=lambda item: item[0])

    first_lower, first_upper = ordered[0]
    total = first_upper - first_lower + 1
    prev_upper = first_upper
    for lower, upper in ordered[1:]:
        if lower > prev_upper:
            total += upper - lower + 1
        elif lower == prev_upper:
            total += (upper - lower)
        elif lower < prev_upper < upper:
            total += upper - prev_upper
        else:
            # upper < prev_upper
            continue

        prev_upper = upper
    return total


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
