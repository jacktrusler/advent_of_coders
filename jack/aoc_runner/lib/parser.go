package lib

import "strconv"

type Parser struct {
	Err error
}

func (p *Parser) Atoi(s string) int {
	if p.Err != nil {
		return 0
	}
	n, err := strconv.Atoi(s)
	if err != nil {
		p.Err = err
	}
	return n
}
