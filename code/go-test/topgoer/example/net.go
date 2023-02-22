package example

import (
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
)

var names = make(map[string]string)
var conns = make(map[string]net.Conn)
var count = 1
var mu = &sync.Mutex{}

func getCount() string {
	mu.Lock()
	defer mu.Unlock()
	count = count + 1
	return fmt.Sprintf("%d", count)
}

func ssender() {
	buf := make([]byte, 4096)
	var temp string
	for {
		n, er := os.Stdin.Read(buf)
		if er != nil {
			fmt.Println(er)
			continue
		}
		temp = string(buf[:n])
		msgs := strings.Split(temp, " ")
		if n, ok := names[msgs[0]];ok{
			msgs[0] = n
		}
		if conn, ok := conns[msgs[0]]; ok {
			data := []byte(strings.Join(msgs[1:], " "))
			_, ew := conn.Write(data)
			if ew != nil {
				delete(conns, msgs[0])
				fmt.Println(ew)
			}
		}
	}
}

func sender(conn net.Conn, wg *sync.WaitGroup, id string) {
	buf := make([]byte, 4096)
	var n int
	var er, ew error
	for {
		n, er = os.Stdin.Read(buf)
		_, ew = conn.Write(buf[:n])
		if er != nil || ew != nil {
			fmt.Println("sender:", id, er, ew)
			break
		}
		if string(buf[:n]) == "close\n" {
			break
		}
	}
	wg.Done()
}

func receiver(conn net.Conn, wg *sync.WaitGroup, id string) {
	buf := make([]byte, 4096)
	var temp string
	for {
		n, er := conn.Read(buf)
		temp = string(buf[:n])
		
		temp = id + ": " + temp
		_, ew := os.Stdout.WriteString(temp)
		if er != nil || ew != nil {
			fmt.Println("receiver:", id, er, ew)
			break
		}
		if temp == "close\n" {
			break
		}
	}
	wg.Done()
}

func process(conn net.Conn) {
	remoteID := conn.RemoteAddr().String()
	n := getCount()
	names[remoteID] = n
	conns[n] = conn
	fmt.Println(names, conn)
	fmt.Println("remote:", remoteID, conn.RemoteAddr().Network())
	defer conn.Close()
	wg := &sync.WaitGroup{}
	wg.Add(1)
	// go sender(conn, wg, remoteID)
	go receiver(conn, wg, remoteID+"_"+n)
	wg.Wait()
}

// TCPServer TCP服务
func TCPServer(addr string) {
	fmt.Println("tcp server，输入close关闭对话")
	lister, _ := net.Listen("tcp", addr)
	go ssender()
	for {
		// conn是接口，不适合使用指针
		conn, _ := lister.Accept()
		go process(conn)
	}
}

// TCPClient TCP客户端
func TCPClient(addr string) {
	wg := &sync.WaitGroup{}
	fmt.Println("tcp client， 输入close关闭对话")
	conn, _ := net.Dial("tcp", addr)
	defer conn.Close()
	remoteID := conn.RemoteAddr().String()
	fmt.Println("connect: ", remoteID)
	wg.Add(1)
	go sender(conn, wg, "local")
	go receiver(conn, wg, remoteID)
	wg.Wait()
}
