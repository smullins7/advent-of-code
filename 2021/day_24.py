#!/usr/bin/env python3
from dataclasses import dataclass

from lib_inputs import get_input


@dataclass
class ALU:
    inputs: []
    commands: []
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    def get(self, attr):
        return int(self.__getattribute__(attr))

    def parse(self, s):
        if s.count(" ") == 1:
            return s.split(" ") + [None]
        cmd, first, second = s.split(" ")
        if second.isalpha():
            second = self.get(second)
        return cmd, first, int(second)

    def do_all(self):
        for _ in range(len(self.commands)):
            self.next()

    def next(self):
        cmd, first, second = self.parse(self.commands.pop(0))
        if cmd == "inp":
            self.__setattr__(first, self.inputs.pop(0))
        elif cmd == "add":
            self.__setattr__(first, self.get(first) + second)
        elif cmd == "mul":
            self.__setattr__(first, self.get(first) * second)
        elif cmd == "div":
            self.__setattr__(first, self.get(first) // second)
        elif cmd == "mod":
            self.__setattr__(first, self.get(first) % second)
        elif cmd == "eql":
            self.__setattr__(first, int(self.get(first) == second))
        else:
            raise Exception(f"Unknown command: {cmd}")


last = """inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y"""


def solve_last_to_be_z_is_zero(*args):
    for i in range(1, 10):
        for z in range(0, 10000):
            alu = ALU([i], [x.strip() for x in last.split("\n")], z=z)
            alu.do_all()
            if alu.z == 0:
                print(i, z)


def exec_to_match(commands, target_z, offset):
    for i in reversed(range(1, offset + 1)):
        for z in range(0, 10000):
            alu = ALU([i], list(commands), z=z)
            alu.do_all()
            if alu.z == target_z:
                return i, z

    return -1, -1


def chunk_commands(commands):
    chunks = []
    chunk = []
    for command in commands:
        if command.startswith("inp") and chunk:
            chunks.append(chunk)
            chunk = []

        chunk.append(command)
    return chunks + [chunk]


def prune(solutions):
    lookup = {}
    for digits, z_val in solutions.items():
        if z_val not in lookup or lookup[z_val] < int(digits):
            lookup[z_val] = int(digits)

    pruned = {}
    for z_val, digits in lookup.items():
        pruned[str(digits)] = z_val
    return pruned


def reverse_solve(commands):
    solved = {
        "": 0
    }
    for i, chunk in enumerate(reversed(chunk_commands(commands))):
        next_solve = {}
        for digits, expected_z in solved.items():
            next_digit, z_value = exec_to_match(chunk, expected_z, 9)
            next_solve[digits + str(next_digit)] = z_value

        solved = prune(next_solve)
        print(solved)

    print(solved)


def nope(commands):
    chunks = chunk_commands(commands)

    def dfs(command_chunk_index, possible_digit, target_z, running_solution):
        if command_chunk_index == -1:
            return running_solution

        found = False
        for z in range(0, 5000000):
            alu = ALU([possible_digit], list(chunks[command_chunk_index]), z=z)
            alu.do_all()
            if alu.z == target_z:
                running_solution += str(possible_digit)
                found = True
                print(running_solution)
                break
        if found:
            for i in reversed(range(1, 10)):
                dfs(command_chunk_index - 1, i, z, running_solution)


    for i in reversed(range(1, 10)):
        solution = dfs(len(chunks) - 1, i, 0, "")
        if solution and len(solution) == 14:
            return solution
    return "panic!!!"


# OMG FINALLY WHAT A WASTE OF TIME!!!!
def only_nums_that_matter(commands):
    def _to_i(s):
        return int(s.split(" ")[-1])

    n1, n2, n3 = [], [], []
    for i, command in enumerate(commands):
        if i % 18 == 4:
            n1.append(_to_i(command))
        elif i % 18 == 5:
            n2.append(_to_i(command))
        elif i % 18 == 15:
            n3.append(_to_i(command))
    return list(zip(n1, n2, n3))


def part_one(commands):

    def doit(params, z=0, digits=""):
        if not params:
            return digits if z == 0 else None
        n1, n2, n3 = params.pop(0)
        if n1 == 26:
            if not (1 <= (z % 26) + n2 <= 9):
                return None
            return doit(list(params), z // n1, digits + str((z % 26) + n2))
        for i in reversed(range(1, 10)):
            result = doit(list(params), z // n1 * 26 + i + n3, digits + str(i))
            if result is not None:
                return result

    return doit(only_nums_that_matter(commands))


def part_two(commands):
    def doit(params, z=0, digits=""):
        if not params:
            return digits if z == 0 else None
        n1, n2, n3 = params.pop(0)
        if n1 == 26:
            if not (1 <= (z % 26) + n2 <= 9):
                return None
            return doit(list(params), z // n1, digits + str((z % 26) + n2))
        for i in range(1, 10):
            result = doit(list(params), z // n1 * 26 + i + n3, digits + str(i))
            if result is not None:
                return result

    return doit(only_nums_that_matter(commands))


def print_stuff(commands):
    for i, command in enumerate(commands):
        # well every one of the 14 "chunks" has exactly 18 commands even though
        # most of them look like junk and just futz around with x and y getting reset
        print(f"{i % 18}, {command}")


if __name__ == "__main__":
    for puzzle in (1,):
        for f in (print_stuff, part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=str)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
