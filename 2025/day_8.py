import math

from utils.graphs import NDimGraph
from utils.inputs import get_inputs


def distance(position_a, position_b):
    return math.sqrt(sum([(p - q) ** 2 for p, q in zip(position_a, position_b)]))


def get_circuit(circuits: list, position):
    for circuit in circuits:
        if position in circuit:
            return circuit


def make_conn(circuits, a, b):
    a_circuit, b_circuit = get_circuit(circuits, a), get_circuit(circuits, b)
    if not a_circuit and not b_circuit:
        circuits.append({a, b})
    elif a_circuit == b_circuit:
        pass
    elif a_circuit and b_circuit:
        circuits.remove(b_circuit)
        a_circuit.update(b_circuit)
    elif a_circuit:
        a_circuit.add(b)
    else:
        b_circuit.add(a)


def part_one(data, total):
    graph = NDimGraph()
    distances = {}
    for line in data:
        new_pos = tuple([int(n) for n in line.split(',')])
        for position in graph:
            distances[(position, new_pos)] = distance(position, new_pos)
        graph.add_point(*new_pos)

    sorted_distances = sorted(distances, key=lambda p: distances[p])
    circuits = []
    for _ in range(total):
        a, b = sorted_distances.pop(0)
        distances.pop((a, b))
        make_conn(circuits, a, b)

    desc = sorted(circuits, key=lambda c: len(c), reverse=True)
    return len(desc[0]) * len(desc[1]) * len(desc[2])


def part_two(data, _):
    graph = NDimGraph()
    distances = {}
    for line in data:
        new_pos = tuple([int(n) for n in line.split(',')])
        for position in graph:
            distances[(position, new_pos)] = distance(position, new_pos)
        graph.add_point(*new_pos)

    sorted_distances = sorted(distances, key=lambda p: distances[p])
    circuits = []
    while True:
        a, b = sorted_distances.pop(0)
        distances.pop((a, b))
        make_conn(circuits, a, b)

        if len(circuits) and len(circuits[0]) == len(graph):
            break
        print(len(circuits), len(distances))
    print(a, b)
    return a[0] * b[0]


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data, 10)}")
        print(f"{f.__name__}:\n\t{f(real_data, 1000)}")
