from collections import defaultdict
from itertools import product

ACTIVE = "#"
INACTIVE = "."


def get_neighbors(*args):
    l = []
    for a in args:
        l.append([a - 1, a, a + 1])

    return [point for point in product(*l) if point != args]


def run(grid, next_grid):
    for i in range(6):
        #print_grid(grid)
        grid, next_grid = cycle(grid, next_grid)

    return sum(grid.values())


def cycle(grid, next_grid):
    for point in grid:
        cycle_point(grid, next_grid, point)
        for neighbor in get_neighbors(*point):
            cycle_point(grid, next_grid, neighbor)

    return next_grid, grid


def cycle_point(grid, next_grid, point):
    if grid.get(point, False):
        next_grid[point] = 2 <= sum(map(lambda p: grid.get(p, False), get_neighbors(*point))) <= 3
    else:
        next_grid[point] = 3 == sum(map(lambda p: grid.get(p, False), get_neighbors(*point)))


def print_grid(grid):
    by_z = defaultdict(list)
    for (x, y, z), is_active in grid.items():
        by_z[z].append((x, y, ACTIVE if is_active else INACTIVE))

    for z, points in by_z.items():
        print(f"z={z}:")
        by_y = defaultdict(list)
        for (x, y, c) in points:
            by_y[y].append((x, c))

        for y, x_points in by_y.items():
            print("".join([p[1] for p in sorted(x_points, key=lambda x_c: x_c[0])]))


def init_grid(lines, additional_dimensions):
    grid = {}
    for y, line in enumerate(lines):
        for x, state in enumerate(line.strip()):
            point = (x, y)
            for _ in range(additional_dimensions):
                point += (0, )
            grid[point] = state == ACTIVE

    return grid, dict(grid)


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(run(*init_grid(inputs, 1)))
    print(run(*init_grid(inputs, 2)))

