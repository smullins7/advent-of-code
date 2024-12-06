from collections import defaultdict

from utils.inputs import get_grouped_inputs


def parse_rules(lines):
    rules = defaultdict(set)
    for line in lines:
        left, right = line.split("|")
        rules[left].add(right)

    return rules

def is_in_order(rules, line):
    pages = line.split(",")
    before = {pages[0]}
    for n in pages[1:]:
        if before.intersection(rules[n]):
            # we found at least one page behind us that should be ahead
            return 0
        before.add(n)
    return int(pages[int(len(pages)/2)])

def part_one(data):
    rules = parse_rules(data[0])
    total = 0
    for line in data[1]:
        total += is_in_order(rules, line)
    return total


def part_two(data):
    rules = parse_rules(data[0])
    total = 0
    for line in data[1]:
        if not is_in_order(rules, line):
            pages = line.split(",")
            corrected = []
            while pages:
                page = pages.pop(0)
                afters = rules[page]
                if not pages or set(pages).issubset(afters):
                    corrected.append(page)
                else:
                    pages.append(page)
            total += (int(corrected[int(len(corrected)/2)]))

    return total


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")