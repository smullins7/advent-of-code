#!/usr/bin/env python3
import json
from dataclasses import dataclass
from functools import reduce
import itertools
from lib_inputs import get_input


def add(first, second):
    return [first, second]


@dataclass
class ShouldSplit:
    flag: bool = False


def can_reduce(number):
    should_split = ShouldSplit()

    def depth(element):
        if not element:
            return 0
        elif not isinstance(element, list):
            if element > 9:
                should_split.flag = True
            return 0
        return 1 + max(depth(item) for item in element)

    return max(map(depth, number)) == 4 or should_split.flag


def find_left_most_number(l):
    for l2 in l:
        if isinstance(l2, int):
            return l
        return find_left_most_number(l2)


def find_right_most_number(l):
    for l2 in reversed(l):
        if isinstance(l2, int):
            return l
        return find_right_most_number(l2)

def explode(number):
    # we know depth of four
    for i, n in enumerate(number):
        if isinstance(n, list):
            for j, n2 in enumerate(n):
                if isinstance(n2, list):
                    for k, n3 in enumerate(n2):
                        if isinstance(n3, list):
                            target = None
                            for l, n4 in enumerate(n3):
                                if isinstance(n4, list):
                                    target = n4
                                    break
                            if target:
                                n3[l] = 0
                                if l == 0:
                                    if isinstance(n3[1], int):
                                        n3[1] += target[1]
                                    else:
                                        n3[1][0] += target[1]
                                    # can i find the _right most_ number to my left?
                                    list_to_update = None
                                    if k == 1:
                                        if isinstance(n2[0], int):
                                            n2[0] += target[0]
                                        else:
                                            list_to_update = find_right_most_number(n2[0])
                                    elif j == 1:
                                        if isinstance(n[0], int):
                                            n[0] += target[0]
                                        else:
                                            list_to_update = find_right_most_number(n[0])
                                    elif i == 1:
                                        if isinstance(number[0], int):
                                            number[0] += target[0]
                                        else:
                                            list_to_update = find_right_most_number(number[0])

                                    if list_to_update:
                                        list_to_update[1] += target[0]
                                else:
                                    n3[0] += target[0]
                                    list_to_update = None
                                    if k == 0:
                                        if isinstance(n2[1], int):
                                            n2[1] += target[1]
                                        else:
                                            list_to_update = find_left_most_number(n2[1])
                                    elif j == 0:
                                        if isinstance(n[1], int):
                                            n[1] += target[1]
                                        else:
                                            list_to_update = find_left_most_number(n[1])
                                    elif i == 0:
                                        if isinstance(number[1], int):
                                            number[1] += target[1]
                                        else:
                                            list_to_update = find_left_most_number(number[1])

                                    if list_to_update:
                                        list_to_update[0] += target[1]

                                return True

    return False


def split(number):
    def _split(number):
        return [number // 2, (number // 2) + (1 if number % 2 != 0 else 0)]
    for i, n in enumerate(number):
        if isinstance(n, int):
            if n > 9:
                number[i] = _split(n)
                return
        else:
            for j, n2 in enumerate(n):
                if isinstance(n2, int):
                    if n2 > 9:
                        n[j] = _split(n2)
                        return
                else:
                    for k, n3 in enumerate(n2):
                        if isinstance(n3, int):
                            if n3 > 9:
                                n2[k] = _split(n3)
                                return
                        else:
                            for l, n4 in enumerate(n3):
                                if n4 > 9:
                                    n3[l] = _split(n4)
                                    return




def workit(first, second):
    added = add(first, second)
    while can_reduce(added):
        changed = True
        while changed:
            changed = explode(added)

        split(added)
    return added


def pop_pop(number):
    if isinstance(number, list):
        first = number[0] if isinstance(number[0], int) else pop_pop(number[0])
        second = number[1] if isinstance(number[1], int) else pop_pop(number[1])

        return 3 * first + 2 * second
    return number



def part_one(data):
    data = map(json.loads, data)
    single_num = reduce(workit, data)
    #print("reduced", single_num)
    return pop_pop(single_num)


def part_two(data):
    return max(map(part_one, itertools.permutations(data, 2)))


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")
