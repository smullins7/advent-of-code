from collections import defaultdict
from dataclasses import dataclass, field
from doctest import debug

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
                if self.expect and self.outputs[-1] != self.instructions[len(self.outputs) - 1]:
                    self.stop = True
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


def part_two(data):
    register_lines, program_lines = data
    program = parse_program(program_lines[0])

    options = defaultdict(list)
    for n in program:
        for this_byte, next_byte in try_to_get_back(n):
            if this_byte not in options:
                options[this_byte].append(next_byte)
                continue
            for k, bs in options.items():
                if bs[-1] == this_byte:
                    options[k].append(next_byte)

    print(program)
    for first, rest in options.items():
        buf = []
        for n in reversed([first] + rest):
            buf.append(format(n, "b").zfill(3))

        a = int("".join(buf), 2)
        registers = {
            'A': a,
            'B': 0,
            'C': 0,
        }

        computron = Computer(program, registers)
        computron.run()
        print(a, computron.outputs)

def try_to_get_back(n):
    for i in range(0,8):
        for j in range(0, 8):
            b = i ^ 2
            b = b ^ j
            b = b ^ 7
            if b % 8 == n:
                yield i, j

if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        #print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
        # 375340240026639
        # 1501612567510031
        # 1537922383035407
        # 9223372036854775807