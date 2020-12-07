
from collections import defaultdict
import re

OUTER_BAG = re.compile("^(.*(?!bags contain)) bags contain.*$")
TARGET = ("shiny", "gold")


class Node(object):

    def __init__(self, bag, count=0, children=None):
        self.bag = bag
        self.count = int(count)
        self.children = children or list()

    def add_child(self, n):
        self.children.append(n)


def to_node(bag, count):
    return Node(bag, count=count)


def part1(rules, answers):
    more = False
    for outer_bag, r in rules.items():
        for (style, color) in r.keys():
            if ((style, color) == TARGET or (style, color) in answers) and outer_bag not in answers:
                answers.add(outer_bag)
                more = True
    if more:
        return part1(rules, answers)
    return answers


def part2(rules):
    tree = Node(TARGET, count=1)
    add_bags(TARGET, rules, tree)
    return count_bags(tree, 0) - 1


def add_bags(bag, rules, node):
    for inner_bag, count in rules[bag].items():
        child_node = to_node(inner_bag, count)
        node.add_child(child_node)
        if inner_bag in rules:
            add_bags(inner_bag, rules, child_node)


def count_bags(node, total):
    total += node.count + (node.count * sum([count_bags(x, total) for x in node.children]))
    return total


def traverse(flat_rules, target, seen, total):
    bag_rules = flat_rules[target]
    for bag, count in bag_rules.items():
        if bag in seen:
            continue
        total += count
        seen.add(bag)
        traverse(flat_rules, bag, seen, total)
    return total


def flatten_rules(rules):
    flattened = defaultdict(dict)
    for bag, r in rules.items():
        for (style, color), count in r.items():
            flattened[bag][(style, color)] = int(count)
    return flattened


def parse(lines):
    bags = defaultdict(dict)
    for line in lines:
        m = OUTER_BAG.match(line)
        for inner in line.split("contain ")[1].split(", "):
            if inner == "no other bags.":
                bags[m.groups(1)] = {}
                continue
            n, style, color, _ = inner.split(" ")
            bags[tuple(m.groups(1)[0].split(" "))][(style, color)] = n

    return bags


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    bags = parse(inputs)
    answers = set()
    print(len(part1(bags, answers)))
    print(part2(bags))

