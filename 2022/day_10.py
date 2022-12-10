from lib_inputs import get_input


class Program:

    def __init__(self):
        self.cycle = 1
        self.register = 1
        self.signal_strengths = []

    def run(self, cmd):
        self.accumulate_signal_strength()
        self.cycle += 1
        if cmd.startswith("addx"):
            self.accumulate_signal_strength()
            self.cycle += 1
            self.register += int(cmd.split(" ")[1])

    def accumulate_signal_strength(self):
        if self.cycle in (20, 60, 100, 140, 180, 220):
            self.signal_strengths.append(self.cycle * self.register)


class LcdProgram:

    def __init__(self):
        self.cycle = 1
        self.register = 1
        self.pixel_position = 0

    def run(self, cmd):
        self.draw_pixel()
        self.cycle += 1
        if cmd.startswith("addx"):
            self.draw_pixel()
            self.cycle += 1
            self.register += int(cmd.split(" ")[1])

    def draw_pixel(self):
        if self.pixel_position - 1 <= self.register <= self.pixel_position + 1:
            print("#", end='')
        else:
            print(".", end='')
        self.pixel_position = (self.pixel_position + 1) % 40
        if self.pixel_position == 0:
            print("")


def part_one(data):
    p = Program()
    for cmd in data:
        p.run(cmd)

    return sum(p.signal_strengths)


def part_two(data):
    p = LcdProgram()
    for cmd in data:
        p.run(cmd)


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")

