import os
import re
from datetime import datetime
from pathlib import Path

from utils.binary import c_to_b
from utils.graphs import SparseGrid, Grid, Node, Cell, SparseValueGrid

DAY_RE = re.compile(r"^.*/day_(\d+)\.py$")
BASE_PATH = Path(os.path.dirname(__file__)).parent


def day_filename(filename, is_sample):
    return f"{BASE_PATH}/{datetime.today().year}/inputs/day-{DAY_RE.match(filename).group(1)}{'-sample' if is_sample else ''}.txt"


def get_input(filename, is_sample=True, coerce=str):
    parsed = [coerce(x.rstrip()) for x in open(day_filename(filename, is_sample)).readlines()]
    # some puzzle inputs are only a single line and meant to be split on some delimiter
    return parsed if len(parsed) > 1 else parsed[0]


def get_grouped_input(filename, is_sample=True, coerce=str):
    """Puzzle input grouped by empty lines, e.g.:
      foo
      bar

      baz
    would yield [[foo, bar], [baz]]
    """
    groups = []
    group = []
    for x in open(day_filename(filename, is_sample)).readlines():
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


def to_grid(filename, is_sample=True, coerce=int) -> Grid:
    grid = Grid([])
    for y, line in enumerate(open(day_filename(filename, is_sample)).readlines()):
        grid.rows.append([Cell(x, y, coerce(c)) for x, c in enumerate(line.strip())])
    return grid


def to_sparse_grid(filename, puzzle=1):
    grid = SparseValueGrid({})
    for y, line in enumerate(open(day_filename(filename, puzzle)).readlines()):
        for x, c in enumerate(line.strip()):
            grid.set(x, y, c)
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
