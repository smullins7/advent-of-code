def next_speak(spoken, to_speak, turn):
    if to_speak not in spoken:
        return 0

    return turn - spoken[to_speak]


def part1(line):
    starting_numbers = [int(n) for n in line.split(",")]
    spoken = {}
    for turn_number in range(1, 2021):
        if starting_numbers:
            speak = starting_numbers.pop(0)
            next = next_speak(spoken, speak, turn_number)
            spoken[speak] = turn_number
            continue

        speak = next
        next = next_speak(spoken, speak, turn_number)
        spoken[speak] = turn_number

    return speak


def part2(line):
    starting_numbers = [int(n) for n in line.split(",")]
    spoken = {}
    for turn_number in range(1, 30000001):
        if starting_numbers:
            speak = starting_numbers.pop(0)
            next = next_speak(spoken, speak, turn_number)
            spoken[speak] = turn_number
            continue

        speak = next
        next = next_speak(spoken, speak, turn_number)
        spoken[speak] = turn_number

    return speak


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./example.txt")]
    #print(part1(inputs[0]))
    print(part2(inputs[0]))

