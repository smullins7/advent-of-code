import sys
from collections import defaultdict
from queue import PriorityQueue

from utils.graphs import Grid, Cell
from utils.inputs import get_grids

turns = {
    "R": ("U", "D"),
    "L": ("U", "D"),
    "U": ("L", "R"),
    "D": ("L", "R"),
}

def dijkstra(grid: Grid):
    start = find(grid, "S")
    memo = defaultdict(lambda: sys.maxsize)

    que = PriorityQueue()
    que.put((0, start, "R"))
    que.put((1000, start, "U"))

    while not que.empty():
        score, cell, direction = que.get()
        if score > memo[(cell, direction)] or cell.value == "E":
            continue

        # add neighbors and directions only for "forward" progress not in #
        step_neighbor = grid.find_neighbor(cell, direction)
        if step_neighbor.value != "#":
            new_score = score + 1
            if new_score < memo[(step_neighbor, direction)]:
                memo[(step_neighbor, direction)] = new_score
                que.put((new_score, step_neighbor, direction))

        # and turn neighbors
        for turn_direction in turns[direction]:
            turn_neighbor = grid.find_neighbor(cell, turn_direction)
            if turn_neighbor.value != "#":
                new_score = score + 1001
                if new_score < memo[(turn_neighbor, turn_direction)]:
                    memo[(turn_neighbor, turn_direction)] = new_score
                    que.put((new_score, turn_neighbor, turn_direction))


    best = sys.maxsize
    for (cell, direction), score in memo.items():
        if cell.value == "E":
            best = min(best, score)
    return best, memo

def find(grid: Grid, target: str) -> Cell:
    for cell in grid:
        if cell.value == target:
            return cell


def part_one(grid: Grid):
    return dijkstra(grid)[0]


backup = {
    "R": "L",
    "L": "R",
    "U": "D",
    "D": "U",
}

def find_ends(best: int, memo: dict[tuple[Cell, str], int]) -> list[tuple[Cell, str]]:
    for (cell, direction), score in memo.items():
        if cell.value == "E" and score == best:
            yield cell, direction, score

def part_two(grid: Grid):
    best, memo = dijkstra(grid)

    seats = set()
    todo = []
    todo.extend(find_ends(best, memo))
    while todo:
        cell, direction, max_score = todo.pop()

        seats.add(cell)
        prev = grid.find_neighbor(cell, backup[direction])
        for possible_direction in backup.keys():
            prev_score = memo[(prev, possible_direction)]
            if possible_direction == backup[direction] or prev_score > max_score:
                continue
            todo.append((prev, possible_direction, prev_score))

    return len(seats) + 1


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")