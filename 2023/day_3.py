from collections import defaultdict
from functools import reduce

from utils.graphs import Grid
from utils.inputs import to_grid


def check_is_next_to_symbol(grid, cell):
    for neighbor in grid.find_all_adjacency(cell.x, cell.y):
        if not neighbor.value.isnumeric() and neighbor.value != ".":
            return True
    return False


def part_one(grid: Grid):
    numbers = []
    current_digits = []
    is_next_to_symbol = False
    for row in grid.rows:
        for cell in row:
            if cell.value.isnumeric():
                current_digits.append(cell.value)
                if check_is_next_to_symbol(grid, cell):
                    is_next_to_symbol = True
            else:
                if current_digits:
                    if is_next_to_symbol:
                        numbers.append(int("".join(current_digits)))
                        is_next_to_symbol = False
                        #print(numbers[-1])
                    current_digits = []
    return sum(numbers)


def find_adjacent_gear(grid, cell):
    for neighbor in grid.find_all_adjacency(cell.x, cell.y):
        if neighbor.value == "*":
            return neighbor

def part_two(grid):
    numbers = defaultdict(list)
    current_digits = []
    gear = None
    for row in grid.rows:
        for cell in row:
            if cell.value.isnumeric():
                current_digits.append(cell.value)
                gear = gear or find_adjacent_gear(grid, cell)
            else:
                if current_digits:
                    if gear:
                        numbers[gear].append(int("".join(current_digits)))
                        gear = None
                    current_digits = []
    return sum(map(lambda l: reduce(lambda x, y: x * y, l), filter(lambda l: len(l) == 2, numbers.values())))




if __name__ == "__main__":
    sample_data = to_grid(__file__, coerce=str)
    data = to_grid(__file__, is_sample=False, coerce=str)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__} sample:\n\t{f(data)}") #  526860 too low

