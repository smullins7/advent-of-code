from dataclasses import dataclass
from typing import Tuple

from utils.inputs import get_inputs


@dataclass
class Pipe:
    symbol: str
    connectors: str
    position: Tuple[int, int]

    def outsiders(self, connector):
        for move_func in THE_MAP.get((self.symbol, connector), []):
            yield move_func(*self.position)

    def move(self, connector):
        return moves[connector](*self.position)

    def moves(self):
        for connector in self.connectors:
            yield moves[connector](*self.position)

    def exit(self, incoming_connector):
        for connector in self.connectors:
            if connector != incoming_connector:
                return connector

moves = {
    "N": lambda x, y: (x, y + 1),
    "S": lambda x, y: (x, y - 1),
    "E": lambda x, y: (x + 1, y),
    "W": lambda x, y: (x - 1, y),
}

# entering from direction -> outside neighbor
THE_MAP = {
    ("|", "N"): (moves["E"], ),
    ("|", "S"): (moves["W"], ),

    ("-", "W"): (moves["N"], ),
    ("-", "E"): (moves["S"], ),

    ("L", "E"): (moves["W"], moves["S"]),

    ("J", "N"): (moves["E"], moves["S"]),

    ("7", "W"): (moves["E"], moves["N"]),

    ("F", "S"): (moves["W"], moves["N"]),
}

connectors = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
    ".": "",
}

def move(graph, coordinates, previous=None):
    pipe = graph[coordinates]
    for move_to in pipe.moves():
        if move_to in graph and can_move(graph, coordinates, move_to) and move_to != previous:
            return move_to
    return None


def can_move(graph, a, b):
    return a in set(graph[b].moves()) and b in set(graph[a].moves())

def to_something(data):
    d = {}
    s = None
    for y, line in enumerate(reversed(data)):
        for x, c in enumerate(line):
            #if c == ".": continue
            if c in connectors:
                d[(x, y)] = Pipe(c, connectors[c], (x, y))
            else:
                s = x, y
    return d, s

def loop(graph, position):
    seen = set()
    previous = None
    while True:
        seen.add(position)
        new_position = move(graph, position, previous)
        if not new_position:
            return False
        if new_position in seen:
            return seen
        previous = position
        position = new_position


def part_one(data):
    graph, S = to_something(data)
    for possible_s in connectors.keys():
        possible_graph = graph.copy()
        possible_graph[S] = connectors[possible_s]

        main_loop = loop(possible_graph, S)
        if main_loop:
            return int(len(main_loop) / 2)
    return 0


def outsiders(graph, main_loop, start_at):
    """
    go around main loop, if valid outside neighbor add it to set
    """
    directions = {"N": "S", "S": "N", "E": "W", "W": "E"}
    outside = set()

    current = start_at
    direction = "E"
    while True:
        # process current
        pipe = graph[current]
        for neighbor in pipe.outsiders(direction):
            if neighbor in graph and not neighbor in main_loop:
                outside.add(neighbor)

        # advance current
        direction = pipe.exit(direction)
        current = pipe.move(direction)

        if current == start_at:
            # at this point we've found all the adjacent outside tiles, but they have neighbors too...
            keep_going = True
            while keep_going:
                keep_going = False
                for pos in outside.copy():
                    for move_func in moves.values():
                        possible_outside_neighbor = move_func(*pos)
                        if possible_outside_neighbor in graph and possible_outside_neighbor not in main_loop and possible_outside_neighbor not in outside:
                            outside.add(possible_outside_neighbor)
                            keep_going = True

            return outside

        direction = directions[direction]


def part_two(data):
    graph, S = to_something(data)
    for possible_s in connectors.keys():
        possible_graph = graph.copy()
        possible_graph[S] = Pipe(possible_s, connectors[possible_s], S)

        main_loop = loop(possible_graph, S)
        if main_loop:
            break

    # find the south-west corner piece to start with
    loop_start = None

    for pos in main_loop:
        x, y = pos
        if loop_start is None or x < loop_start[0] or (x == loop_start[0] and y < loop_start[1]):
            loop_start = pos
    print("Identified main loop and starting position at", loop_start)

    outside_tiles = outsiders(possible_graph, main_loop, loop_start)
    return len(possible_graph) - len(main_loop) - len(outside_tiles)

if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_two, ):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")

