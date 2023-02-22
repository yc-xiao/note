package example

import (
	"fmt"
)

// ExSelect 测试select
func ExSelect() {
	/*
		chan 信道，由发送端关闭执行关闭操作。已关闭的信道执行写操作时会panic，执行读操作时返回信道默认值，即v, ok <- ch； v=0, ok=false。
		select 随机选择一条可读信道执行，已关闭信道是可读的，返回信道默认值。若无可读信道则执行default，若无default则阻塞
	*/
	msg := [...]chan int{
		make(chan int),
		make(chan int, 3),
		make(chan int, 3),
		make(chan int),
	}
	main := func(msg []chan int) {
	loop:
		for {
			// select 随机选择一条可读(已关闭)通信执行，若无则执行default，若无default则阻塞。
			select {
			case i, ok := <-msg[0]:
				fmt.Println("chan 0 ->", i, ok)
			case i, ok := <-msg[1]:
				fmt.Println("chan 1 ->", i, ok)
			case i, ok := <-msg[2]:
				fmt.Println("chan 2 ->", i, ok)
				if i == 1000 {
					break loop // break 跳出select；break loop，跳到指定位置(跳出select跟for)
				}
			}
		}
		fmt.Println("main end")
		msg[3] <- 1000
		close(msg[3])
	}
	send := func(c chan int, n int) {
		for i := 0; i < 3; i++ {
			c <- i
		}
		if n == 2 {
			c <- 1000
		}
		close(c) // 发送端关闭信道，重复关闭信道会panic
	}

	for i, ch := range msg[:3] {
		fmt.Printf("start ch%d，%v\n", i, ch)
		go send(ch, i)
	}

	go main(msg[:])
	v, ok := <-msg[3]
	fmt.Println("gobal end", v, ok)
	v, ok = <-msg[3] // 已关闭信道可读，返回信道类型的默认值，状态为false
	fmt.Println("gobal end", v, ok)
}
