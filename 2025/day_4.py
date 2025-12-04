from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def part_one(grid: Grid):
    total = 0
    for cell in grid:
        if cell.value == '@' and sum([1 for n in grid.find_all_neighbors(cell) if n.value == '@']) < 4:
            total += 1
    return total


def to_remove(grid: Grid) -> list[Cell]:
    l = []
    for cell in grid:
        if cell.value == '@' and sum([1 for n in grid.find_all_neighbors(cell) if n.value == '@']) < 4:
            l.append(cell)
    return l


def part_two(grid: Grid):
    total = 0
    while True:
        cells = to_remove(grid)
        if not cells:
            break
        for cell in cells:
            cell.value = '.'
        total += len(cells)

    return total


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
