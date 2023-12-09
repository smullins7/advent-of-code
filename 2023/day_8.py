import re
from itertools import cycle
from math import lcm
from utils.graphs import TwoDirectionNode
from utils.inputs import get_inputs

PAT = re.compile(r"^(?P<node>.*) = \((?P<left>.*), (?P<right>.*)\)$")


def part_one(data):
    lr = cycle(data[0])
    graph = {}
    for line in data[2:]:
        m = PAT.match(line)
        node = TwoDirectionNode(m.group("node"), m.group("left"), m.group("right"))
        graph[node.value] = node

    current, end = "AAA", "ZZZ"
    steps = 0
    for direction in lr:
        if current == end:
            return steps
        current = graph[current].go(direction)
        steps += 1


def try_one(graph, position, directions):
    steps = 0
    for direction in cycle(directions):
        if position.endswith("Z"):
            return steps
        position = graph[position].go(direction)
        steps += 1


def part_two(data):
    graph = {}
    for line in data[2:]:
        m = PAT.match(line)
        node = TwoDirectionNode(m.group("node"), m.group("left"), m.group("right"))
        graph[node.value] = node

    currents = [k for k in graph.keys() if k.endswith("A")]
    steps = []
    for current in currents:
        steps.append(try_one(graph, current, data[0]))

    return lcm(*steps)


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_two,):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
