package example

import (
	"fmt"
)

func init() {
	// fmt.Println("同一个文件，多个init包按从上到下的顺序执行；")
	// fmt.Printf("同一个包，不同文件的init包按文件名的顺序执行。\n")
}

// ExVariableError 变量常见错误
func ExVariableError() {
	type student struct {
		name string
		age  int
	}
	m := make(map[string]*student)
	stus := []student{
		{name: "pprof.cn", age: 18},
		{name: "测试", age: 23},
		{name: "博客", age: 28},
	}

	// PS: 取地址时，需要注意取的是那个变量的地址
	// stu是变量，m[stu.name] = &stu， &stu取变量stu的地址。
	for _, stu := range stus {
		fmt.Printf("%p\n", &stu)
		m[stu.name] = &stu
	}
	// var stu student
	// stu = stus[0]
	// m[stus[0].name] = &stu
	// stu = stus[1]
	// m[stus[1].name] = &stu
	// stu = stus[2]
	// m[stus[2].name] = &stu

	// 地址应该取&stus[n]
	// for i := 0; i < len(stus); i++ {
	// 	m[stus[i].name] = &stus[i]
	// }

	for k, v := range m {
		fmt.Printf("%s => %s\t", k, v.name)
	}
	fmt.Println()
}

// ExVariable 变量栗子
func ExVariable() {
	var (
		v1 uint  = 1
		v2 uint8 = 1
		v3 byte  = 1 // type byte = uint8
		v4 rune  = 1 // type rune = int32
		v5 int32 = 1
		v6 int   = 1 // int -> system -> 32/64
	)
	fmt.Printf("%T %T %T %T %T %T \n", v1, v2, v3, v4, v5, v6)

	// 超出范围，溢出
	var v7 int8 = 1
	fmt.Printf("int8: 1+127 = %d; 除法: 5/2=%d, 5.0/2=%f \n\n", v7+127, 5/2, 5.0/2)

	ss := "床前明月光，疑是地上霜。"
	ss2 := []rune(ss)
	fmt.Printf("len %d, %s\n", len(ss), ss)
	fmt.Printf("len %d, %s\n\n", len(ss2), string(ss2))

	// 引用类型与值类型
	desc := `类型：引用类型(slice, map, chan)和值类型，引用类型一般使用make进行初始化。
函数传参都是值传递，由于引用类型的结构(struct)包含指针，修改时会关联对应的数据故称为引用类型。
如：slice的底层结构为len+cap+*array，在值传递过程中拷贝*array，当修改*array会操作到对应的array。
`
	fmt.Println(desc)
	type user struct {
		name    string
		friends []*user
	}
	// copy 函数 copy 在两个 slice 间复制数据，复制长度以 len 小的为准
	u1, u2, u3 := &user{name: "小明"}, &user{name: "小红"}, &user{name: "小黄"}
	u1.friends = append(u1.friends, u2, u3)
	u2.friends = append(u2.friends, u1)
	u3.friends = append(u3.friends, u1)
	fmt.Println(u1, u2, u3)
	// u1Friends := []*user{} , copy复制失败，因为u1Friends的cap跟len=0
	u1Friends := make([]*user, len(u1.friends))
	copy(u1Friends, u1.friends)
	u1.friends[0].name += "?"
	fmt.Println(u1Friends[0].name, u1.friends[0].name)

	fmt.Println("六种定义未赋值(slice, map, chan, interface, func, *ptr)，默认值为nil")
}
