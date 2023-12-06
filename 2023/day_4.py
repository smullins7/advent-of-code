from collections import defaultdict

from utils.inputs import get_inputs


def parse_card(line):
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    card_field, rest = line.split(": ")
    winning, picks = rest.split(" | ")
    return int(card_field.split(" ")[-1]), [x for x in winning.strip().split(" ") if x], [x for x in
                                                                                          picks.strip().split(" ")
                                                                                          if x]


def part_one(data):
    total = 0
    for _, winning, picks in data:
        count = len(set(winning).intersection(set(picks)))
        if count:
            total += 2 ** (count - 1)
    return total


def part_two(data):
    by_card = {}
    for card_num, winning, picks in reversed(data):
        count = len(set(winning).intersection(set(picks)))
        by_card[card_num] = 1 + sum([by_card[i + 1] for i in range(card_num, card_num + count)])

    return sum(by_card.values())


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=parse_card)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
