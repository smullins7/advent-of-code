from utils.graphs import Grid, Cell
from utils.inputs import get_grids

target = "XMAS"

def is_line(cells: list[Cell]) -> bool:
    x = set([cell.x for cell in cells])
    if len(x) == 1:
        return True
    y = set([cell.y for cell in cells])
    if len(y) == 1:
        return True
    return len(x) == 4 and len(y) == 4

def find_xmas(grid: Grid, cell: Cell, seen: list[Cell], count=0) -> int:
    for neighbor in grid.find_all_neighbors(cell):
        partial = "".join([cell.value for cell in seen]) + neighbor.value
        if not target.startswith(partial):
            continue
        if target == partial and is_line(seen + [neighbor]):
            count += 1
        else:
            count = find_xmas(grid, neighbor, seen + [neighbor], count)

    return count


def part_one(data: Grid):
    total = 0
    for cell in data:
        if cell.value != "X":
            continue
        total += find_xmas(data, cell, [cell])
    return total


def find_x_mas(grid: Grid, a_cell: Cell):
    # 1 2
    #  A
    # 3 4
    diagonals = grid.find_diagonal_neighbors(a_cell)
    if len(diagonals) != 4:
        return False
    m = sum([1 for cell in diagonals if cell.value == "M"])
    s = sum([1 for cell in diagonals if cell.value == "S"])
    return m == 2 and s == 2 and diagonals[0].value != diagonals[-1].value

def part_two(data: Grid):
    total = 0
    for cell in data:
        if cell.value != "A":
            continue
        total += bool(find_x_mas(data, cell))
    return total


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")