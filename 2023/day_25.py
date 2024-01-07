from collections import defaultdict

import matplotlib.pyplot as plt
import networkx

from utils.inputs import get_inputs


# just visualize the graph and then it's obvious which three connections to cut
def draw(data):
    g = defaultdict(set)
    for line in data:
        left, right = line.split(": ")
        for r in right.split(" "):
            g[left].add(r)
            g[r].add(left)

    edges = []
    for k, others in g.items():
        for o in others:
            edges.append((k, o))

    G = networkx.Graph()
    G.add_edges_from(edges)
    networkx.draw_networkx(G)
    plt.show()

    return 0


# hard coded from visualizing puzzle input
TO_CUT = {
    "mnf": "hrs",
    "hrs": "mnf",
    "kpc": "nnl",
    "nnl": "kpc",
    "rkh": "sph",
    "sph": "rkh"
}


def count(g: defaultdict, node: str):
    seen = set()
    todo = [node]
    while todo:
        thing = todo.pop(0)
        if thing in seen:
            continue
        seen.add(thing)
        for other in g[thing]:
            todo.append(other)
    return len(seen)


def part_one(data):
    g = defaultdict(set)
    for line in data:
        left, right = line.split(": ")
        for r in right.split(" "):
            g[left].add(r)
            g[r].add(left)

    for k in g:
        if k in TO_CUT:
            other = TO_CUT[k]
            g[k].remove(other)

    first = count(g, next(iter(g)))
    return first, len(g), (len(g) - first) * first


def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
