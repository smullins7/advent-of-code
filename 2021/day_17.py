#!/usr/bin/env python3

from lib_inputs import get_input


def parse(line):
    return [[int(s3) for s3 in s2[2:].split("..")] for s2 in line[13:].split(", ")]


def determine_steps(target_x_min, target_x_max):
    possible = []

    for x in range(1, target_x_max + 1):
        steps = 0
        position = 0
        velocity = x

        while position < target_x_max and velocity > 0:
            position += velocity
            steps += 1
            velocity -= 1
            if target_x_min <= position <= target_x_max:
                possible.append((steps, x))
        if velocity == 0:
            # feeling lazy today, oh well
            for buffer_step in range(steps + 1, steps + 150):
                possible.append((buffer_step, x))
    return possible


def go(x, y, steps):
    x_p, y_p = 0, 0
    for _ in range(steps):
        x_p += x
        y_p += y
        x = max(x - 1, 0)
        y -= 1
    return x_p, y_p


def highest_y(y, steps):
    y_p = 0
    highest = 0
    for _ in range(steps):
        y_p += y
        y -= 1
        if y_p > highest:
            highest = y_p
        if y <= 0:
            break
    return highest


def part_one(data):
    x_min, x_max = data[0]
    y_min, y_max = data[1]
    solution = None
    for steps, x in determine_steps(x_min, x_max):
        current_y = y_min
        while True:
            x_p, y_p = go(x, current_y, steps)
            if x_min <= x_p <= x_max and y_min <= y_p <= y_max:
                high = highest_y(current_y, steps)
                if solution is None or high > solution:
                    solution = high
            elif y_p > y_max:
                break
            current_y += 1

    return solution


def part_two(data):
    x_min, x_max = data[0]
    y_min, y_max = data[1]
    solutions = set()
    for steps, x in determine_steps(x_min, x_max):
        current_y = y_min
        while True:
            x_p, y_p = go(x, current_y, steps)
            if x_min <= x_p <= x_max and y_min <= y_p <= y_max:
                solutions.add((x, current_y))
            elif y_p > y_max:
                break
            current_y += 1

    return len(solutions)


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=parse)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
