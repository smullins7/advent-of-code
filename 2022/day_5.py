from collections import defaultdict

from lib_inputs import get_input
import re

MOVE_PAT = re.compile(r"move (?P<move>\d+) from (?P<from>\d+) to (?P<to>\d+)")

def parse(data):
    stacks, moves = defaultdict(list), []
    read_stacks = True
    for line in data:
        if line and read_stacks:
            for pos, crate in read_stack(line).items():
                stacks[pos].append(crate)
        else:
            read_stacks = False
            m = MOVE_PAT.match(line)
            if m:
                moves.append((int(m.group("move")), int(m.group("from")) - 1, int(m.group("to")) - 1))
    return stacks, moves


def read_stack(line):
    crates = {}
    for i, c in enumerate(line):
        if c.isalpha():
            crates[int((i -1) / 4)] = c
    return crates


def part_one(stacks, moves):
    for (move, _from, to) in moves:
        while move > 0:
            stacks[to].insert(0, stacks[_from].pop(0))
            move -= 1

    return "".join([stacks[k][0] for k in sorted(stacks)])


def part_two(stacks, moves):
    for (move, _from, to) in moves:
        temp = [stacks[_from].pop(0) for n in range(0, move)]
        stacks[to] = temp + stacks[to]

    return "".join([stacks[k][0] for k in sorted(stacks)])


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        stacks, moves = parse(data)
        print(f"{f.__name__}:\n\t{f(stacks, moves)}")

