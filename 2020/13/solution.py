from functools import reduce

def part1(wait_time, buses):
    min_time = 0
    target = None
    for bus in [int(bus) for bus in buses.split(",") if bus != "x"]:
        bus_time = bus - wait_time % bus
        if not min_time or bus_time < min_time:
            target = bus
            min_time = bus_time

    return target * min_time


def part2_too_slow(buses):
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


# copied off the interwebs...
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def part2(buses):
    bus_offsets = [(i, int(bus)) for (i, bus) in enumerate(buses.split(",")) if bus != "x"]
    remainders = [0 if offset == 0 else -offset % bus_id for offset, bus_id in bus_offsets]

    return chinese_remainder([x[1] for x in bus_offsets], remainders)

if __name__ == "__main__":
    wait_time, buses = [line.strip() for line in open("./input.txt")]
    print(part1(int(wait_time), buses))
    print(part2(buses)) #266204454441577
