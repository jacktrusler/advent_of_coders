package goutils

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

const SessionCookie = "53616c7465645f5fa71e19a254583d19eb10c409743c00a0bdeed4395a6e99f655f01cf7ff873eeeb51bb93d3e604420d4822d66a92b0c2eaf718c6bd8696da9"

func FileAsString(file string) string {
	content, err := os.ReadFile(file)
	if err != nil {
		log.Fatal(err)
	}

	fileAsString := string(content)
	fileAsString = strings.TrimSuffix(fileAsString, "\n")
	return fileAsString
}

func FetchInput(year, day, session string) {
	url := fmt.Sprintf("https://www.adventofcode.com/%s/day/%s/input", year, day)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	cookies := []*http.Cookie{
		{Name: "session", Value: SessionCookie},
	}
	for _, cookie := range cookies {
		req.AddCookie(cookie)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	var bodyString string
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Println("Error reading body: ", err)
			return
		}

		bodyString = string(bodyBytes)
	}

	fmt.Println("Status code:", resp.StatusCode)
	fmt.Println(bodyString)

}
