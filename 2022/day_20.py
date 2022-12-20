from dataclasses import dataclass
from typing import List
import uuid
from utils.inputs import get_input


def parse(value):
    return Num(uuid.uuid4(), int(value))


@dataclass
class Num:
    uuid: uuid.UUID
    value: int
    moved: bool = False


def part_one(data: List[Num]):
    length = len(data)
    cursor = 0
    for item in data[:]:
        while data[cursor].moved:
            cursor += 1
        if abs(item.value % (length - 1)) not in (0, length - 1) and not item.moved:
            new_index = (cursor + item.value) % (length - 1)
            data.pop(cursor)
            item.moved = True
            data.insert(new_index, item)
            # we moved the item "behind" the cursor so we need to advance the cursor
            if new_index < cursor:
                cursor += 1
        else:
            cursor += 1

    return coordinates(data)


def part_two(data: List[Num]):
    length = len(data)
    decryption_key = 811589153
    decrypted_data = [Num(n.uuid, n.value * decryption_key) for n in data]
    frozen_order = [Num(n.uuid, n.value) for n in decrypted_data]
    for _ in range(10):
        print("mixing")
        for frozen_num in frozen_order:
            index, decrypted_num = find(decrypted_data, frozen_num.uuid)
            new_index = (index + decrypted_num.value) % (length - 1)
            if new_index == index:
                continue
            decrypted_data.pop(index)
            decrypted_data.insert(new_index, decrypted_num)

    return coordinates(decrypted_data)


def find(list_of_num: List[Num], uuid_n: uuid.UUID):
    for index, num in enumerate(list_of_num):
        if num.uuid == uuid_n:
            return index, num


def coordinates(data):
    length = len(data)
    zero_index = None
    for i, n in enumerate(data):
        if n.value == 0:
            zero_index = i

    return sum([
        data[(zero_index + (1000 % length)) % length].value,
        data[(zero_index + (2000 % length)) % length].value,
        data[(zero_index + (3000 % length)) % length].value
    ])


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")
