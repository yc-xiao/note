package example

import (
	"fmt"
	"os"
)

// handleError 处理 error
func handleError(err error, s string, raise bool) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s error: %v", s, err)
		if raise {
			os.Exit(1)
		}
	}
}

// handleErrorAndFatal 处理error并中断
func handleErrorAndFatal(e error, s string) {
	handleError(e, s, true)
}

// handleErrorAndFatal 处理error并打印
func handleErrorAndPrint(e error, s string) {
	handleError(e, s, false)
}
