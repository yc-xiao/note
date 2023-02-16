package example

import (
	"os"
	"strings"
)

// args 将os.Args变量赋予args，进行白盒测试时可以替换args
var args = os.Args

// F1_1 -
func F1_1() {
	var s, sep string
	for _, v := range args {
		s += sep + v
		sep = " "
	}
}

// F1_2 -
func F1_2() {
	_ = strings.Join(args[1:], " ")
}
