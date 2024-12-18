from utils.graphs import SparseGrid
from utils.inputs import get_inputs

def shortest_path(grid: SparseGrid, start: tuple[int,int], end: tuple[int,int]):
    explored = []

    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            x, y = node
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            for neighbor in neighbors:
                nx, ny = neighbor
                if neighbor not in explored and not grid.has(nx, ny) and 0 <= nx <= grid.max_x and 0 <= ny <= grid.max_y:
                    new_path = list(path) + [neighbor]
                    queue.append(new_path)

                    if neighbor == end:
                        return new_path
            explored.append(node)

def part_one(data, limit):
    grid = SparseGrid()
    grid.min_x = 0
    grid.min_y = 0
    for line in data[:limit]:
        x, y = line.split(",")
        grid.set(int(x), int(y))

    start = 0, 0
    end = grid.max_x, grid.max_y
    print(grid)
    return len(shortest_path(grid, start, end)) - 1


def can_do(data, limit):
    grid = SparseGrid()
    grid.min_x = 0
    grid.min_y = 0
    for line in data[:limit]:
        x, y = line.split(",")
        grid.set(int(x), int(y))

    start = 0, 0
    end = grid.max_x, grid.max_y
    return shortest_path(grid, start, end)

def part_two(data, limit):
    path = set(can_do(data, limit))
    while True:
        next_x, next_y = [int(n) for n in data[limit].split(",")]
        limit += 1
        if (next_x, next_y) not in path:
            continue
        path = can_do(data, limit)
        if not path:
            break
        path = set(path)

    return limit, data[limit] # off by one just look in the input file


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data, 12)}")
        print(f"{f.__name__}:\n\t{f(real_data, 1024)}")