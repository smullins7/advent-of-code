def get_input(day, puzzle=1, coerce=str):
    return [coerce(x.strip()) for x in open(f"./inputs/day-{day}-{puzzle}.txt").readlines()]
