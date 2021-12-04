#!/usr/bin/env python3

import itertools

from lib_inputs import get_input


class BingoBoard:

    def __init__(self):
        self.rows = []

    def add_row(self, line):
        self.rows.append(list(filter(None, line.split(" "))))

    def has_bingo(self, seen):
        for row in self.rows:
            if seen.issuperset(set(row)):
                return True
        for col in range(len(self.rows[0])):
            if seen.issuperset(set([row[col] for row in self.rows])):
                return True
        return False

    def sum_of_not_seen(self, seen):
        return sum(map(int, filter(lambda n: n not in seen, itertools.chain(*self.rows))))


def parse(data):
    numbers = data[0].split(",")
    boards, board = [], None
    for line in data[1:]:
        if not line:
            if board:
                boards.append(board)
            board = BingoBoard()
        else:
            board.add_row(line)

    boards.append(board)
    return numbers, boards


def play_bingo(numbers, boards, first=True):
    winners = set()
    seen = set()
    for number in numbers:
        for i, board in enumerate(boards):
            seen.add(number)
            if board.has_bingo(seen):
                winners.add(i)
                if first or len(winners) == len(boards):
                    return board, number, seen


def part_one(numbers, boards):
    winning_board, number, seen = play_bingo(numbers, boards)
    print(winning_board.sum_of_not_seen(seen), int(number))
    return winning_board.sum_of_not_seen(seen) * int(number)


def part_two(numbers, boards):
    winning_board, number, seen = play_bingo(numbers, boards, first=False)
    print(winning_board.sum_of_not_seen(seen), int(number))
    return winning_board.sum_of_not_seen(seen) * int(number)


for puzzle in ("sample", 1):
    data = get_input(4, puzzle=puzzle, coerce=str)
    numbers, boards = parse(data)
    print(f"Part 1: Input {puzzle}, {part_one(numbers, boards)}")
    print(f"Part 2: Input {puzzle}, {part_two(numbers, boards)}")
