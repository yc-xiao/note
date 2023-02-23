package example

import (
	"context"
	"fmt"
	"time"
)

var dms = 10 * time.Microsecond

func worker(ctx context.Context, name string) {
	defer fmt.Println("end", name)
	fmt.Println("start", name)
	for {
		select {
		case <-ctx.Done():
			break
		default:
			go worker(ctx, name)
		}
	}
}

func testWithCancal() {
	ctx, cancel := context.WithCancel(context.Background())
	go worker(ctx, "WithCancel")
	time.Sleep(dms)
	cancel()
}

func testWithDeadline() {
	// 到期会自动cancal，可以手动cancal
	ctx, cancal := context.WithDeadline(context.Background(), time.Now().Add(dms))
	go worker(ctx, "WithDeadline")
	time.Sleep(dms)
	_ = cancal
}

func testWithTimeout() {
	ctx, cancal := context.WithTimeout(context.Background(), dms)
	go worker(ctx, "WithTimeout")
	time.Sleep(dms)
	_ = cancal
}

// ExContext 测试上下文
func ExContext() {
	testWithCancal()
	testWithDeadline()
	testWithTimeout()
}
