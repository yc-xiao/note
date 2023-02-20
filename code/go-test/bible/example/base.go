package example

import (
	"errors"
	"fmt"
	"strings"
)

// testLocalAndGlobalVar 测试变量的作用域
func testLocalAndGlobalVar() {
	x := "hello!"
	for i := 0; i < len(x); i++ {
		fmt.Println(x)
		x := x[i] // x: x是一个局部新变量
		fmt.Println(x)
		if x != '!' {
			x := x + 'A' - 'a'
			fmt.Printf("%c\n", x) // "HELLO" (one letter per iteration)
		}
	}
	fmt.Println()
	for i := 0; i < len(x); i++ {
		fmt.Println(x)
		x = string(x[i]) // x: x外层变量
		fmt.Println(x)
	}
}

// testType type测试
func testType() {
	// 新的变量类型A B
	type A int
	type B int

	// int的别名有C, D
	type C = int
	type D = int

	var a A = 10
	var b B = 10
	var c C = 10
	var d D = 10
	var e int = 10
	fmt.Println(c == d, c == e, d == e)
	fmt.Println(a == A(b), b == B(a), e == int(a), e == int(b))

}

// testPointer 指针测试
func testPointer() {
	// 变量：类型+地址+值组成；指针是特殊的变量：类型+地址+值(其他变量的地址)组成；
	// 指针通过*取值，变量通过&取地址。
	n := 100      // var n int = 100， 变量n的类型为int
	pn1 := &n     // &n取变量n的地址，该地址指向100
	var pn2 *int  // 定义一个int类型的指针变量(变量具有类型)
	pn2 = pn1     // pn2 = pn1 = &n
	*pn2++        // *pn2 == n = 100
	var pn3 **int // 定义一个*int类型的指针变量
	pn3 = &pn2    // pn3 = &pn2, *pn3 -> pn2, **pn3 -> *pn2
	fmt.Printf("n的值为%d，n的地址为%p\n", n, &n)
	fmt.Printf("pn1的值为%d(%x), pn1的地址为%p\n", pn1, pn1, &pn1)
	fmt.Printf("pn2的值为%d(%x), pn2的地址为%p\n", pn2, pn2, &pn2)
	fmt.Printf("pn3的值为%d(%x), pn3的地址为%p\n", pn3, pn3, &pn3)
	fmt.Println(n, pn1, *pn1, pn2, *pn2, pn3, *pn3, **pn3)
}

// testSwitch
func testSwitch() {
	var v int
	switch {
	default:
		fmt.Println("default")
	case v == 0:
		fmt.Println("v == 0")
		fallthrough
	case v > 10:
		fmt.Println("v fallthrough")
	case v > 10:
		fmt.Println("v > 10")
	}
	fmt.Println("v2 == 10")
	// 当switch有值v时，case 若值与v相等则执行，若无值与v相等则执行default
	switch v := 10; v {
	case 0:
		fmt.Println("v == 0")
	default:
		fmt.Println("default")
		fallthrough
	case 1:
		fmt.Println("fallthrough")
	case 10: // case 9则执行default和case1
		fmt.Println("v == 10")
	}
}

// testIota iota累加器
func testIota() {
	// 不支持 var
	const (
		a1 = iota // 0
		a2        // 1
		a3        // 2
		a4 = "a4" // a4
		a5        // a4
		a6 = iota // 5
	)
	fmt.Println(a1, a2, a3, a4, a5, a6)
}

// defaultValue 变量的默认值
func defaultValue() {
	// 基础类型字符串，数值，布尔值，浮点数，结构体的默认值为"", 0, false, 0.0, {}
	type Student struct{ Name string }
	var s string
	var i int
	var B bool
	var st Student
	fmt.Println(s, i, B, st)

	// 引用类型(func, *struct, slice, map, chan, interface)的默认值为nil
	type F func(s string)
	type I interface{}
	var pst *Student
	var f F
	var c chan string
	var m map[string]string
	var in I
	if m == nil {
		fmt.Println("m is nil")
	}
	fmt.Println(pst, f, c, in, m)

	// 引用类型初始化，slice, map, chan是封装的struct使用make初始化，而结构体可以直接使用new返回指针
	ss, dic, ch := make([]string, 10), make(map[string]string), make(chan string)
	if ss == nil {
		fmt.Println("ss is nil")
	}
	if dic == nil {
		fmt.Println("dic is nil")
	}
	if ch == nil {
		fmt.Println("ch is nil")
	}
	fmt.Println(ss, dic, ch)
}

// tryError painc上抛异常，使用defer延期函数func(){}()执行recover捕获painc
func tryError() {
	defer func() {
		if e := recover(); e != nil {
			fmt.Println(e)
		}
	}()
	panic(errors.New("test painc"))
}

// longString 长字符，字符串打印
func longString() {
	ss := "床前明月光，\n" +
		"疑是地上霜。\n" +
		"举头望明月，\n" +
		"低头思故乡。\n"
	fmt.Printf("char len %d, str len %d \n", len(ss), len([]rune(ss)))
	for i, s := range ss {
		_, _ = i, string(s)
	}
	// string 可转换为[]rune，rune==int32，也可以转换为[]int8， byte代表int8
	for i := 0; i < len(ss); i++ {
		_, _, _ = ss[i], byte(ss[i]), string(ss[i])
		// fmt.Println(i, ss[i], byte(ss[i]), string(ss[i]))
	}

	sss := `
		床前明月光，
		疑是地上霜。
		举头望明月，
		低头思故乡。
	`
	fmt.Println(sss)
	for _, s := range strings.Split(sss, "\n") {
		fmt.Println(strings.TrimSpace(s))
	}
}
