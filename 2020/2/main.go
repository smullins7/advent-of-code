package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"
)

func toi(s string) int {
	i, _ := strconv.Atoi(s)
	return i
}

func part1() {
	contents := readFile("./input.txt")
	lines := strings.Split(contents, "\n")

	//4-5 l: rllllj
	re, _ := regexp.Compile(`^(\d+)-(\d+) (.): (.*)$`)
	total := 0
	for _, line := range lines {
		match := re.FindStringSubmatch(line)
		minChar, maxChar, char, password := match[1], match[2], match[3], match[4]
		count := strings.Count(password, char)
		if (count >= toi(minChar)) && (count <= toi(maxChar)) {
			total += 1
		}
	}
	fmt.Println(total)
}

func part2() {
	contents := readFile("./input.txt")
	lines := strings.Split(contents, "\n")

	//4-5 l: rllllj
	re, _ := regexp.Compile(`^(\d+)-(\d+) (.): (.*)$`)
	total := 0
	for _, line := range lines {
		match := re.FindStringSubmatch(line)
		positionA, positionB, char, password := match[1], match[2], match[3], match[4]

		if (string(password[toi(positionA)-1]) == char) != (string(password[toi(positionB)-1]) == char) {
			total += 1
		}
	}
	fmt.Println(total)
}

func readFile(filename string) string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Printf("error: %s", err)
	}
	return strings.TrimSpace(string(content))
}

func main() {
	part1()
	part2()
}