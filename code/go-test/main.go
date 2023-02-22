package main

import (
	"flag"
	_ "yc/go-test/bible/example"
	t "yc/go-test/topgoer/example"
)

var mode = flag.String("mode", "s", "s/c")
var addr = flag.String("addr", "localhost", "ip地址")
var port = flag.String("port", ":8000", "ip端口")

func main() {
	flag.Parse()
	if *mode == "s" {
		t.TCPServer(*addr + *port)
	} else {
		t.TCPClient(*addr + *port)
	}
}
