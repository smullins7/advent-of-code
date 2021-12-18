from itertools import permutations

PHASES = list(range(0,5))
PHASES2 = list(range(5,10))


class Program(object):

    def __init__(self, program, stores=None):
        self.program = program
        self.pointer = 0
        self.stores = stores or []

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

    def input(self):
        return self.stores.pop(0) if self.stores else input()

    def output(self, value):
        self.stores.append(value)


def add(program, modes):
    first, second, dest = program.next(modes[0]), program.next(modes[1]), program.next()
    program.write(dest, int(first) + int(second))


def multiply(program, modes):
    first, second, dest = program.next(modes[0]), program.next(modes[1]), program.next()
    program.write(dest, int(first) * int(second))


def store(program, modes):
    dest = program.next()
    program.write(dest, program.input())


def output(program, modes):
    first = program.next(modes[0])
    program.output(first)


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


def run(program):
    instruction = program.next()
    opcode, modes = parse_instruction(instruction)
    if opcode == "99":
        return
    OP_CODES[opcode](program, modes)
    if opcode == "04":
        return
    run(program)


def part1(inputs):
    max_thruster_output = 0
    for phases in permutations(PHASES):
        output = None
        for phase in phases:
            p = Program(inputs, stores=[phase, output or 0])
            output = run(p)

        max_thruster_output = max(int(output), max_thruster_output)

    return max_thruster_output


def part2(inputs):
    max_thruster_output = 0
    for phases in permutations(PHASES2):
        l = list(phases)
        amp_a = Program(inputs, stores=[l[0], 0])

        amp_b = Program(list(inputs), stores=[l[1]])
        amp_c = Program(list(inputs), stores=[l[2]])
        amp_d = Program(list(inputs), stores=[l[3]])
        amp_e = Program(list(inputs), stores=[l[4]])
        while True:
            run(amp_a)
            amp_b.stores.insert(0, amp_a.stores.pop())
            run(amp_b)
            amp_c.stores.insert(0, amp_b.stores.pop())
            run(amp_c)
            amp_d.stores.insert(0, amp_c.stores.pop())
            run(amp_d)
            amp_e.stores.insert(0, amp_d.stores.pop())
            run(amp_e)
            if amp_e.program[amp_e.pointer] == "99":
                break
            amp_a.stores.insert(0, amp_e.stores.pop())
        max_thruster_output = max(int(amp_e.stores[0]), max_thruster_output)

    return max_thruster_output


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./example.txt")][0].split(",")
    #print(part1(inputs))
    print(part2(inputs))

