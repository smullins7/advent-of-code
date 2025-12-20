import sys
from itertools import combinations

from utils.inputs import get_inputs
from utils.numbers import bin_to_int, int_to_bin


def convert_target(s):
    return bin_to_int(''.join(['1' if c == '#' else '0' for c in s]))


def convert_buttons(l, size):
    buttons = []
    for s in l:
        button = ['0'] * size
        for b in s[1:-1].split(','):
            button[int(b)] = '1'
        buttons.append(bin_to_int(''.join(button)))
    return buttons


def tryit(target, buttons):
    for button_group in buttons:
        result = 0
        for button in button_group:
            result = result ^ button
        if result == target:
            return True

    return False


def part_one(data):
    total = 0
    for line in data:
        parts = line.split(' ')
        raw_target = parts[0][1:-1]
        target = convert_target(raw_target)
        buttons = convert_buttons(parts[1:-1], len(raw_target))
        count = 1
        while True:
            if tryit(target, combinations(buttons, count)):
                total += count
                break
            count += 1

    return total


def did_we_pass_it(value, joltage):
    for v, target in zip(value, joltage):
        if v > target:
            return True
    return False


def add_em(existing, button):
    return list(map(lambda left, right: left + right, existing, button))


def part_two(data):
    for line in data:
        parts = line.split(' ')
        width = len(parts[0][1:-1])
        buttons = [[int(inner) for inner in int_to_bin(i, width)] for i in convert_buttons(parts[1:-1], width)]
        joltage = [int(j) for j in parts[-1][1:-1].split(',')]
        print(buttons, joltage)
        # todo some kind of breadth first search, like put all buttons in a queue and then see if the total of that branch equals the joltage, if so count length, if impossible, prune, else add all buttons to end of queue
        # make a copy since we'll but mutating as we go
        queue = [(list(button), 1) for button in buttons]
        total = 0
        printed = set()
        while queue:
            current, counter = queue.pop(0)
            if counter not in printed:
                print(f"{counter} presses has {len(queue)} options to try...")
                printed.add(counter)
            for button in buttons:
                new_values = add_em(current, button)
                if new_values == joltage:
                    print(f"found it but don't know how many button presses yet: {new_values}, {counter + 1}")
                    total += counter + 1
                    break
                elif did_we_pass_it(new_values, joltage):
                    # print(f"this path didn't pan out, pruning after {counter + 1} presses")
                    continue
                queue.append((new_values, counter + 1))

    return 0


def dijkstra_every_time(buttons, start_button, joltage):
    unvisited_nodes = [(start_button, 1)]
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[(start_button, 1)] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        node, direction, steps = current_min_node
        for neighbor in grid.find_neighbors(node):
            # skip if neighbor is in same direction and steps is already at 3
            next_direction = get_direction(node, neighbor)
            if not is_legal_dir(direction, next_direction) or neighbor == start_node or (
                    next_direction == direction and steps == 3):
                continue
            steps_in_direction = 1 if next_direction != direction else steps + 1
            tentative_value = shortest_path[current_min_node] + neighbor.value
            _next = (neighbor, next_direction, steps_in_direction)
            if tentative_value < shortest_path[_next]:
                shortest_path[_next] = tentative_value
                # We also update the best path to the current node
                previous_nodes[_next] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
        if len(unvisited_nodes) % 1000 == 0:
            print(len(unvisited_nodes))

    return previous_nodes, shortest_path


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        # print(f"{f.__name__}:\n\t{f(real_data)}")
