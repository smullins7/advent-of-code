import re
from itertools import product

from utils.inputs import get_grouped_inputs

button_re = re.compile(r"^Button [A|B]: X\+(\d+), Y\+(\d+)$")
prize_re = re.compile(r"Prize: X=(\d+), Y=(\d+)$")

def parse_machine(lines, offset=0):
    a = button_re.match(lines[0]).groups()
    b = button_re.match(lines[1]).groups()
    prize = prize_re.match(lines[2]).groups()

    return {
        'a_x': int(a[0]),
        'a_y': int(a[1]),
        'b_x': int(b[0]),
        'b_y': int(b[1]),
        'p_x': int(prize[0]) + offset,
        'p_y': int(prize[1]) + offset,
    }

def evaluate_machine(points: dict[str, int]) -> int:
    min_cost = None
    for a_count, b_count in product(range(0, 101), range(0, 101)):
        if (points['a_x'] * a_count + points['b_x'] * b_count) == points['p_x'] and (points['a_y'] * a_count + points['b_y'] * b_count) == points['p_y']:
            cost = a_count * 3 + b_count
            if min_cost is None or cost < min_cost:
                min_cost = cost
    if min_cost:
        print("Can win on", points, min_cost)
    return min_cost or 0

def part_one(data):
    total = 0
    for lines in data:
        total += evaluate_machine(parse_machine(lines))
    return total


def solve_b(a_x, a_y, b_x, b_y, t_x, t_y) -> int:
    b = (t_y * a_x - a_y * t_x) / (b_y * a_x - b_x * a_y)
    return int(b) if b == int(b) else 0

def solve_a(a_x, b_x, t_x, b) -> int:
    a = (t_x - b * b_x) / a_x
    return int(a) if a == int(a) else 0


def part_two(data):
    total = 0
    for lines in data:
        machine = parse_machine(lines, offset=10000000000000)
        b = solve_b(machine['a_x'], machine['a_y'], machine['b_x'], machine['b_y'], machine['p_x'], machine['p_y'])
        if not b:
            continue
        a = solve_a(machine['a_x'], machine['b_x'], machine['p_x'], b)
        if not a:
            continue
        total += a * 3 + b
    return total


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")