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
        return 6 # five of a kind
    if len(counts) == 2:
        if list(counts.values())[0] in (1, 4):
            return 5 # four of a kind
        return 4 # full house
    if len(counts) == 3:
        for count in counts.values():
            if count == 2:
                return 2 # two pair
        return 3 # three of a kind
    if len(counts) == 4:
        return 1 # one pair
    return 0 # high card

@dataclass
class Hand:
    original: List
    counts_by_value: Dict
    bid: int
    type: int

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
            if a == b:
                continue
            return a > b

    def __lt__(self, other):
        return other.is_higher_rank(self)

    def __gt__(self, other):
        return self.is_higher_rank(other)

def part_one(data):
    return sum([(i+1) * c.bid for i, c in enumerate(sorted(data))])


def part_two(data):
    return 0


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=Hand.of)
        print(f"{f.__name__}:\n\t{f(data)}")
