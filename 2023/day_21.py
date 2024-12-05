from utils.graphs import Grid, Cell
from utils.inputs import get_grids


def find_s(grid: Grid) -> Cell:
    for cell in grid:
        if cell.value == "S":
            return cell


def search(grid: Grid, cell: Cell, seen: dict[Cell, int], steps: int = 0):
    if steps > 64:
        return
    seen[cell] = steps
    for neighbor in grid.find_neighbors(cell):
        if neighbor.value == ".":
            search(grid, neighbor, seen, steps + 1)


def bfs(grid: Grid, start: Cell):
    seen = {}
    q = [(start, 0)]
    while q:
        cell, steps = q.pop(0)
        if steps > 64 or cell in seen:
            continue
        seen[cell] = steps
        for neighbor in grid.find_neighbors(cell):
            if neighbor.value == "." and neighbor not in seen:
                q.append((neighbor, steps + 1))
    return seen


def part_one(grid: Grid):
    start = find_s(grid)
    seen = bfs(grid, start)
    return sum(1 for count in seen.values() if count % 2 == 0)


def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
