from collections import defaultdict
from pathlib import Path

from lib_inputs import get_input

CD_CMD = "$ cd "
LS_CMD = "$ ls"
DIR = "dir "


class Filesystem:

    def __init__(self):
        self.current_path = Path("/")
        self.directory = defaultdict(dict)

    def cd(self, target):
        if target == "..":
            self.current_path = self.current_path.parent
        else:
            self.current_path = self.current_path / target

    def ls(self, target):
        if target.startswith(DIR):
            pass
        else:
            size, name = target.split(" ")
            self.directory[self.current_path][name] = int(size)

    def parse(self, text):
        if text.startswith(CD_CMD):
            self.cd(text[len(CD_CMD):])
        elif text != LS_CMD:
            self.ls(text)


def part_one(data):
    f = Filesystem()
    for line in data:
        f.parse(line)

    sizes = defaultdict(int)
    for path in sorted(f.directory, key=lambda p: len(p.parts), reverse=True):
        size = sum(f.directory[path].values())
        sizes[path] += size
        for parent in path.parents:
            sizes[parent] += size
    return sum([size for size in sizes.values() if size <= 100000])


def part_two(data):
    f = Filesystem()
    for line in data:
        f.parse(line)

    sizes = defaultdict(int)
    for path in sorted(f.directory, key=lambda p: len(p.parts), reverse=True):
        size = sum(f.directory[path].values())
        sizes[path] += size
        for parent in path.parents:
            sizes[parent] += size

    total_file_size = 70000000
    update_size = 30000000
    unused_size = total_file_size - sizes[Path("/")]
    for size in sorted(sizes.values()):
        if size + unused_size > update_size:
            return size


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
