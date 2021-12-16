#!/bin/bash

YEAR=$(date +%Y)
DAY=$(date +'%-d')
BASE_DIR=$(dirname "$0")
INPUT_FILE=${BASE_DIR}/${YEAR}/inputs/day-${DAY}-1.txt
SAMPLE_FILE=${BASE_DIR}/${YEAR}/inputs/day-${DAY}-sample.txt
PYTHON_FILE=${BASE_DIR}/${YEAR}/day_${DAY}.py

if test -f "${INPUT_FILE}"; then
    echo "${INPUT_FILE} exists, not downloading input data"
else
  # Get today's puzzle input
  curl -s https://adventofcode.com/${YEAR}/day/${DAY}/input --cookie "session=$(cat .session)" -o ${INPUT_FILE}
fi

if test -f "${SAMPLE_FILE}"; then
    echo "${SAMPLE_FILE} exists, not touching"
else
  touch ${INPUT_FILE}
fi

if test -f "${PYTHON_FILE}"; then
  echo "${PYTHON_FILE} exists, not writing stub python file"
else
  cat <<EOT >> ${PYTHON_FILE}
#!/usr/bin/env python3

from lib_inputs import get_input


def parse(line):
    return str(line)


def part_one(data):
    return 0


def part_two(data):
    return 0


if __name__ == "__main__":
    for puzzle in ("sample", 1):
        for f in (part_one, part_two):
            data = get_input(__file__, puzzle=puzzle, coerce=parse)
            print(f"{f.__name__}: Input {puzzle}, {f(data)}")

EOT
  chmod +x ${PYTHON_FILE}
fi