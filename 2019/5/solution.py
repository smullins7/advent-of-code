import sys


class Program(object):

    def __init__(self, program):
        self.program = program
        self.pointer = 0

    def next(self, mode="1"):
        v = self.program[self.pointer]
        self.increment()
        if mode == "0":
            v = self.program[int(v)]
        return v

    def write(self, pointer, value):
        self.program[int(pointer)] = str(value)

    def increment(self, step=1):
        self.pointer += step

    def jump(self, pointer):
        self.pointer = int(pointer)


def add(program, modes):
    first, second, dest = program.next(modes[0]), program.next(modes[1]), program.next()
    program.write(dest, int(first) + int(second))


def multiply(program, modes):
    first, second, dest = program.next(modes[0]), program.next(modes[1]), program.next()
    program.write(dest, int(first) * int(second))


def store(program, modes):
    dest = program.next()
    program.write(dest, sys.stdin.readline(1))


def output(program, modes):
    first = program.next(modes[0])
    print(first)


def jump_true(program, modes):
    first, second = program.next(modes[0]), program.next(modes[1])
    if int(first) > 0:
        program.jump(second)


def jump_false(program, modes):
    first, second = program.next(modes[0]), program.next(modes[1])
    if int(first) == 0:
        program.jump(second)


def less_than(program, modes):
    first, second, dest = program.next(modes[0]), program.next(modes[1]), program.next()
    program.write(dest, int(int(first) < int(second)))


def equals(program, modes):
    first, second, dest = program.next(modes[0]), program.next(modes[1]), program.next()
    program.write(dest, int(int(first) == int(second)))


OP_CODES = {
    "01": add,
    "02": multiply,
    "03": store,
    "04": output,
    "05": jump_true,
    "06": jump_false,
    "07": less_than,
    "08": equals
}


def get_value(program, index, mode):
    value = program[index]
    if mode == "0":
        value = program[value]
    return value


def parse_instruction(instruction):
    opcode = instruction[len(instruction) - 2:]
    modes = instruction[:len(instruction) - len(opcode)]
    if not modes:
        modes = "00"
    elif len(modes) == 1:
        modes = "0" + modes
    return "0" + opcode if len(opcode) == 1 else opcode, modes[::-1]


def proc(program, cursor):
    instruction = program[cursor]
    opcode = instruction[len(instruction)-2:]
    modes = instruction[:len(instruction)-len(opcode)]
    if opcode in ("01", "1", "02", "2"):
        arg1 = program[cursor + 1]
        arg2 = program[cursor + 2]
        dest = program[cursor + 3]
        if not modes or modes[-1] == "0":
            arg1 = program[int(arg1)]
        if not modes or len(modes) == 1 or modes[0] == "0":
            arg2 = program[int(arg2)]
        program[int(dest)] = str(OP_CODES[opcode](program, arg1, arg2))
        cursor += 3

    elif opcode == "99":
        return

    else:
        arg = program[cursor + 1]
        if opcode in ("04", "4") and (not modes or modes == "0"):
            arg = program[int(arg)]
        OP_CODES[opcode](program, arg)
        cursor += 1

    proc(program, cursor + 1)


def part1(inputs):
    proc(inputs, 0)


def part2(program):
    instruction = program.next()
    opcode, modes = parse_instruction(instruction)
    if opcode == "99":
        return
    OP_CODES[opcode](program, modes)
    part2(program)


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")][0].split(",")

    program = Program(inputs)
    print(part2(program))

    #program = Program(inputs)
    #print(part2(program))

