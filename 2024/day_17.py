from collections import defaultdict
from dataclasses import dataclass, field
from doctest import debug
from itertools import permutations

from utils.inputs import get_grouped_inputs


def parse_registers(lines):
    d = {}
    for line in lines:
        _, reg, value = line.split(" ")
        d[reg[:-1]] = int(value)
    return d

def parse_program(line):
    return [int(v) for v in line.split(" ")[1].split(",")]

@dataclass
class Computer:
    instructions: list[int]
    registers: dict[str, int]
    expect: bool = False
    pointer: int = 0
    outputs: list[int] = field(default_factory=list)
    stop: bool = False

    def run(self):
        while not self.stop and self.pointer < len(self.instructions):
            self.tick()

    def next(self):
        value = self.instructions[self.pointer]
        self.pointer += 1
        return value

    def tick(self):
        opcode = self.next()
        operand = self.next()
        self.perform(opcode, operand)

    def get_combo_value(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.registers['A']
            case 5:
                return self.registers['B']
            case 6:
                return self.registers['C']

    def perform(self, opcode: int, operand: int):
        def _div():
            return int(self.registers['A'] / (2 ** self.get_combo_value(operand)))
        match opcode:
            case 0: #adv Division
                self.registers['A'] = _div()
            case 1: #bxl bitwise XOR
                self.registers['B'] = operand ^ self.registers['B']
            case 2: #bst
                self.registers['B'] = self.get_combo_value(operand) % 8
            case 3 : #jnz
                if self.registers['A'] != 0:
                    self.pointer = operand
            case 4: #bxc
                self.registers['B'] = self.registers['B'] ^ self.registers['C']
            case 5: #out
                self.outputs.append(self.get_combo_value(operand) % 8)
            case 6: #bvd
                self.registers['B'] = _div()
            case 7: #cdv
                self.registers['C'] = _div()



def part_one(data):
    register_lines, program_lines = data
    registers = parse_registers(register_lines)
    program = parse_program(program_lines[0])
    computron = Computer(program, registers)
    computron.run()
    return computron.outputs

def part_two_dig(data):
    register_lines, program_lines = data
    program = parse_program(program_lines[0])

    a = 0
    while True:
        registers = parse_registers(register_lines)
        registers['A'] = a

        computron = Computer(program, registers)
        computron.run()
        if program[:len(computron.outputs)] == computron.outputs:
            print(computron.outputs)
            print(a)
            a *= 8
        else:
            a += 1

def part_two_junk(data):
    register_lines, program_lines = data
    program = parse_program(program_lines[0])

    # 2,4,1,2,7,5,4,3,0,3,1,7,5,5,3,0
    # B = A % 8 -> last 3 bits
    # B = B ^ 2 -> +/- 2
    # C = A / (2 ** B) -> big num
    # B = B ^ C -> big num +/- B
    # A = A / 8 -> lose last 3 bits
    # B = B ^ 7 -> +/- 7
    # output B % 8 -> last 3 bits

    """
    101 
    """

    """
    C = A / (2**B)
    B= B ^ C, 
    B = B ^ 7 ->  0, B had to be 7
    output B % 8 = 0, B had to be 0
    """
    # 2,4,1,2,7,5,4,3,0,3,1,7,5,5,3,0
    #                          1   4    2
    a_binary = "1010011110000001111"

    to_try = [a_binary]
    while to_try:
        a_bin = to_try.pop(0)
        a = int(a_bin, 2)
        registers = {
            'A': a,
            'B': 0,
            'C': 0,
        }

        computron = Computer(program, registers)
        try:
            computron.run()
        except OverflowError:
            print("too big...")
            continue
        if program == computron.outputs:
            print(a)
            return
        elif program[:len(computron.outputs)] == computron.outputs:
            print(computron.outputs)
            to_try.append("0" + a_bin)
            to_try.append("1" + a_bin)


def part_two_abandon(data):
    register_lines, program_lines = data
    program = parse_program(program_lines[0])

    todo = [(list(reversed(program)), 0, [])]
    answers = []
    while todo:
        nums_to_print, previous, acc = todo.pop(0)
        to_print = nums_to_print.pop(0)

        for possible in eightbit(previous, to_print):
            copy = list(acc)
            copy.append(possible)
            if nums_to_print:
                todo.append((list(nums_to_print), possible, copy))
            else:
                answers.append(int("".join([format(n, "03b") for n in copy]), 2))
        else:
            with_zero = list(eightbit(0, to_print))
            if with_zero:
                copy = list(acc)
                copy.append(0)
                copy.append(with_zero[0])
                if nums_to_print:
                    todo.append((list(nums_to_print), with_zero[0], copy))
                else:
                    answers.append(int("".join([format(n, "03b") for n in copy]), 2))
            else:
                print("who knows")

    for a in answers:
        computron = Computer(program, {
            'A': a,
            'B': 0,
            'C': 0,
        })
        computron.run()
        if computron.outputs == program:
            print(a)
            return a

    return "im done"

def part_two(data):
    def to_n(l):
        return int("".join([format(n, "03b") for n in l]), 2)
    register_lines, program_lines = data
    program = parse_program(program_lines[0])
    start =[5, 3, 2, 2, 3]
    end =[0, 1, 2, 3, 6, 0, 1, 7]
    for i in range(10):
        print("trying ", i)
        for to_try in permutations(range(8), i):
            a = to_n(start + list(to_try) + end)
            c = Computer(program, {'A': a, 'B': 0, 'C': 0})
            c.run()
            if c.outputs == program:
                return a

    return "I give up"

def try_to_get_back(n):
    for i in range(0,8):
        for j in range(0, 8):
            b = i ^ 2
            b = b ^ j
            b = b ^ 7
            if b % 8 == n:
                yield i, j


def eightbit(previous: int, need_to_print: int):
    # B = A % 8 -> last 3 bits
    # B = B ^ 2 -> +/- 2
    # C = A / (2 ** B) -> big num
    # B = B ^ C -> big num +/- B
    # A = A / 8 -> lose last 3 bits
    # B = B ^ 7 -> +/- 7
    # output B % 8 -> last 3 bits
    for i in range(8):
        a = int(format(previous, "03b") + format(i, "03b"), 2)
        b = a % 8
        b = b ^ 2
        c = int(a / (2**b))
        b = b ^ c
        b = b ^ 7
        if b % 8 == need_to_print:
            yield i

if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        #print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")