import os
import re

DAY_RE = re.compile(r"^.*/day_(\d+)\.py$")
BASE_PATH = os.path.dirname(__file__)


def get_input(filename, puzzle=1, coerce=str):
    parsed = [coerce(x.strip()) for x in open(f"{BASE_PATH}/inputs/day-{DAY_RE.match(filename).group(1)}-{puzzle}.txt").readlines()]
    # some puzzle inputs are only a single line and meant to be split on some delimiter
    return parsed if len(parsed) > 1 else parsed[0]
