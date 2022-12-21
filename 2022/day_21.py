from dataclasses import dataclass
from typing import List, Dict

from utils.inputs import get_input
from utils.operators import from_op_string, counter_op, OPS


@dataclass
class Monkey:
    id: str
    value: int = None
    left: str = None
    right: str = None
    op: () = None

    def resolve(self, resolutions):
        if self.value is not None:
            return self.value

        if self.left in resolutions and self.right in resolutions:
            return self.op(resolutions[self.left], resolutions[self.right])


def parse(line):
    monkey_id, stuff = line.split(": ")
    if stuff.isnumeric():
        return Monkey(id=monkey_id, value=int(stuff))

    left, op, right = stuff.split(" ")
    return Monkey(id=monkey_id, left=left, right=right, op=from_op_string(op))


def part_one(data: List[Monkey]):
    resolved = {}
    while "root" not in resolved:
        for monkey in data[:]:
            value = monkey.resolve(resolved)
            if value:
                resolved[monkey.id] = value
                data.remove(monkey)

    return resolved["root"]


def solve(monkey_id: str, monkeys: Dict[str, Monkey]):
    monkey = monkeys[monkey_id]
    if monkey.value:
        return monkey.value

    return monkey.op(solve(monkey.left, monkeys), solve(monkey.right, monkeys))


def dfs_solve(monkey_id, monkeys, root_value):
    if monkey_id == "humn":
        return root_value
    monkey = monkeys[monkey_id]
    if can_solve(monkey.left, monkeys):
        root_value = apply(monkey.op, solve(monkey.left, monkeys), root_value)
        return dfs_solve(monkey.right, monkeys, root_value)
    elif can_solve(monkey.right, monkeys):
        root_value = counter_op(monkey.op)(root_value, solve(monkey.right, monkeys))
        return dfs_solve(monkey.left, monkeys, root_value)


def can_solve(monkey_id: str, monkeys):
    monkey = monkeys[monkey_id]
    if monkey.id == "humn":
        return False
    left = can_solve(monkey.left, monkeys) if monkey.left else True
    right = can_solve(monkey.right, monkeys) if monkey.right else True
    return left and right


def apply(op: (), left_val, right_val):
    if op in (OPS["+"], OPS["*"]):
        return counter_op(op)(right_val, left_val)

    return op(left_val, right_val)


def part_two(data: List[Monkey]):
    monkeys = {monkey.id: monkey for monkey in data}
    root = monkeys["root"]
    root_value = solve(root.right, monkeys) if can_solve(root.right, monkeys) else solve(root.left, monkeys)
    return dfs_solve(root.left, monkeys, root_value)


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")

