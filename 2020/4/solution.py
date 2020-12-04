import re

HAIR_COLOR_RE = re.compile("^#[0-9a-f]{6}$")


def is_valid_height(s):
    if s[:-2].isdigit() and s.endswith("cm"):
        return 150 <= int(s[:-2]) <= 193
    if s[:-2].isdigit() and s.endswith("in"):
        return 59 <= int(s[:-2]) <= 76
    return False


FIELDS = {
    "byr": lambda x: len(x) == 4 and 1920 <= int(x) <= 2002,
    "iyr": lambda x: len(x) == 4 and 2010 <= int(x) <= 2020,
    "eyr": lambda x: len(x) == 4 and 2020 <= int(x) <= 2030,
    "hgt": lambda x: is_valid_height(x),
    "hcl": lambda x: bool(HAIR_COLOR_RE.match(x)),
    "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda x: len(x) == 9 and x.isdigit()
}
FIELD_KEYS = set(FIELDS.keys())

def part1(passports):
    count = 0
    for passport in passports:
        if FIELD_KEYS.issubset(passport):
            count += 1
    return count


def part2(passports):
    count = 0
    for passport in passports:
        if not FIELD_KEYS.issubset(passport):
            continue
        valid = True
        for k, f in FIELDS.items():
            if not f(passport[k]):
                valid = False
                break
        if valid:
            count += 1
    return count


def accumulate_passports(filename):
    passports = []
    passport = {}
    for line in open(filename):
        line = line.strip()
        if line:
            passport.update([x.split(":") for x in line.split(" ")])
        else:
            passports.append(passport)
            passport = {}

    return passports


if __name__ == "__main__":
    passports = accumulate_passports("input.txt")
    print(part1(passports))
    print(part2(passports))
