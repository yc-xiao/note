package example

import (
	"testing"
)

var addr = "127.0.0.1:39999"

func TestMain(m *testing.M) {
	go Service(addr)
	m.Run()
}

// TestRequests go test -v -run=Request ./example/.
func TestRequests(t *testing.T) {
	urls := []string{}
	for i := 0; i < 10; i++ {
		urls = append(urls, "http://"+addr+"/?aa=1")
	}
	urls = append(urls, "http://"+addr+"/count")
	Requests(urls)
}

// BenchmarkRequests go test -v -run=TestMain -bench=Request ./example/.
func BenchmarkRequests(b *testing.B) {
	for i := 0; i <= b.N; i++ {
		TestRequests(&testing.T{})
	}
}
