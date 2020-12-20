import re

CAN_REPLACE = re.compile("^\D+$")


def run(rules, messages):
    regex = re.compile(f"^({to_regex(rules)})$")
    for m in messages:
        if regex.match(m) is not None:
            print(m)
    return sum([regex.match(message) is not None for message in messages])


def parse(filename):
    mode = "rules"
    rules = {}
    messages = []
    for line in open(filename):
        line = line.strip()
        if not line:
            mode = "messages"
            continue
        if mode == "rules":
            rule_id, rule_s = line.split(": ")
            rule_id = f"_{rule_id}_"
            if rule_s.startswith('"'):
                rules[rule_id] = rule_s[1]
            else:
                replaced = re.sub("(\d+)", r"_\1_", rule_s).replace(" ", "")
                if rule_id == "_8_":
                    replaced = "_42_+"
                elif rule_id == "_11_":
                    # it's a total hack but i don't care
                    replaced = "(_42__31_|_42__42__31__31_|_42__42__42__31__31__31_|_42__42__42__42__31__31__31__31_)"
                elif "|" in replaced:
                    left, right = replaced.split("|")
                    replaced = f"({left}|{right})"
                rules[rule_id] = replaced
        elif mode == "messages":
            messages.append(line)

    return rules, messages


def to_regex(rules):
    while len(rules) > 1:
        replace = {}
        for rule_id, rule_s in rules.items():
            if rule_s.isalpha():
                replace[rule_id] = rule_s
                continue
            match = CAN_REPLACE.match(rule_s)
            if match:
                replace[rule_id] = f"{rule_s}"

        for replace_id, replace_value in replace.items():
            for rule_id, rule_s in rules.items():
                rules[rule_id] = rule_s.replace(replace_id, replace_value)
            rules.pop(replace_id)

    return list(rules.values())[0]


if __name__ == "__main__":
    rules, messages = parse("input")
    print(run(rules, messages)) #220 too low 245 too high
