from utils.graphs import Grid, Cell
from utils.inputs import to_grid


def check_visibility(grid: Grid, cell: Cell):
    x, y, v = cell.x, cell.y, cell.value
    if grid.is_on_border(cell):
        return True
    # check up
    if all(cell.value < v for cell in grid.walk_up(cell)):
        return True

    # check down
    if all(cell.value < v for cell in grid.walk_down(cell)):
        return True

    # check left
    if all(cell.value < v for cell in grid.walk_left(cell)):
        return True

    # check right
    if all(cell.value < v for cell in grid.walk_right(cell)):
        return True

    return False


def calc_score(grid: Grid, cell: Cell):
    if grid.is_on_border(cell):
        return 0

    up_score = 0
    for other_cell in grid.walk_up(cell):
        up_score += 1
        if other_cell.value >= cell.value:
            break

    down_score = 0
    for other_cell in grid.walk_down(cell):
        down_score += 1
        if other_cell.value >= cell.value:
            break

    left_score = 0
    for other_cell in grid.walk_left(cell):
        left_score += 1
        if other_cell.value >= cell.value:
            break

    right_score = 0
    for other_cell in grid.walk_right(cell):
        right_score += 1
        if other_cell.value >= cell.value:
            break

    return up_score * down_score * left_score * right_score


def part_one(grid: Grid):
    visible = 0
    for cell in grid:
            visible += int(check_visibility(grid, cell))
    return visible


def part_two(grid: Grid):
    max_score = 0
    for cell in grid:
        score = calc_score(grid, cell)
        max_score = max(score, max_score)
    return max_score


if __name__ == "__main__":
    for f in (part_one, part_two):
        grid = to_grid(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(grid)}")

