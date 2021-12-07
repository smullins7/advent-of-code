#!/bin/bash

YEAR=$(date +%Y)
DAY=$(date +'%-d')
BASE_DIR=$(dirname "$0")
INPUT_FILE=${BASE_DIR}/${YEAR}/inputs/day-${DAY}-1.txt
PYTHON_FILE=${BASE_DIR}/${YEAR}/day_${DAY}.py

if test -f "${INPUT_FILE}"; then
    echo "${INPUT_FILE} exists, not downloading input data"
else
  # Get today's puzzle input
  curl -s https://adventofcode.com/${YEAR}/day/${DAY}/input --cookie "session=$(cat .session)" -o ${INPUT_FILE}
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


for puzzle in ("sample", 1):
    data = get_input(__file__, puzzle=puzzle, coerce=parse)
    print(f"Part 1: Input {puzzle}, {part_one(data)}")
    print(f"Part 2: Input {puzzle}, {part_two(data)}")

EOT
fi