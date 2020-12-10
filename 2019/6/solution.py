from collections import defaultdict, deque

def part1(inputs):
    objects = {}
    for line in inputs:
        stationary, orbiting = line.split(")")
        objects[orbiting] = stationary

    counts = defaultdict(int)
    for orbiting, stationary in objects.items():
        get_count(objects, counts, orbiting)
    return sum(counts.values())


def get_count(objects, counts, object):
    if object not in counts and object != "COM":
        counts[object] = 1 + get_count(objects, counts, objects[object])

    return counts[object]


class Node(object):

    def __init__(self, n, edges=None):
        self.n = n
        self.edges = edges or []

    def add_edge(self, n):
        self.edges.append(n)


def part2(inputs):
    graph = defaultdict(list)
    for line in inputs:
        stationary, orbiting = line.split(")")
        graph[orbiting].append(stationary)
        graph[stationary].append(orbiting)
        #stationary_node = Node(stationary)
        #orbiting_node = Node(orbiting)
        #stationary_node.add_edge(orbiting_node)
        #orbiting_node.add_edge(stationary_node)
        #graph[stationary] = stationary_node
        #graph[orbiting] = orbiting_node

    start = "YOU"
    target = "SAN"
    return len(find_shortest_path(dict(graph), start, target)) -3 #remove "YOU" and "SAN"


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def search(visited, queue, start, target):
    visited.append(start)
    queue.append(start)

    while queue:
        node = queue.pop(0)
        if node.n == target:
            print("found the target....now what?")
            return
        for edge in node.edges:
            visited.append(edge)
            queue.append(edge)


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(part1(inputs))
    print(part2(inputs))

