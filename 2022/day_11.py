import math
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import List, Dict

from utils.inputs import get_grouped_input
from utils.operators import from_op_string


@dataclass
class Monkey1:
    id: int
    items: List[int]
    op: ()
    test: ()
    action_true: int
    action_false: int
    inspections: int = 0

    def take_turn(self, monkeys: Dict):
        for item in self.items:
            new_worry_level = self.op(item) // 3
            monkeys[self.action_true if self.test(new_worry_level) else self.action_false].catch(new_worry_level)
            self.inspections += 1
        self.items = []

    def catch(self, item):
        self.items.append(item)

    @staticmethod
    def from_lines(lines):
        _id, items, op, test, action_true, action_false = lines
        left, symbol, right = op.split(" = ")[1].split(" ")

        return Monkey1(
            int(_id.split(" ")[1][:-1]),
            [int(v.strip()) for v in items.split(":")[1].split(",")],
            lambda n: from_op_string(symbol)(n if left == "old" else int(left), n if right == "old" else int(right)),
            lambda n: n % int(test.split(" ")[-1]) == 0,
            int(action_true.split(" ")[-1]),
            int(action_false.split(" ")[-1]),
        )


def part_one(data):
    monkeys = {}
    for monkey_lines in data:
        monkey = Monkey1.from_lines(monkey_lines)
        monkeys[monkey.id] = monkey

    ids = sorted(monkeys)
    for _ in range(20):
        for _id in ids:
            monkeys[_id].take_turn(monkeys)

    return reduce(mul, sorted([monkey.inspections for monkey in monkeys.values()])[-2:])


@dataclass
class Monkey2:
    id: int
    items: List[int]
    op: ()
    divisor: int
    action_true: int
    action_false: int
    inspections: int = 0
    global_divisor: int = 0

    def take_turn(self, monkeys: Dict):
        for item in self.items:
            new_worry_level = self.op(item) % self.global_divisor
            divisible = new_worry_level % self.divisor == 0
            monkeys[self.action_true if divisible else self.action_false].catch(new_worry_level)
            self.inspections += 1
        self.items = []

    def catch(self, item):
        self.items.append(item)

    @staticmethod
    def from_lines(lines):
        _id, items, op, test, action_true, action_false = lines
        left, symbol, right = op.split(" = ")[1].split(" ")
        return Monkey2(
            int(_id.split(" ")[1][:-1]),
            [int(v.strip()) for v in items.split(":")[1].split(",")],
            lambda n: from_op_string(symbol)(n if left == "old" else int(left), n if right == "old" else int(right)),
            int(test.split(" ")[-1]),
            int(action_true.split(" ")[-1]),
            int(action_false.split(" ")[-1]),
        )


def part_two(data):
    monkeys = {}
    for monkey_lines in data:
        monkey = Monkey2.from_lines(monkey_lines)
        monkeys[monkey.id] = monkey

    global_divisor = math.lcm(*[m.divisor for m in monkeys.values()])
    for monkey in monkeys.values():
        monkey.global_divisor = global_divisor
    ids = sorted(monkeys)
    for _ in range(10000):
        for _id in ids:
            monkeys[_id].take_turn(monkeys)

    return reduce(mul, sorted([monkey.inspections for monkey in monkeys.values()])[-2:])


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_grouped_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")

