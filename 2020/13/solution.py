def part1(wait_time, buses):
    min_time = 0
    target = None
    for bus in [int(bus) for bus in buses.split(",") if bus != "x"]:
        bus_time = bus - wait_time % bus
        if not min_time or bus_time < min_time:
            target = bus
            min_time = bus_time

    return target * min_time


def part2_slow(buses):
    bus_offsets = [(i, int(bus)) for (i, bus) in enumerate(buses.split(",")) if bus != "x"]
    time_offset, slowest_bus_id = max(bus_offsets, key=lambda x: x[1])
    other_buses = [(bus[0] - time_offset, bus[1]) for bus in bus_offsets if bus != (time_offset, slowest_bus_id)]
    # find max one
    step = 0
    while True:
        step += 1
        v = step * slowest_bus_id
        viable = True
        for offset, id in other_buses:
            if (v % id + offset) % id != 0:
                viable = False
                break

        if viable:
            return v - time_offset


def lcm_with_offset(bus_one, bus_two):
    step = 0
    while True:
        step += 1
        v = step * bus_one[1]
        if v + bus_two[0] % bus_two[1] == 0:
            return v - bus_one[0]

if __name__ == "__main__":
    wait_time, buses = [line.strip() for line in open("./example.txt")]
    print(part1(int(wait_time), buses))
    print(part2(buses))

