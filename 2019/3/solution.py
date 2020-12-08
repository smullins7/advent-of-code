from collections import defaultdict


def generate_points(position, move):
    if move[0] == "L":
        return [(position[0] - x, position[1]) for x in range(1, int(move[1:]) + 1)]
    elif move[0] == "R":
        return [(position[0] + x, position[1]) for x in range(1, int(move[1:]) + 1)]
    elif move[0] == "U":
        return [(position[0], position[1] + y) for y in range(1, int(move[1:]) + 1)]
    else:
        return [(position[0], position[1] - y) for y in range(1, int(move[1:]) + 1)]


def part1(inputs):
    positions = defaultdict(set)
    for wire_id, wire in enumerate(inputs):
        current_position = (0, 0)
        for move in wire.split(","):
            points = generate_points(current_position, move)
            for point in points:
                positions[point].add(wire_id)
            current_position = points[-1]

    min_distance = 0
    for point, s in positions.items():
        if len(s) > 1:
            distance = sum([abs(n) for n in point])
            if not min_distance or distance < min_distance:
                min_distance = distance
    return min_distance


def part2(inputs):
    positions = defaultdict(set)
    for wire_id, wire in enumerate(inputs):
        current_position = (0, 0)
        steps = 0
        for move in wire.split(","):
            points = generate_points(current_position, move)
            for point in points:
                steps += 1
                positions[point].add((wire_id, steps))
            current_position = points[-1]

    min_distance = 0
    for point, s in positions.items():
        by_wire = {}
        for wire_id, steps in s:
            if wire_id not in by_wire or by_wire[wire_id] > steps:
                by_wire[wire_id] = steps
        if len(by_wire) > 1:
            distance = sum(by_wire.values())
            if not min_distance or distance < min_distance:
                min_distance = distance

    return min_distance


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(part1(inputs))
    print(part2(inputs))
