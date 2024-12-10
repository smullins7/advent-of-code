from utils.inputs import get_inputs


def keep_going(exploded: list[str]) -> bool:
    found_blank = False
    for c in exploded:
        if found_blank and c != ".":
            return True
        if c == ".":
            found_blank = True
    return False



def part_one(data):
    exploded = []
    file_id = 0
    is_file = True
    for c in data:
        if is_file:
            exploded.extend([str(file_id)] * int(c))
            file_id += 1
        else:
            exploded.extend(["."] * int(c))
        is_file = not is_file

    print("".join(exploded))
    while keep_going(exploded):
        char = exploded.pop()
        if char == ".":
            continue
        exploded[exploded.index(".")] = char
    print("".join(exploded))
    total = 0
    for i, c in enumerate(exploded):
        total += i * int(c)
    return total


def checksum(start, file_id, length):
    return sum(map(lambda i: i * file_id, range(start, start + length)))


def print_lengths(lengths):
    buf = []
    for file_id, length in lengths:
        buf.extend([str(file_id) * length])
    print("".join(buf))


def combine_free_space(lengths):
    l = []
    for (file_id, length) in lengths:
        if file_id == "." and l[-1][0] == ".":
            l[-1] = ".", l[-1][1] + length
        else:
            l.append((file_id, length))
    return l


def part_two(data):
    lengths = []
    file_id = 0
    is_file = True
    for c in data:
        if is_file:
            lengths.append((int(file_id), int(c)))
            file_id += 1
        else:
            lengths.append((".", int(c)))
        is_file = not is_file


    file_ids = [i for i in lengths if i[0] != "."]
    for to_move_file_id, to_move_length in reversed(file_ids[1:]):
        #print_lengths(lengths)
        for i, (file_id, length) in enumerate(lengths):
            if file_id == "." and to_move_length <= length:
                from_index = lengths.index((to_move_file_id, to_move_length))
                if from_index < i:
                    continue
                lengths[from_index] = (".", to_move_length)
                lengths[i] = (to_move_file_id, to_move_length)
                if to_move_length < length:
                    lengths.insert(i + 1, (".", length - to_move_length))
                break
        lengths = combine_free_space(lengths)
    #print_lengths(lengths)
    index = 0
    total = 0
    for file_id, length in lengths:
        if file_id != ".":
            total += checksum(index, file_id, length)
        index += length
    return total


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")