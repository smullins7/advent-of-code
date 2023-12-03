#!/bin/bash

DAY=${1:-$(date +'%-d')}
YEAR=${2:-$(date +%Y)}
BASE_DIR=$(dirname "$0")
INPUT_FILE=${BASE_DIR}/${YEAR}/inputs/day-${DAY}.txt
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
  touch ${SAMPLE_FILE}
fi

if test -f "${PYTHON_FILE}"; then
  echo "${PYTHON_FILE} exists, not writing stub python file"
else
  cat <<EOT >> ${PYTHON_FILE}
from utils.inputs import get_input


def part_one(data):
    return 0


def part_two(data):
    return 0


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")

EOT
  chmod +x ${PYTHON_FILE}
fi
