from collections import defaultdict


def part1(rules, tickets):
    invalid = []
    for ticket in tickets:
        for field in ticket:
            if is_invalid(field, rules):
                invalid.append(field)

    return sum(invalid)


def part2(rules, tickets, your_ticket):
    valid = [your_ticket]
    for ticket in tickets:
        if not any([is_invalid(field, rules) for field in ticket]):
            valid.append(ticket)

    possible = defaultdict(list)
    for field_index in range(len(your_ticket)):
        for field_name, rule in rules.items():
            if all([rule(v) for v in [t[field_index] for t in valid]]):
                possible[field_name].append(field_index)

    known_fields = {}
    while possible:
        for name, possible_indexes in possible.items():
            if len(possible_indexes) == 1:
                known_fields[name] = possible_indexes[0]

        for name in known_fields:
            taken = possible.pop(name, None)
            if taken:
                for s in possible:
                    indexes = possible[s]
                    if taken[0] in indexes:
                        indexes.remove(taken[0])

    return known_fields


def is_invalid(field, rules):
    for field_rules in rules.values():
        if field_rules(field):
            return False
    return True


def parse_input(filename):
    rules, tickets = {}, []
    section = "rules"
    for line in open(filename):
        line = line.strip()
        if not line:
            continue

        if line.startswith("your ticket:"):
            section = "your ticket"
        elif line.startswith("nearby tickets:"):
            section = "tickets"
        elif section == "rules":
            field_name, rule_str = line.split(": ")
            rules[field_name] = to_rule(rule_str)
        elif section == "tickets":
            tickets.append([int(x) for x in line.split(",")])
        elif section == "your ticket":
            your_ticket = [int(x) for x in line.split(",")]

    return rules, tickets, your_ticket


def to_rule(rule_str):
    first, second = rule_str.split(" or ")
    lower, upper = first.split("-")
    first_f = lambda n: int(lower) <= n <= int(upper)
    lower2, upper2 = second.split("-")
    second_f = lambda n: int(lower2) <= n <= int(upper2)

    return lambda n: first_f(n) or second_f(n)


if __name__ == "__main__":
    rules, tickets, your_ticket = parse_input("input.txt")
    print(part1(rules, tickets))
    fields = part2(rules, tickets, your_ticket)

    total = 1
    for name, index in fields.items():
        if name.startswith("departure"):
            total *= your_ticket[index]

    print(total)

