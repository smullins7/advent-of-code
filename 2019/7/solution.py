from itertools import permutations

PHASES = list(range(0,5))
PHASES2 = list(range(5,10))


class Program(object):

    def __init__(self, program, input_queue: list, output_queue: list):
        self.program = program
        self.pointer = 0
        self.input_queue = input_queue
        self.output_queue = output_queue

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
        return self.input_queue.pop()

    def output(self, value):
        self.output_queue.insert(0, value)

    def __str__(self):
        return f"{self.pointer}, {self.input_queue}, {self.output_queue}"


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
        return False
    OP_CODES[opcode](program, modes)
    if opcode == "04":
        return True
    return run(program)


def part1(inputs):
    max_thruster_output = 0
    for phases in permutations(PHASES):
        output = None
        for phase in phases:
            p = Program(inputs, stores=[phase, output or 0])
            output = run(p)

        max_thruster_output = max(int(output), max_thruster_output)

    return max_thruster_output


def attempt(phase_signals: list[int], instructions) -> int:
    a_to_b = [phase_signals[1]]
    b_to_c = [phase_signals[2]]
    c_to_d = [phase_signals[3]]
    d_to_e = [phase_signals[4]]
    e_to_a = [0, phase_signals[0]]
    amp_a = Program(list(instructions), e_to_a, a_to_b)
    amp_b = Program(list(instructions), a_to_b, b_to_c)
    amp_c = Program(list(instructions), b_to_c, c_to_d)
    amp_d = Program(list(instructions), c_to_d, d_to_e)
    amp_e = Program(list(instructions), d_to_e, e_to_a)
    should_run = True

    while should_run:
        for amp in [amp_a, amp_b, amp_c, amp_d, amp_e]:
            should_run = run(amp)
    return int(amp_e.output_queue[0])

def part2(inputs):
    max_thruster_output = 0
    for phases in permutations(PHASES2):
        l = list(phases)
        max_thruster_output = max(attempt(l, inputs), max_thruster_output)

    return max_thruster_output


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")][0].split(",")
    #print(part1(inputs))
    print(part2(inputs))

