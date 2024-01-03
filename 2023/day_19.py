import re
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import Tuple

from utils.inputs import get_grouped_inputs

PAT = re.compile(r"^{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$")


def ruler(text):
    def foo(part):
        return eval(f"part.{text}")

    return foo


@dataclass
class Workflow:
    name: str
    raw: str
    rules: list = field(init=False)

    def __post_init__(self):
        self.rules = []
        for chunk in self.raw.split(","):
            if chunk.count(":"):
                text, destination = chunk.split(":")

                self.rules.append((ruler(text), destination))
            else:
                self.rules.append((lambda part: True, chunk))


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def total(self):
        return sum([self.x, self.m, self.a, self.s])


def parse_workflows(lines):
    d = {}
    for line in lines:
        name, stuff = line.split("{")
        d[name] = Workflow(name, stuff[:-1])
    return d


def parse_parts(lines):
    for line in lines:
        m = PAT.match(line)
        yield Part(*[int(n) for n in m.groups()])


def eval_part(part: Part, workflows: dict[str, Workflow], name: str = "in") -> int:
    w = workflows[name]
    for rule_func, destination in w.rules:
        if rule_func(part):
            if destination == "A":
                return part.total()
            elif destination == "R":
                return 0
            else:
                return eval_part(part, workflows, destination)
    print("should not have happened...")
    return 0


def part_one(data):
    rules, part_lines = data
    workflows = parse_workflows(rules)
    parts = parse_parts(part_lines)
    return sum(eval_part(p, workflows) for p in parts)


@dataclass(unsafe_hash=True)
class RangePart:
    x: Tuple[int, int] = (1, 4001)
    m: Tuple[int, int] = (1, 4001)
    a: Tuple[int, int] = (1, 4001)
    s: Tuple[int, int] = (1, 4001)

    def total(self):
        return sum([
            len(range(*self.x)),
            len(range(*self.m)),
            len(range(*self.a)),
            len(range(*self.s))
        ])


def ruler2(text):
    def foo(part: RangePart):
        copied, next_one = copy(part), copy(part)
        if "<" in text:
            letter, upper = text.split("<")
            current_min, current_max = part.__getattribute__(letter)
            if current_min > int(upper):
                return False, None
            copied.__setattr__(letter, (current_min, int(upper)))
            next_one.__setattr__(letter, (int(upper), current_max))
            return copied, next_one
        elif ">" in text:
            letter, lower = text.split(">")
            current_min, current_max = part.__getattribute__(letter)
            if current_max < int(lower):
                return False, None
            copied.__setattr__(letter, (int(lower), current_max))
            next_one.__setattr__(letter, (current_min, int(lower)))
            return copied, next_one
        else:
            return True, None

    return foo


@dataclass
class RangeWorkflow:
    name: str
    raw: str
    rules: list = field(init=False)

    def __post_init__(self):
        self.rules = []
        for chunk in self.raw.split(","):
            if chunk.count(":"):
                text, destination = chunk.split(":")
                self.rules.append((ruler2(text), destination))
            else:
                self.rules.append((lambda part: (True, None), chunk))


def rec(part: RangePart, workflows: dict[str, RangeWorkflow], answers: set[RangePart], name: str = "in"):
    workflow = workflows[name]
    previous = None
    for rule, destination in workflow.rules:
        answer, next_one = rule(previous or part)
        if answer is False:
            break
        elif answer is not True:
            if destination == "R":
                break
            if destination == "A":
                answers.add(answer)
                break
            answers.update(rec(answer, workflows, answers, destination))
            previous = answer
        else:
            answers.union(rec(previous, workflows, answers, destination))
    return answers


def part_two(data):
    rules, _ = data
    workflows = {}
    for rule in rules:
        name, stuff = rule.split("{")
        w = RangeWorkflow(name, stuff[:-1])
        workflows[w.name] = w
    part = RangePart()

    all_of_them = rec(part, workflows, set())



if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        #print(f"{f.__name__}:\n\t{f(real_data)}")
