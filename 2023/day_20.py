import math
from copy import copy
from dataclasses import dataclass, field
from itertools import count

from utils.inputs import get_inputs

TYPES = {
    "%": "flip-flop",
    "&": "conjunction",
    "b": "broadcaster"
}


@dataclass
class Module:
    name: str
    type: str
    destinations: list[str]
    bit: bool = False
    received: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.name.isalpha():
            self.name = self.name[1:]

    @staticmethod
    def parse(line):
        name, dest = line.split(" -> ")
        return Module(name, TYPES[name[0]], dest.split(", "))

    def receive(self, source: str, pulse: bool):
        # print(f"{source} -> {pulse} -> {self.name}")
        if self.type == "broadcaster":
            return pulse
        elif self.type == "flip-flop" and not pulse:
            self.bit = not self.bit
            return self.bit
        elif self.type == "conjunction":
            self.received[source] = pulse
            return not all(self.received.values())


def prep_modules(data):
    modules = {m.name: copy(m) for m in data}
    to_add = []
    for name, module in modules.items():
        for dest in module.destinations:
            if dest not in modules:
                to_add.append(Module(dest, "terminal", []))
                continue

            _module = modules[dest]
            if _module.type == "conjunction":
                _module.received[name] = False

    for module in to_add:
        modules[module.name] = module
    return modules


def part_one(data):
    modules = prep_modules(data)

    lows, highs = 0, 0
    for _ in range(1000):
        # breadth first
        q = [("button", "broadcaster", False)]
        while q:
            source, dest, pulse = q.pop(0)
            if pulse:
                highs += 1
            else:
                lows += 1
            if dest not in modules:
                continue
            module = modules[dest]
            next_pulse = module.receive(source, pulse)
            if next_pulse is None:
                continue
            for next_dest in module.destinations:
                q.append((module.name, next_dest, next_pulse))
    return lows * highs


def part_two(data):
    modules = prep_modules(data)
    target = None
    for module in modules.values():
        if "rx" in module.destinations:
            target = module.name
            break

    look_for = set()
    for module in modules.values():
        if target in module.destinations:
            look_for.add(module.name)

    lowest = {}
    for presses in count(1):
        q = [("button", "broadcaster", False)]
        while q:
            source, dest, pulse = q.pop(0)
            module = modules[dest]
            next_pulse = module.receive(source, pulse)
            if next_pulse is None:
                continue
            for next_dest in module.destinations:
                q.append((module.name, next_dest, next_pulse))
            if dest in look_for and next_pulse:
                lowest[dest] = presses
        if len(lowest) == len(look_for):
            return math.lcm(*lowest.values())


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=Module.parse)
    for f in (part_one, part_two):
        # print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
