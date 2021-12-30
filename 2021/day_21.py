#!/usr/bin/env python3
from dataclasses import dataclass
from collections import defaultdict
import itertools


@dataclass
class D100:
    value: int = 1
    rolled: int = 0

    def roll(self):
        self.rolled += 1
        val = self.value
        self.value += 1
        if self.value == 101:
            self.value = 1
        return val


@dataclass
class Pawn:
    position: int
    score: int = 0

    def move(self, die):
        total = sum([die.roll() for _ in range(3)])
        self.position += total
        while self.position > 10:
            self.position = self.position - 10
        self.score += self.position


def part_one(p1_start, p2_start):
    die = D100()
    p1, p2 = Pawn(p1_start), Pawn(p2_start)
    p1_turn = True
    while p1.score < 1000 and p2.score < 1000:
        pawn = p1 if p1_turn else p2
        pawn.move(die)
        p1_turn = not p1_turn
    return die.rolled * min(p1.score, p2.score)


@dataclass(unsafe_hash=True)
class QuantumPawn:
    position: int
    score: int = 0

    def move(self, n):
        self.position += n
        while self.position > 10:
            self.position = self.position - 10
        self.score += self.position


def part_two(p1_start, p2_start):
    quant_die = [1, 2, 3]
    games_in_progress = defaultdict(int)
    games_in_progress[(QuantumPawn(p1_start), QuantumPawn(p2_start))] = 1

    quantum_counts = defaultdict(int)
    for rolls in (itertools.product(quant_die, quant_die, quant_die)):
        quantum_counts[sum(rolls)] += 1

    p1_turn = True
    p1_wins, p2_wins = 0, 0
    while games_in_progress:
        temp = defaultdict(int)
        for (p1_pawn, p2_pawn), in_progress_universes in games_in_progress.items():
            if p1_pawn.score > 20:
                p1_wins += in_progress_universes
            elif p2_pawn.score > 20:
                p2_wins += in_progress_universes
            else:
                for n, universe_count in quantum_counts.items():
                    if p1_turn:
                        new_pawn = QuantumPawn(p1_pawn.position, p1_pawn.score)
                        new_pawn.move(n)
                        temp[(new_pawn, p2_pawn)] += in_progress_universes * universe_count
                    else:
                        new_pawn = QuantumPawn(p2_pawn.position, p2_pawn.score)
                        new_pawn.move(n)
                        temp[(p1_pawn, new_pawn)] += in_progress_universes * universe_count

        games_in_progress = temp
        p1_turn = not p1_turn
    return max(p1_wins, p2_wins)


def wins(pawns):
    return sum([v for p, v in pawns.items() if p.score > 20])


"""
Player 1 starting position: 4
Player 2 starting position: 3
"""
if __name__ == "__main__":
    for positions in [(4, 8), (4, 3)]:
        print(part_two(*positions))
