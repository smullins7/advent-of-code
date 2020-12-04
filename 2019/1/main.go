package main

import (
	"fmt"
	"io/ioutil"
    "math"
	"strconv"
	"strings"
)

const filename = "./input.txt"

func part1(lines []string) {
	total := 0
	for _, line := range lines {
		total = total + calcFuel(line)
	}

	fmt.Println(total)
}

func part2(lines []string) {
	total := 0
	for _, line := range lines {
        incrementalFuel := calcFuel(line)
        for incrementalFuel > 0 {
		    total = total + incrementalFuel
            incrementalFuel = calcFuel(strconv.Itoa(incrementalFuel))
        }
	}

	fmt.Println(total)
}

func calcFuel(input string) int {
    i, _ := strconv.Atoi(input)
    return int(math.Max(0, float64((i / 3) - 2)))
}

func readFile(filename string) string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Printf("error: %s", err)
	}
	return strings.TrimSpace(string(content))
}

func main() {
	contents := readFile(filename)
	lines := strings.Split(contents, "\n")
	part1(lines)
	part2(lines)
}
