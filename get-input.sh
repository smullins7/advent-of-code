#!/bin/bash

year=$(date +%Y)
day=$(date +'%-d')
curl -s https://adventofcode.com/${year}/day/${day}/input --cookie "session=$(cat .session)" -o ${year}/inputs/day-${day}-1.txt
