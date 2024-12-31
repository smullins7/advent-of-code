from utils.graphs import Grid, Cell
from utils.inputs import get_grids

def find_track(grid: Grid) -> dict[Cell, int]:
    cell = grid.find("S")
    track = {
        cell: 0
    }
    distance = 1
    while cell.value != "E":
        for neighbor in grid.find_neighbors(cell):
            if not neighbor in track and neighbor.value != "#":
                track[neighbor] = distance + 1
                distance += 1
                cell = neighbor
                break
    return track



def part_one(grid: Grid):
    """
    learn to read the problem better...
    this is not a maze/path finding problem, this is only one direct path from S to E and it's literally all
    the "." spaces in the grid

    so if we have the set of "." cells, then every possible cheat is just a neighbor whose value is "#",
    not on the border, and who has a neighbor that is also on the track. So all I need to do is throw all
    the track cells into a set, then iterate through them from S to E and check all those "#" neighbors,
    but I need the score somehow, oh the score is the index of the track cell
    """
    track = find_track(grid)
    print("found track", len(track))
    cheats = 0
    for cell in track:
        for neighbor in grid.find_neighbors(cell):
            if neighbor.value == "#" and not grid.is_on_border(neighbor):
                # possible cheat, need to see if one of this neighbor's neighbor is on track and not cell
                direction = cell.get_direction(neighbor)
                reenter_cell = grid.find_neighbor(neighbor, direction)
                if reenter_cell in track: # this is a cheat
                    savings = track[reenter_cell] - track[cell] - 2 # for moving through the cheat wall
                    if savings >= 100:
                        cheats += 1

    return cheats


def find_within(grid: Grid, start: Cell, track: dict[Cell, int]) -> int:
    seen = set()
    q = [start]
    while q:
        cell = q.pop(0)
        for neighbor in grid.find_neighbors(cell):
            if neighbor not in seen and start.get_distance(neighbor) <= 20:
                seen.add(neighbor)
                q.append(neighbor)

    cheats = 0
    for cell in seen:
        if cell not in track:
            continue
        savings = track[cell] - track[start] - start.get_distance(cell)
        if savings >= 100:
            cheats += 1
    return cheats

def part_two(grid: Grid):
    """
    i think the key is that a cheat is defined by its start and end position, not by the path that it takes,
    so i could take all possible beginning/end positions for cheats and then whittle them down...but that's a
    crazy big space to iterate through. I could iterate through the track and only look for all positions that
    are within 20 spaces
    """
    track = find_track(grid)
    cheats = 0
    for cell in track:
        cheats += find_within(grid, cell, track)
    return cheats


if __name__ == "__main__":
    sample_data, real_data = get_grids(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")