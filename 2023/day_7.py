from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from utils.inputs import get_input

LABELS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def by_count(value):
    counts = defaultdict(int)
    for v in value:
        counts[v] += 1
    return counts


def determine_type(counts):
    if len(counts) == 1:
        return 6  # five of a kind
    if len(counts) == 2:
        if list(counts.values())[0] in (1, 4):
            return 5  # four of a kind
        return 4  # full house
    if len(counts) == 3:
        for count in counts.values():
            if count == 2:
                return 2  # two pair
        return 3  # three of a kind
    if len(counts) == 4:
        return 1  # one pair
    return 0  # high card


def determine_type_with_jokers(counts, previous_type):
    if 9 not in counts or counts[9] == 5:  # no jokers or all jokers (stays 5 of a kind)
        return previous_type
    if counts[9] == 1:
        if previous_type == 0:
            return 1  # high card -> one pair
        if previous_type == 1:
            return 3  # one pair -> three of a kind
        if previous_type == 2:
            return 4  # two pair -> full house
        if previous_type == 3:
            return 5  # three of a kind -> four of a kind
        if previous_type == 5:
            return 6  # four of a kind -> five of a kind
    if counts[9] == 2:
        if previous_type == 1:
            return 3  # one pair -> three of a kind
        if previous_type == 2:
            return 5  # two pair -> four of a kind
        if previous_type == 4:
            return 6  # full house -> five of a kind
    if counts[9] == 3:
        if previous_type == 3:
            return 5  # three of a kind -> four of a kind
        if previous_type == 4:
            return 6  # full house -> five of a kind
    if counts[9] == 4:
        return 6  # four of a kind -> five of a kind


@dataclass
class Hand:
    original: List
    counts_by_value: Dict
    bid: int
    type: int
    jokers: bool = False

    @staticmethod
    def of(line):
        cards, bid = line.split(" ")
        nums = []
        for card in cards:
            nums.append(LABELS.index(card))
        counts = by_count(nums)
        return Hand(nums, counts, int(bid), determine_type(counts))

    def is_higher_rank(self, other):
        if self.type < other.type:
            return False
        if self.type > other.type:
            return True
        for a, b in zip(self.original, other.original):
            if self.jokers:
                if a == 9:  # J
                    a = -1
                if b == 9:  # J
                    b = -1
            if a == b:
                continue
            return a > b

    def __lt__(self, other):
        return other.is_higher_rank(self)

    def __gt__(self, other):
        return self.is_higher_rank(other)


def part_one(data):
    return sum([(i + 1) * c.bid for i, c in enumerate(sorted(data))])


def part_two(data):
    for hand in data:
        hand.jokers = True
        hand.type = determine_type_with_jokers(hand.counts_by_value, hand.type)
    return sum([(i + 1) * c.bid for i, c in enumerate(sorted(data))])


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=Hand.of)
        print(f"{f.__name__}:\n\t{f(data)}")
