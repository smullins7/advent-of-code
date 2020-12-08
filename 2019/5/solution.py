import sys


def store(p, x):
    p[int(x)] = sys.stdin.readline(1)


OP_CODES = {
    "1": lambda p, x, y: int(x) + int(y),
    "01": lambda p, x, y: int(x) + int(y),
    "2": lambda p, x, y: int(x) * int(y),
    "02": lambda p, x, y: int(x) * int(y),
    "3": store,
    "03": store,
    "4": lambda p, x: print(int(x)),
    "04": lambda p, x: print(int(x))
}


def proc(program, cursor):
    #print(f"_{cursor}")
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
        #print(instruction, arg1, arg2, dest)
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


def part2(inputs):
  pass


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")][0].split(",")
    # not 424870 too low
    # should be 13285749
    print(part1(inputs))
    print(part2(inputs))

