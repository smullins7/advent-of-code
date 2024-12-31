from collections import defaultdict

from utils.algos import shortest_path
from utils.graphs import Grid
from utils.inputs import get_grids


def part_one_too_slow(grid: Grid):
    """
    find the start and end, run shortest_path to get a baseline
    find all non-border wall pieces that have at least 2 empty neighbors

    iterate through all above wall pieces, where you modify the graph temporarily
    to set that piece to an empty and then call shortest_path again (or modify can_traverse
    to allow for going through the cheat space...) and calculate the savings

    return all savings > 100
    """
    start = grid.find("S")
    end = grid.find("E")
    baseline = len(shortest_path(grid, start, at_end=lambda traveled: traveled == end, can_traverse=lambda node, neighbor, path: neighbor.value != "#")) - 1
    possible_cheats = []
    for cell in grid.find_all_with("#"):
        if sum([1 for neighbor in grid.find_neighbors(cell) if neighbor.value != "#"]) > 1:
            possible_cheats.append(cell)

    print("Checking a total of ", len(possible_cheats), "options for cheating")
    cheats = []
    for i, cheat_cell in enumerate(possible_cheats):
        cheat = len(shortest_path(grid, start, at_end=lambda traveled: traveled == end,
                                     can_traverse=lambda node, neighbor, path: neighbor == cheat_cell or neighbor.value != "#")) - 1
        cheats.append(baseline - cheat)
        if i % 10 == 0:
            print(i)
    return len(cheats), len([1 for cheat_length in cheats if cheat_length >= 100])

def part_one(grid: Grid):
    # use dijkstra from day_16, but change the memo to the cheat cell and the from and to cells
    # but how do we restrict that you can only use one cheat???
    return 0

def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        #print(f"{f.__name__}:\n\t{f(real_data)}")