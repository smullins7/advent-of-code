import json
from enum import Enum
from functools import cmp_to_key

from utils.inputs import get_grouped_input


class Result(Enum):
    CORRECT = 1
    INCORRECT = 2
    CONTINUE = 3


def done(result):
    return result in (Result.CORRECT, Result.INCORRECT)


def compare_int(left, right):
    if left < right:
        return Result.CORRECT
    elif left > right:
        return Result.INCORRECT
    return Result.CONTINUE


def compare_list(left, right):
    for i, item in enumerate(left):
        if i == len(right):
            return Result.INCORRECT
        result = compare(item, right[i])
        if done(result):
            return result

    if len(right) > len(left):
        return Result.CORRECT
    return Result.CONTINUE


def compare(first, second):
    if type(first) == int and type(second) == int:
        result = compare_int(first, second)
        if done(result):
            return result
    elif type(first) == list and type(second) == list:
        result = compare_list(first, second)
        if done(result):
            return result
    elif type(first) == int:
        result = compare_list([first], second)
        if done(result):
            return result
    else:  # first is list
        result = compare_list(first, [second])
        if done(result):
            return result

    return Result.CONTINUE


def sort_compare(a, b):
    result = compare(a, b)
    if result == Result.CORRECT:
        return -1
    return 1


def part_one(data):
    correct = []
    for i, (first, second) in enumerate(data):
        result = compare(first, second)
        if result == Result.CORRECT:
            correct.append(i + 1)

    return sum(correct)


def part_two(data):
    flattened = [item for sublist in data for item in sublist] + [[[2]], [[6]]]
    sorty = sorted(flattened, key=cmp_to_key(sort_compare))
    return (sorty.index([[2]]) + 1) * (sorty.index([[6]]) + 1)


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_grouped_input(__file__, is_sample=0, coerce=json.loads)
        print(f"{f.__name__}:\n\t{f(data)}")
