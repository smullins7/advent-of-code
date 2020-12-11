def adjacent_seats(grid, x, y):
    adjacent = []
    if x > 0:
        adjacent.append(grid[x-1][y])

    if x > 0 and y > 0:
        adjacent.append(grid[x - 1][y-1])

    if y > 0:
        adjacent.append(grid[x][y-1])

    if x < len(grid) - 1 and y > 0:
        adjacent.append(grid[x + 1][y - 1])

    if x < len(grid) - 1:
        adjacent.append(grid[x + 1][y])

    if y < len(grid[x]) - 1:
        adjacent.append(grid[x][y + 1])

    if x > 0 and y < len(grid[x]) - 1:
        adjacent.append(grid[x - 1][y + 1])

    if x < len(grid) - 1 and y < len(grid[x]) - 1:
        adjacent.append(grid[x + 1][y + 1])

    return filter(lambda s: s != ".", adjacent)


def new_value(grid, x, y):
    if grid[x][y] == ".":
        return "."
    if grid[x][y] == "L":
        return "#" if all([x == "L" for x in adjacent_seats(grid, x, y)]) else "L"

    return "L" if sum([x == "#" for x in adjacent_seats(grid, x, y)]) >= 4 else "#"


def part1(inputs):
    next = [[c for c in row] for row in inputs]

    while run(inputs, next):
        inputs, next = next, inputs

    total = 0
    for r in next:
        for s in r:
            if s == "#":
                total += 1
    return total


def run(current, next):
    changed = False
    for x, row in enumerate(current):
        for y, position in enumerate(row):
            next[x][y] = new_value(current, x, y)
            if not changed and next[x][y] != current[x][y]:
                changed = True

    return changed


def run2(current, next):
    changed = False
    for x, row in enumerate(current):
        for y, position in enumerate(row):
            next[x][y] = new_value2(current, x, y)
            if not changed and next[x][y] != current[x][y]:
                changed = True

    return changed


def new_value2(grid, x, y):
    if grid[x][y] == ".":
        return "."
    if grid[x][y] == "L":
        return "L" if any([found(grid, x, y, xs, ys, "#") for xs, ys in STEPS]) else "#"

    return "L" if len(list(filter(lambda b: b, [found(grid, x, y, xs, ys, "#") for xs, ys in STEPS]))) >= 5 else "#"


def part2(inputs):
    next = [[c for c in row] for row in inputs]

    while run2(inputs, next):
        inputs, next = next, inputs

    total = 0
    for r in next:
        for s in r:
            if s == "#":
                total += 1
    return total


def found(grid, xstart, ystart, xstep, ystep, target):
    x, y = xstart, ystart

    x += xstep
    y += ystep
    while 0 <= x < len(grid) and 0 <= y < len(grid[x]):
        if grid[x][y] == target:
            return True
        elif grid[x][y] != ".":
            return False
        x += xstep
        y += ystep

    return False


STEPS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]

if __name__ == "__main__":
    inputs = [[c for c in line.strip()] for line in open("./input.txt")]
    #rint(part1(inputs))
    print(part2(inputs))

