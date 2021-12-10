#!/usr/bin/env python3

from lib_inputs import get_input

from collections import defaultdict
import statistics

MATCH = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}


def score(item):
    symbol, count = item
    return {
               ")": 3,
               "]": 57,
               "}": 1197,
               ">": 25137
           }[symbol] * count


def detect_illegal(line):
    opens = []
    for symbol in line:
        if symbol in ("(", "[", "{", "<"):
            opens.append(symbol)
        else:
            other = MATCH[symbol]
            if opens.pop(-1) != other:
                return symbol

    return None


def part_one(data):
    illegals = defaultdict(int)

    for line in data:
        illegal_symbol = detect_illegal(line)
        if illegal_symbol:
            illegals[illegal_symbol] += 1

    return sum(map(score, illegals.items()))


def detect_incomplete(line):
    opens = []
    for symbol in line:
        if symbol in ("(", "[", "{", "<"):
            opens.append(symbol)
        else:
            opens.pop(-1)

    return opens


def score_incomplete(opens):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    score = 0
    for symbol in reversed(opens):
        score = score * 5 + scores[symbol]
    return score


def part_two(data):
    scores = []
    for line in data:
        if detect_illegal(line):
            continue
        opens = detect_incomplete(line)
        if opens:
            scores.append(score_incomplete(opens))

    return int(statistics.median(scores))


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        data = get_input(__file__, puzzle=puzzle, coerce=str)
        print(f"Part 1: Input {puzzle}, {part_one(data)}")
        print(f"Part 2: Input {puzzle}, {part_two(data)}")
