from dataclasses import dataclass, field, fields
from typing import List, Set, Dict

from utils.inputs import get_input
import itertools

import re

"""
def part_one_abondonded(data):
    graph = {}
    for (valve, rate, tunnels) in data:
        graph[valve] = {
            "rate": int(rate),
            "tunnels": tunnels.split(", "),
        }

    pairs = list(itertools.combinations([k for k in graph.keys() if graph[k]["rate"] or k == "AA"], 2))
    paths = {}
    print("pairs", len(pairs))
    for pair in pairs:
        paths[pair] = shortest_path(graph, *pair)
        paths[tuple(reversed(pair))] = paths[pair]
    print("calculated all shortest path pairs")
    all_options = choices(graph, paths)
    #print("total", len(list(all_options)))
    #pruned = [option for option in all_options if option[0] in HIGHS]
    #print("pruned", len(pruned))
    max_p = 0
    checked = 0
    for option in all_options:
        p = run(graph, list(option), paths)
        max_p = max(p, max_p)
        checked += 1
        if checked % 1000 == 0:
            print("checked", checked)
    return max_p


def choices(graph, paths):
    # doesn't scale for real input
    #return itertools.permutations([k for k in graph.keys() if graph[k]["rate"]])

    first_maybes = []
    all_keys = [k for k in graph.keys() if graph[k]["rate"]]
    for option in itertools.permutations(all_keys, 5):
        location = "AA"
        time_spent = 0
        for valve in option:
            path = paths[(location, valve)]
            time_spent += path + 1
            location = valve
        score = run(graph, list(option), paths)
        first_maybes.append((option, time_spent, score))
    print("first", len(first_maybes))
    # take these first 5, score them all then sort and only take the best N
    _sorted = sorted(first_maybes, key=lambda item: item[2], reverse=True)
    next_set = _foo(graph, all_keys, 3, paths, _sorted)
    _sorted = sorted(next_set, key=lambda item: item[2], reverse=True)

    next_set = _foo(graph, all_keys, 3, paths, _sorted)
    _sorted = sorted(next_set, key=lambda item: item[2], reverse=True)

    next_set = _foo(graph, all_keys, 3, paths, _sorted)
    _sorted = sorted(next_set, key=lambda item: item[2], reverse=True)

    return _sorted


def _foo(graph, all_keys, num, paths, existing_options=None):
    extended_options = []
    for existing_option, time_spent, score in existing_options:
        for next_option in itertools.permutations([k for k in all_keys if k not in existing_option], num):
            if time_spent > 30:
                continue
            location = existing_option[-1]
            this_time = time_spent
            for valve in next_option:
                path = paths[(location, valve)]
                this_time += path + 1
                location = valve
            new_score = run(graph, list(existing_option + next_option), paths)
            extended_options.append((existing_option + next_option, this_time, new_score))
    return extended_options


def run(graph, order, paths):
    location = "AA"
    pressure_released = 0
    open_valves = []
    minutes_remaining = 30

    while minutes_remaining:
        pressure_released += sum(open_valves)
        if not order:
            minutes_remaining -= 1
            continue
        valve_to_open = order.pop(0)

        path = paths[(location, valve_to_open)]
        if path >= minutes_remaining:
            return pressure_released
        for _ in range(path):
            minutes_remaining -= 1
            pressure_released += sum(open_valves)
        open_valves.append(graph[valve_to_open]["rate"])
        minutes_remaining -= 1
        location = valve_to_open

    return pressure_released
"""
PAT = re.compile(r"Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? (.*)")


def parse(line):
    return PAT.match(line).groups()


def part_one(data):
    graph = {}
    for (valve, rate, tunnels) in data:
        graph[valve] = {
            "rate": int(rate),
            "tunnels": tunnels.split(", "),
        }

    pairs = list(itertools.combinations([k for k in graph.keys() if graph[k]["rate"] or k == "AA"], 2))
    paths = {}
    print("pairs", len(pairs))
    for pair in pairs:
        paths[pair] = shortest_path(graph, *pair)
        paths[tuple(reversed(pair))] = paths[pair]
    print("calculated all shortest path pairs")

    options = walk(graph, paths, 30)
    _sorted = sorted(options.values(), key=lambda item: item[1], reverse=True)
    return _sorted[0][1]


def walk(graph, paths, max_time, exclude=None):
    exclude = exclude or []
    ALL_VALVES = [k for k in graph.keys() if (graph[k]["rate"] and k not in exclude)]
    options = {("AA",): (list(), 0, max_time)}

    for _ in range(len(ALL_VALVES)):
        print("options size", len(options))
        for chosen_valves in list(options.keys()):
            open_valves, score, time_remaining = options[chosen_valves]
            if not time_remaining:
                continue
            del options[chosen_valves]
            for _next in [k for k in ALL_VALVES if k not in chosen_valves]:
                opened_valve, new_score, new_time = run_partial(graph, chosen_valves[-1], _next, paths, open_valves,
                                                                score, time_remaining)
                options[chosen_valves + (_next,)] = (
                    open_valves + [opened_valve] if opened_valve else open_valves, new_score, new_time)
    for path, (open_valves, score, time_remaining) in options.items():
        if time_remaining:
            for _ in range(time_remaining):
                score += sum(open_valves)
            options[path] = (open_valves, score, 0)

    return options


def run_partial(graph, current, _next, paths, open_valves, score, time_left):
    path = paths[(current, _next)]
    if path >= time_left + 1:
        # not enough time to traverse and open valve
        return None, score + (sum(open_valves) * time_left), 0

    for _ in range(path + 1):
        score += sum(open_valves)

    return graph[_next]["rate"], score, time_left - path - 1  # 1 to open the valve


