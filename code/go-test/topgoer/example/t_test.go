package example

import "testing"

// TestTestTopgoer
// go test ./topgoer/...
func TestExTopgoer(t *testing.T) {
	ExTopgoer()
}

// BenchmarkTestTopgoer
// go test ./topgoer/... -v -bench=BenchmarkTestTopgoer
func BenchmarkExTopgoer(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ExTopgoer()
	}
}
