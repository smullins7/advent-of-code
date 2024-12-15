from itertools import chain, pairwise

from utils.graphs import Grid, Cell
from utils.inputs import get_grouped_inputs

def as_grid(grid_lines) -> Grid:
    grid = Grid()
    for y, line in enumerate(grid_lines):
        grid.add_row([Cell(x, y, c) for x, c in enumerate(line.strip())])
    return grid

def find_robot(grid: Grid) -> Cell:
    for cell in grid:
        if cell.value == "@":
            return cell

def part_one(data):
    grid_lines, direction_lines = data
    grid = as_grid(grid_lines)
    robot = find_robot(grid)
    for d in chain.from_iterable(direction_lines):
        neighbor = grid.find_neighbor(robot, d)
        """
        if # then do nothing
        if . then robot is . and neighbor is @ (swap)
        if O (letter) then check its neighbor recursively to find .
        """
        if neighbor.value == "#":
            continue
        if neighbor.value == ".":
            neighbor.value = "@"
            robot.value = "."
            robot = neighbor
        if neighbor.value == "O":
            first_neighbor = neighbor
            while True:
                further_neighbor = grid.find_neighbor(neighbor, d)
                if further_neighbor.value != "O":
                    break
                neighbor = further_neighbor

            if further_neighbor.value == "#":
                continue
            first_neighbor.value = "@"
            robot.value = "."
            robot = first_neighbor
            further_neighbor.value = "O"

    print(grid)

    total = 0
    for cell in grid:
        if cell.value == "O":
            total += cell.y * 100 + cell.x
    return total


expand = {
 "#": "#",
 "O": "]",
 ".": ".",
 "@": ".",
}
def as_grid2(grid_lines) -> Grid:
    grid = Grid()
    for y, line in enumerate(grid_lines):
        x = 0
        row = []
        for c in line.strip():
            row.append(Cell(x, y, "[" if c == "O" else c))
            x += 1
            row.append(Cell(x, y, expand[c]))
            x += 1
        grid.add_row(row)
    return grid

def move_horizontal(to_move: list[Cell]):
    if to_move[0].value != "@" or to_move[-1].value != ".":
        raise Exception(f"invalid moves: {to_move}")
    for dest, source in pairwise(reversed(to_move)):
        dest.value = source.value
    to_move[0].value = "."

def handle_horizontal(grid: Grid, robot: Cell, direction: str) -> Cell:
    neighbor = grid.find_neighbor(robot, direction)
    if neighbor.value == "#":
        return robot
    elif neighbor.value == ".":
        neighbor.value = "@"
        robot.value = "."
        return neighbor
    else: # []
        to_move = [robot, neighbor]
        while True:
            further_neighbor = grid.find_neighbor(neighbor, direction)
            to_move.append(further_neighbor)
            if further_neighbor.value not in ("[", "]"):
                break
            neighbor = further_neighbor

        if further_neighbor.value == "#":
            return robot
        move_horizontal(to_move)
        return to_move[1]


def move_vertical(grid: Grid, cells: list[Cell], direction: str):
    for cell in cells:
        dest = grid.find_neighbor(cell, direction)
        dest.value = cell.value
        cell.value = "."

def to_move_vertical(grid: Grid, robot: Cell, direction: str) -> list[Cell]:
    moves = set()
    todo = [robot]
    while todo:
        cell = todo.pop()
        if cell.value == "#":
            return []
        moves.add(cell)
        neighbor = grid.find_neighbor(cell, direction)
        if neighbor.value == ".":
            continue
        todo.append(neighbor)
        if neighbor.value == "[":
            todo.append(grid.find_neighbor(neighbor, ">"))
        else: # ]
            todo.append(grid.find_neighbor(neighbor, "<"))


    return sorted(moves, key=lambda cell: cell.y, reverse=direction == "v")



def handle_vertical(grid: Grid, robot: Cell, direction: str) -> Cell:
    moves = to_move_vertical(grid, robot, direction)
    if moves:
        move_vertical(grid, moves, direction)
        robot.value = "."
        return grid.find_neighbor(robot, direction)
    else:
        return robot


def part_two(data):
    grid_lines, direction_lines = data
    grid = as_grid2(grid_lines)
    robot = find_robot(grid)

    for d in chain.from_iterable(direction_lines):
        if d in ("<", ">"):
            robot = handle_horizontal(grid, robot, d)
        else:
            robot = handle_vertical(grid, robot, d)

        print(grid)

    total = 0
    for cell in grid:
        if cell.value == "[":
            total += cell.y * 100 + cell.x
    return total


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")