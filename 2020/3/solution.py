import math


def traverse(grid, right, down):
    position_x = 0
    position_y = 0
    trees = 0
    while position_y + down < len(grid):
        position_x = (position_x + right) % len(grid[position_y])
        position_y = position_y + down
        if grid[position_y][position_x] == "#":
            trees += 1
    return trees


def part1(inputs):
    print(traverse(inputs, 3, 1))


def part2(inputs):
    print(math.prod([traverse(inputs, *slopes) for slopes in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]]))


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    part1(inputs)
    part2(inputs)
