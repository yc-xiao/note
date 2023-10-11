package main

/*
	开启一个ssh反向代理 ssh -R remoteIP:remotePort:localhost:localPort proxyUser@proxyIP -p proxyPort -i private.pem -N
	将ssh的私钥写入data对象中，并编译为新的二进制文件，可以隐藏用户私钥。
*/

import (
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"os/exec"
	"strings"
	"time"
)

var data = `
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
`

func checkError(e error) {
	if e != nil {
		log.Fatalln(e)
	}
}

var usage = func() {
	fmt.Fprintf(flag.CommandLine.Output(), "Usage of %s:\n", os.Args[0])
	fmt.Fprintf(flag.CommandLine.Output(), "命令: ssh -R remoteIP:remotePort:localhost:localPort proxyUser@proxyIP -p proxyPort -i private.pem -N\n")
	flag.PrintDefaults()
}

func main() {
	var err error
	// 自定义参数解析
	localIP := flag.String("localIP", "localhost", "-localIP localhost")
	localPort := flag.String("localPort", "22", "-localPort 22")
	remoteIP := flag.String("remoteIP", "0.0.0.0", "-remoteIP 0.0.0.0")
	remotePort := flag.String("remotePort", "22", "-remotePort 22")
	proxyIP := flag.String("proxyIP", "192.168.1.1", "-proxyIP 192.168.1.1")
	proxyUser := flag.String("proxyUser", "test", "-proxyUser test")
	proxyPort := flag.String("proxyPort", "22", "-proxyPort 22")
	serverAliveInterval := flag.String("serverAliveInterval", "-1", "-serverAliveInterval -1")
	flag.Usage = usage
	flag.Parse()

	// 检测ssh隧道是否开启
	checkCMD := fmt.Sprintf("ps -aux|grep %s@%s|grep %s|grep -vE 'grep'", *proxyUser, *proxyIP, *remotePort)
	if err = exec.Command("bash", "-c", checkCMD).Run(); err == nil {
		log.Printf("ssh隧道已存在，使用命令  %s  查询\n", checkCMD)
		return
	}

	// 检测远程端口是否能使用
	if _, err = net.Dial("tcp", net.JoinHostPort(*proxyIP, *remotePort)); err == nil {
		log.Fatalf("远程端口%s被占用，请使用 -remotePort 切换端口\n", *remotePort)
	}

	// 生成临时文件
	rand.New(rand.NewSource(time.Now().Unix()))
	tempFilePath := fmt.Sprintf("/tmp/%d", rand.Intn(1000)+100000)
	err = os.WriteFile(tempFilePath, []byte(data), 0600)
	checkError(err)

	// 开启ssh隧道
	// ssh -R remoteIP:remotePort:localhost:localPort proxyUser@proxyIP -p proxyPort -i private.pem -N
	cmdString := ""
	if *serverAliveInterval != "-1" {
		cmdString = fmt.Sprintf("ssh -o ServerAliveInterval=%s -R %s:%s:%s:%s %s@%s -p %s -i %s -N", *serverAliveInterval, *remoteIP, *remotePort, *localIP, *localPort, *proxyUser, *proxyIP, *proxyPort, tempFilePath)
	} else {
		cmdString = fmt.Sprintf("ssh -R %s:%s:%s:%s %s@%s -p %s -i %s -N", *remoteIP, *remotePort, *localIP, *localPort, *proxyUser, *proxyIP, *proxyPort, tempFilePath)
	}
	log.Println(cmdString)
	cmdList := strings.Split(cmdString, " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	err = cmd.Start()
	checkError(err)

	// 等待1秒后移除文件
	time.Sleep(1 * time.Second)
	err = os.Remove(tempFilePath)
	checkError(err)

	err = cmd.Wait()
	checkError(err)
}