def shortest_path(graph, start, end):
    explored = []

    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            neighbors = graph[node]["tunnels"]

            for neighbor in neighbors:
                if neighbor == end:
                    return len(path)
                new_path = list(path) + [neighbor]
                queue.append(new_path)

            explored.append(node)


def part_two_abondoned(data):
    graph = {}
    for (valve, rate, tunnels) in data:
        graph[valve] = {
            "rate": int(rate),
            "tunnels": tunnels.split(", "),
        }

    pairs = list(itertools.combinations([k for k in graph.keys() if graph[k]["rate"] or k == "AA"], 2))
    paths = {}
    print("pairs", len(pairs))
    for pair in pairs:
        paths[pair] = shortest_path(graph, *pair)
        paths[tuple(reversed(pair))] = paths[pair]
    print("calculated all shortest path pairs")

    options = walk_with_elephant({k: v["rate"] for k, v in graph.items() if v["rate"]}, paths)
    _sorted = sorted(options, key=lambda state: state.score, reverse=True)
    return _sorted[0]


@dataclass
class State:
    your_location: str = "AA"
    elephant_location: str = "AA"
    your_pending_moves: int = 0
    elephant_pending_moves: int = 0
    open_valves: Dict[str, int] = field(default_factory=dict)  # valve name -> flow rate
    score: int = 0
    time: int = 26

    def update_score_once(self):
        self.score += sum(self.open_valves.values())

    def update_score_remaining(self):
        self.score += (sum(self.open_valves.values()) * self.time)
        self.time = 0

    def num_of_actions(self):
        return min(self.time, max(self.your_pending_moves, self.elephant_pending_moves) + 1)

    def take_action(self, valve_rates):
        if self.your_pending_moves:
            self.your_pending_moves -= 1
        elif self.your_location not in self.open_valves:
            self.open_valves[self.your_location] = valve_rates[self.your_location]

        if self.elephant_pending_moves:
            self.elephant_pending_moves -= 1
        elif self.elephant_location not in self.open_valves:
            self.open_valves[self.elephant_location] = valve_rates[self.elephant_location]

        self.time -= 1

    @staticmethod
    def copy_from(other):
        state = State()
        for field in fields(State):
            setattr(state, field.name, getattr(other, field.name))
        state.open_valves = other.open_valves.copy()

        return state


def walk_with_elephant(valve_rates, paths) -> List[State]:
    ALL_VALVES = valve_rates.keys()
    live_options = [State()]
    finished_options = []
    while live_options:
        print("options size", len(live_options))
        for state in live_options[:]:
            live_options.pop()

            closed_valves = [v for v in ALL_VALVES if v not in state.open_valves]
            if not state.time or not closed_valves:
                finished_options.append(state)
                continue

            if len(closed_valves) == 1:
                next_state = State.copy_from(state)
                your_moves = paths[(next_state.your_location, closed_valves[0])]
                next_state.your_location = closed_valves[0]
                next_state.your_pending_moves = your_moves
                next_state.elephant_pending_moves = 0
                resolve_state(next_state, valve_rates)
                live_options.append(next_state)

                another_state = State.copy_from(state)
                elephant_moves = paths[(state.elephant_location, closed_valves[0])]
                another_state.elephant_location = closed_valves[0]
                another_state.elephant_pending_moves = elephant_moves
                another_state.your_pending_moves = 0
                resolve_state(another_state, valve_rates)
                live_options.append(another_state)
            else:
                for (your_dest, elephant_dest) in itertools.permutations(closed_valves, 2):
                    next_state = State.copy_from(state)
                    your_moves = paths[(next_state.your_location, your_dest)]
                    elephant_moves = paths[(next_state.elephant_location, elephant_dest)]
                    next_state.your_location = your_dest
                    next_state.elephant_location = elephant_dest
                    next_state.your_pending_moves = your_moves
                    next_state.elephant_pending_moves = elephant_moves
                    resolve_state(next_state, valve_rates)
                    live_options.append(next_state)

    # for all live/finished options with time remaining, finish their time
    all_options = finished_options + live_options
    for state in all_options:
        if state.time:
            state.update_score_remaining()
    return all_options


def resolve_state(state: State, valve_rates):
    for _ in range(state.num_of_actions()):
        state.update_score_once()
        state.take_action(valve_rates)


def part_two(data):
    graph = {}
    for (valve, rate, tunnels) in data:
        graph[valve] = {
            "rate": int(rate),
            "tunnels": tunnels.split(", "),
        }

    valves = [k for k in graph.keys() if graph[k]["rate"]]
    pairs = list(itertools.combinations(valves + ["AA"], 2))
    paths = {}
    print("pairs", len(pairs))
    for pair in pairs:
        paths[pair] = shortest_path(graph, *pair)
        paths[tuple(reversed(pair))] = paths[pair]
    print("calculated all shortest path pairs")

    # take half the keys and give them to the elephant...
    half = len(valves) // 2
    best = 0
    for elephant_valves in itertools.combinations(valves, half):
        human_valves = [v for v in valves if v not in elephant_valves]
        elephant_options = walk(graph, paths, 26, human_valves)
        human_options = walk(graph, paths, 26, elephant_valves)

        _sorted_elephant = sorted(elephant_options.values(), key=lambda item: item[1], reverse=True)
        _sorted_human = sorted(human_options.values(), key=lambda item: item[1], reverse=True)
        total = _sorted_elephant[0][1] + _sorted_human[0][1]
        best = max(best, total)

    return best


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")
