from functools import reduce

from utils.inputs import get_input


def parse_races(data):
    times, distances = data
    return zip([int(t) for t in times.split("Time:")[1].split(" ") if t],
        [int(d) for d in distances.split("Distance:")[1].split(" ") if d])

def parse_race(data):
    times, distances = data
    return (int("".join([t for t in times.split("Time:")[1].split(" ") if t])),
        int("".join([d for d in distances.split("Distance:")[1].split(" ") if d])))

def compute_distance(time_holding_button, total_time_of_race):
    return time_holding_button * (total_time_of_race - time_holding_button)

def possible_times_holding_button(total_time_of_race):
    return range(total_time_of_race)

def part_one(data):
    l = []
    for time, distance in parse_races(data):
        winners = 0
        for time_holding_button in possible_times_holding_button(time):
            if compute_distance(time_holding_button, time) > distance:
                winners += 1
        l.append(winners)

    return reduce(lambda x, y: x * y, l)


def part_two(data):
    time, distance = parse_race(data)
    winners = 0
    for time_holding_button in possible_times_holding_button(time):
        if compute_distance(time_holding_button, time) > distance:
            winners += 1
    return winners

if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")

