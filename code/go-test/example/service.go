package example

import (
	"fmt"
	"net/http"
	"strings"
	"sync"
)

var count = 0
var mu sync.Mutex

func addCount() {
	mu.Lock()
	count++
	mu.Unlock()
}

func parseRequest(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Host, r.Method, r.URL)
	addCount()
	texts := []string{}
	for k, v := range r.Header {
		texts = append(texts, fmt.Sprintf("Header %s=%s", k, v))
	}
	if err := r.ParseForm(); err != nil {
		w.WriteHeader(500)
	} else {
		for k, v := range r.Form {
			texts = append(texts, fmt.Sprintf("Form %s=%s", k, v))
		}
	}
	w.Write([]byte(strings.Join(texts, "\n")))
}

func getCount(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Host, r.Method, r.URL)
	mu.Lock()
	fmt.Fprintf(w, "count %d", count)
	mu.Unlock()
}

// Service 服务端
func Service(addr string) {
	fmt.Println("listen: ", addr)
	http.HandleFunc("/", parseRequest)
	http.HandleFunc("/count", getCount)
	http.ListenAndServe(addr, nil)
}
