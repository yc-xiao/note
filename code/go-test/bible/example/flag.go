package example

import (
	"flag"
	"fmt"
)

// var argx = flag.String("参数字段 method", "默认值 Get", "说明 -method Get/Post")
var argx = flag.String("method", "Get", "method Get/Post")

// TestFlag 测试flag
func TestFlag() {
	flag.Parse()
	fmt.Println("method=", *argx)
}
