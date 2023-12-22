import re
from pathlib import Path

from utils.binary import c_to_b
from utils.graphs import Grid, Node, Cell, SparseValueGrid, SparseGrid

DAY_RE = re.compile(r"^.*day_(\d+)\.py$")


def day_filename(filename: Path, is_sample):
    return filename.parent / "inputs" / f"day-{DAY_RE.match(filename.name).group(1)}{'-sample' if is_sample else ''}.txt"


def get_input(filename: str, is_sample=True, coerce=str):
    parsed = [coerce(x.rstrip()) for x in open(day_filename(Path(filename), is_sample)).readlines()]
    # some puzzle inputs are only a single line and meant to be split on some delimiter
    return parsed if len(parsed) > 1 else parsed[0]


def get_inputs(filename: str, coerce=str):
    return get_input(filename, True, coerce), get_input(filename, False, coerce)


def get_grouped_inputs(filename: str, coerce=str):
    return get_grouped_input(filename, True, coerce), get_grouped_input(filename, False, coerce)

def get_grouped_input(filename, is_sample=True, coerce=str):
    """Puzzle input grouped by empty lines, e.g.:
      foo
      bar

      baz
    would yield [[foo, bar], [baz]]
    """
    groups = []
    group = []
    for x in open(day_filename(Path(filename), is_sample)).readlines():
        x = x.rstrip()
        if not x:
            groups.append(group)
            group = []
        else:
            group.append(coerce(x))
    if group:
        groups.append(group)
    return groups


def input_to_binary(filename, puzzle=1):
    return "".join([c_to_b(c) for c in open(day_filename(filename, puzzle)).readline().strip()])


def get_grids(filename: str, coerce=str):
    return to_grid(filename, True, coerce), to_grid(filename, False, coerce)
def to_grid(filename, is_sample=True, coerce=int) -> Grid:
    grid = Grid()
    for y, line in enumerate(open(day_filename(Path(filename), is_sample)).readlines()):
        grid.add_row([Cell(x, y, coerce(c)) for x, c in enumerate(line.strip())])
    return grid


def to_sparse_grid(filename, is_sample=True):
    """
    Parse input that assumes a grid format where "." denotes no value and any other character denotes some presence on the grid.
    This assumes there is only one kind of non-period character on the grid. Do not use this for puzzles that would have
    multiple different characters!

    Also, assumes the x, y coordinates are meant to match an actual grid so y will be at most 0
    """
    grid = SparseGrid()
    for y, line in enumerate(open(day_filename(Path(filename), is_sample)).readlines()):
        for x, c in enumerate(line.strip()):
            if c == ".":
                continue
            grid.set(x, -y)
    return grid


def to_nodes(filename, puzzle=1) -> Node:
    nodes = {}

    def _get(value) -> Node:
        if value not in nodes:
            nodes[value] = Node.from_value(value)
        return nodes[value]

    for line in open(day_filename(filename, puzzle)).readlines():
        left, right = line.strip().split("-")
        left_node = _get(left)
        right_node = _get(right)
        left_node.add_path(right_node)
    return nodes["start"]
