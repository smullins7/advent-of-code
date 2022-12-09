from lib_inputs import get_input


def to_grid(data):
    grid = []
    for y, line in enumerate(data):
        grid.append([])
        for c in line:
            grid[y].append(int(c))

    return grid


def check_visibility(grid, x, y, v):
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    if x == 0 or y == 0 or x == max_x or y == max_y:
        return True
    # check up
    if all(grid[y_prime][x] < v for y_prime in range(y)):
        return True

    # check down
    if all(grid[y_prime][x] < v for y_prime in range(y + 1, max_y + 1)):
        return True

    # check left
    if all(grid[y][x_prime] < v for x_prime in range(x)):
        return True

    # check right
    if all(grid[y][x_prime] < v for x_prime in range(x + 1, max_x + 1)):
        return True

    return False


def calc_score(grid, x, y, v):
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1

    if x == 0 or y == 0 or x == max_x or y == max_y:
        return 0

    up_score = 0
    for y_prime in reversed(range(y)):
        up_score += 1
        if grid[y_prime][x] >= v:
            break

    down_score = 0
    for y_prime in range(y + 1, max_y + 1):
        down_score += 1
        if grid[y_prime][x] >= v:
            break

    left_score = 0
    for x_prime in reversed(range(x)):
        left_score += 1
        if grid[y][x_prime] >= v:
            break

    right_score = 0
    for x_prime in range(x + 1, max_x + 1):
        right_score += 1
        if grid[y][x_prime] >= v:
            break

    return up_score * down_score * left_score * right_score


def part_one(data):
    grid = to_grid(data)
    visible = 0
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            visible += int(check_visibility(grid, x, y, v))
    return visible


def part_two(data):
    grid = to_grid(data)
    max_score = 0
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            score = calc_score(grid, x, y, v)
            max_score = max(score, max_score)
    return max_score


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")

