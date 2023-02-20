package example

import (
	"fmt"
	"io"
	"net/http"
)

// Requests 访问urls
func Requests(urls []string) {
	n := len(urls)
	ch := make(chan string, n)
	for _, url := range urls {
		go get(url, ch)
	}
	for i := 0; i < n; i++ {
		fmt.Println(<-ch)
	}
}

func get(url string, ch chan<- string) {
	resp, err := http.Get(url)
	handleErrorAndFatal(err, "Requests http.Get")
	defer resp.Body.Close()
	data, err := io.ReadAll(resp.Body)
	handleErrorAndFatal(err, "Requests io.ReadAll")
	ch <- string(data)
}
