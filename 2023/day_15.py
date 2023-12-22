from collections import defaultdict
from functools import reduce

from utils.inputs import get_inputs


def hashit(s: str):
    return reduce(lambda v, c: ((v + ord(c)) * 17) % 256, s, 0)

def part_one(data):
    return sum(map(hashit, data.split(",")))


def part_two(data):
    boxes = defaultdict(list)
    lenses = dict()
    for s in data.split(","):
        if s.count("="):
            label, lens_num = s.split("=")
            box_num = hashit(label)
            labels = boxes[box_num]
            if label not in labels:
                labels.append(label)
            lenses[label] = int(lens_num)
        else:
            label = s[:-1]
            box_num = hashit(label)
            labels = boxes[box_num]
            if label in labels:
                labels.remove(label)
            lenses.pop(label, None)

    total = 0
    for label, focal in lenses.items():
        box_num = hashit(label)
        total += (1 + box_num ) * (1 + boxes[box_num].index(label)) * focal
    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")

