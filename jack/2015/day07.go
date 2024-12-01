package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"log"
	"strconv"
	"strings"
)

// create 2 maps, wire map with values, and if the operation has completed
var wireMap = make(map[string]uint16)
var lineMap = make(map[string]bool)

// Extract operation (AND NOT OR RSHIFT LSHIFT)
// Extract wires or numbers to assign
func extract(s string) (string, []string) {
	var op, res, a1, a2 string

	var n int
	var err error

	n, err = fmt.Sscanf(s, "%s -> %s", &a1, &res)
	if err == nil && n == 2 {
		return "ASSIGN", []string{a1, res}
	}

	n, err = fmt.Sscanf(s, "NOT %s -> %s", &a1, &res)
	if err == nil && n == 2 {
		return "NOT", []string{a1, res}
	}

	n, err = fmt.Sscanf(s, "%s %s %s -> %s", &a1, &op, &a2, &res)
	if err == nil && n == 4 {
		return op, []string{a1, a2, res}
	}

	log.Fatalf("error with %s", s)

	return "", nil
}

func parseNum(s string) uint16 {
	num, err := strconv.ParseUint(s, 10, 16)
	if err != nil {
		log.Fatal(err)
	}
	return uint16(num)
}

// wire can only be used if it has been ASSIGNED a number, i.e is intialized in map. Or is an integer
func canUseInput(m map[string]uint16, ss ...string) bool {
	for _, s := range ss {
		if !keyExists(s, m) && !utils.IsUint(s) {
			return false
		}
	}

	return true
}

func keyExists(s string, m map[string]uint16) bool {
	_, exists := m[s]
	return exists
}

// Operations
func assignment(in, out string, m map[string]uint16) bool {
	if !canUseInput(m, in) {
		return false
	}

	if utils.IsUint(in) {
		m[out] = parseNum(in)
	} else {
		m[out] = m[in]
	}

	return true
}

func not(in, out string, m map[string]uint16) bool {
	if !canUseInput(m, in) {
		return false
	}

	if utils.IsUint(in) {
		m[out] = ^parseNum(in)
	} else {
		m[out] = ^m[in]
	}

	return true
}

func and(in1, in2, out string, m map[string]uint16) bool {
	if !canUseInput(m, in1, in2) {
		return false
	}

	in1Num, in2Num := utils.IsUint(in1), utils.IsUint(in2)

	switch {
	case in1Num && in2Num:
		m[out] = parseNum(in1) & parseNum(in2)
	case in1Num:
		m[out] = parseNum(in1) & m[in2]
	case in2Num:
		m[out] = m[in1] & parseNum(in2)
	default:
		m[out] = m[in1] & m[in2]
	}

	return true
}

func or(in1, in2, out string, m map[string]uint16) bool {
	if !canUseInput(m, in1, in2) {
		return false
	}

	in1Num, in2Num := utils.IsUint(in1), utils.IsUint(in2)

	switch {
	case in1Num && in2Num:
		m[out] = parseNum(in1) | parseNum(in2)
	case in1Num:
		m[out] = parseNum(in1) | m[in2]
	case in2Num:
		m[out] = m[in1] | parseNum(in2)
	default:
		m[out] = m[in1] | m[in2]
	}

	return true
}

func lshift(in, pos, out string, m map[string]uint16) bool {
	if !canUseInput(m, in) {
		return false
	}

	if utils.IsUint(in) {
		m[out] = parseNum(in) << parseNum(pos)
	} else {
		m[out] = m[in] << parseNum(pos)
	}
	return true
}

func rshift(in, pos, out string, m map[string]uint16) bool {
	if !canUseInput(m, in) {
		return false
	}

	if utils.IsUint(in) {
		m[out] = parseNum(in) >> parseNum(pos)
	} else {
		m[out] = m[in] >> parseNum(pos)
	}

	return true
}

func containsFalse() bool {
	for _, value := range lineMap {
		if !value {
			return true
		}
	}
	return false
}
func Day7() {
	fmt.Println("Running day 7...")
	// --- Part 1 ---
	fileAsString := utils.FileAsString("./data/day07.txt")
	stringArr := strings.Split(fileAsString, "\n")

	for i := range stringArr {
		lineMap[stringArr[i]] = false
	}

	for containsFalse() {
		for i := range stringArr {
			op, wires := extract(stringArr[i])
			switch op {
			case "ASSIGN":
				if assignment(wires[0], wires[1], wireMap) {
					lineMap[stringArr[i]] = true
				}
			case "NOT":
				if not(wires[0], wires[1], wireMap) {
					lineMap[stringArr[i]] = true
				}
			case "AND":
				if and(wires[0], wires[1], wires[2], wireMap) {
					lineMap[stringArr[i]] = true
				}
			case "OR":
				if or(wires[0], wires[1], wires[2], wireMap) {
					lineMap[stringArr[i]] = true
				}
			case "LSHIFT":
				if lshift(wires[0], wires[1], wires[2], wireMap) {
					lineMap[stringArr[i]] = true
				}
			case "RSHIFT":
				if rshift(wires[0], wires[1], wires[2], wireMap) {
					lineMap[stringArr[i]] = true
				}
			}
		}
	}
	fmt.Println("--- Part 1 ---")
	fmt.Println("Answer: ", wireMap["a"])

	// --- Part 2 ---
	var newWireMap = make(map[string]uint16)
	newWireMap["b"] = wireMap["a"]
	for i := range stringArr {
		lineMap[stringArr[i]] = false
	}

	for containsFalse() {
		for i := range stringArr {
			op, wires := extract(stringArr[i])

			if op == "ASSIGN" && wires[1] == "b" {
				lineMap[stringArr[i]] = true
				continue
			}

			switch op {
			case "ASSIGN":
				if assignment(wires[0], wires[1], newWireMap) {
					lineMap[stringArr[i]] = true
				}
			case "NOT":
				if not(wires[0], wires[1], newWireMap) {
					lineMap[stringArr[i]] = true
				}
			case "AND":
				if and(wires[0], wires[1], wires[2], newWireMap) {
					lineMap[stringArr[i]] = true
				}
			case "OR":
				if or(wires[0], wires[1], wires[2], newWireMap) {
					lineMap[stringArr[i]] = true
				}
			case "LSHIFT":
				if lshift(wires[0], wires[1], wires[2], newWireMap) {
					lineMap[stringArr[i]] = true
				}
			case "RSHIFT":
				if rshift(wires[0], wires[1], wires[2], newWireMap) {
					lineMap[stringArr[i]] = true
				}
			}
		}
	}
	fmt.Println("--- Part 2 ---")
	fmt.Println("Answer: ", newWireMap["a"])

}
