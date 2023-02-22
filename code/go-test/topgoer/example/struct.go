package example

import (
	"fmt"
)

// Animal 动物
type Animal struct {
	name string
}

// AnimalB B类动物
type AnimalB = Animal

// Dog 狗
type Dog struct {
	*Animal         // 继承只能通过嵌套匿名结构体实现，非匿名字段无法继承方法
	B       AnimalB // 非匿名字段可以非显示调用方法
}

// 结构体跟*a都可以调用setName，修改不生效
func (a Animal) setName(name string) {
	a.name = name
}

// 结构体跟*a都可以调用setPName，修改生效
func (a *Animal) setPName(name string) {
	a.name = name
}

func (a *Animal) move() {
	fmt.Printf("%s会动！\n", a.name)
}

// Dog可重写move方法
func (d Dog) move() {
	fmt.Printf("%s会跑！\n", d.name)
}

func testT() {
	// 结构体在定义方法时，通过T或*T确定是否能修改内部的值。
	// 通常调用方法时，T与*T都可以调用所有的方法，方法会自动转换T与*T。
	// 但接口定义方法时会严格要求，T只能调用接收者为T的方法，*T能调用*T+T的方法。
	// 若T的匿名字段是S，则接口集为S+T，若T的匿名字段为*S则接口集合为S+*S+T。
	a := Animal{"小金"}
	fmt.Println(a.name)
	a.name = "小木"
	fmt.Println(a.name)
	a.setName("小水") // setName是复制变量，不会更新字段
	fmt.Println(a.name)
	a.setPName("小火") // setPName是复制地址，会更新字段
	fmt.Println(a.name)

	pa := &Animal{"小金"}
	fmt.Println(pa.name)
	pa.name = "小木"
	fmt.Println(pa.name)
	pa.setName("小水") // setName是复制变量，不会更新字段
	fmt.Println(pa.name)
	pa.setPName("小火") // setPName是复制地址，会更新字段
	fmt.Println(pa.name)

	type PI interface{ setPName(string) } // PI 定义接口PI
	type I interface{ setName(string) }   // I 定义接口I
	var p PI
	p = pa
	p.setPName("小土1")
	fmt.Println(pa.name)
	// p = a // 编译报错

	var i I
	i = pa
	i.setName("小土2")
	fmt.Println(pa.name)
	i = a
	a.setName("小土3")
	fmt.Println(a.name)
}

func testAnonymity() {
	fmt.Println("本地自定义的结构体可以定义方法，包外的结构体无法添加新的方法。")
	fmt.Println("即type oint int，可以给新的结构体oint添加方法；type aint=int不能给aint(int)添加方法。")
	fmt.Println("结构体可以通过 匿名字段 继承(匿名调用) 匿名结构体的方法，若非匿名字段，则通过指定字段调用方法")
	d := &Dog{Animal: &Animal{"小黑"}, B: AnimalB{"小黄"}}
	d.Animal.move() // 显示调用匿名字段的方法
	d.B.move()      // 显示调用非匿名字段方法
	d.move()        // 若Dog无重载Animal的move方法，则匿名调用d.Animal.move，若重载则调用d.move
}

// ExStuct 结构体
func ExStuct() {
	testT()
}
