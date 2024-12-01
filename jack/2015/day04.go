package main

import (
	"crypto/md5"
	"fmt"
	"strconv"
	"strings"
)

func Day4() {
	fmt.Println("Running day 4...")
	// secret key
	input := "bgvyzdsv"

	// find the nonce that produces hex with leading zeros 0x000...
	found5 := false
	i := 0
	for {
		strI := strconv.Itoa(i)
		data := []byte(input + strI)
		str := fmt.Sprintf("%x", md5.Sum(data))
		// Part 1 - 5 leading zeros
		if !found5 && strings.HasPrefix(str, "00000") {
			fmt.Println(str, "Part 1 Index", i)
			found5 = true
		}
		// Part 2 - 6 leading zeros
		if strings.HasPrefix(str, "000000") {
			fmt.Println(str, "Part 2 Index", i)
			break
		}
		i++
	}
}
