package example

import (
	"testing"
)

// Test_F1_1 测试F1_1函数
func Test_F1_1(t *testing.T) {
	// 白盒测试，记录全局参数args， 在测试结束后通过defer恢复args值
	saved := args
	defer func() { args = saved }()
	args = []string{"test", "a", "b", "c"}
	F1_1()
}

// Test_F1_2 测试F1_2函数
func Test_F1_2(t *testing.T) {
	F1_2()
}

// Benchmark_F1_1 测试F1_1 性能
func Benchmark_F1_1(b *testing.B) {
	for i := 0; i < b.N; i++ {
		F1_1()
	}
}

// Benchmark_F1_2 测试F1_2 性能
func Benchmark_F1_2(b *testing.B) {
	for i := 0; i < b.N; i++ {
		F1_2()
	}
}

// Example_F1_1 测试F1_1 性能
// func Example_F1_1(b *testing.T) {

// }

// Example_F1_2 测试F1_2 性能
// func Example_F1_2(b *testing.B) {

// }
