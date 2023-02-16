package example

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
)

// testArgs 可变参数
func testArgs(args ...interface{}) {
	for i, arg := range args {
		fmt.Printf("%d, %T, %v\n", i, arg, arg)
	}
}

// testJSONByMap
// map[string]interface{} 全部转换
func testJSONByMap() {
	type O = map[string]interface{}
	tempfile := "a.json"
	obj, obj2 := make(O), make(O)
	obj["name"], obj["nums"] = "名称", []int{1, 2, 3}

	objData, _ := json.Marshal(obj)
	file, _ := os.OpenFile(tempfile, os.O_CREATE|os.O_RDWR, os.ModePerm)
	defer file.Close()
	file.Write(objData)
	file, _ = os.OpenFile(tempfile, os.O_CREATE|os.O_RDWR, os.ModePerm)
	objData2, _ := io.ReadAll(file)
	json.Unmarshal(objData2, &obj2)
	fmt.Println(objData, obj)
	fmt.Println(objData2, obj2)
	os.Remove(tempfile)
}

// testJSONByStruct
// Struct 定义转换
func testJSONByStruct() {
	type Animal struct {
		Name string `json:"name"`
	}
	type Dog struct {
		Animal           // 匿名字段，json自动会提取匿名字段
		Actions []string `json:"actions"`
	}
	type Dog2 struct {
		A       Animal   `json:"animal"` // 非匿名字段，作为一个对象
		Actions []string `json:"actions"`
	}

	tempfile := "struct.txt"
	d1 := &Dog{Animal: Animal{Name: "d1"}, Actions: []string{"跑", "叫", "吃"}}
	d2 := Dog2{A: Animal{Name: "d2"}}
	d1d, _ := json.Marshal(d1)
	d2d, _ := json.Marshal(d2)
	file, _ := os.OpenFile(tempfile, os.O_CREATE|os.O_RDWR, os.ModePerm)
	defer file.Close()
	file.Write(d1d)
	file.WriteString("\n")
	file.Write(d2d)
}

// Person class
type Person struct {
	father       *Person   // Person内只能用指针Person，不能直接包含Person
	mother       *Person   // 首字母大写表示包外可用，小写则包外不可用。即外包json无法解析小写变量，且包外无法使用小写变量
	children     *[]Person //
	Name, Gender string
}

// TestStruct 公开函数
func TestStruct() {
	testStruct()
	testStruct2()
}

// testStruct 结构体测试
func testStruct() {
	a := Person{Name: "用户a", Gender: "男"}
	a.father = &Person{Name: "用户a的爸爸", Gender: "男"}
	a.mother = &Person{Name: "用户a的妈妈", Gender: "女"}
	fmt.Println(a, a.father)
}

// testStruct2 结构体测试
func testStruct2() {
	// 匿名字段，组合
	type Student struct {
		Person // 匿名字段，s.Name == s.Person.Name。包内继承Person所有字段与方法， 包外只继承公开的字段和属性。
	}

	type Teacher struct {
		p        Person // 显示字段，t.p.Name
		students []*Student
	}
	s1 := &Student{Person{Name: "小明", Gender: "男"}}
	s1.Name = "小敏"
	s1.Person.Gender = "女"
	fmt.Println(s1)
}

// testUintAndFloat32 注意符号位
// uint 无符号位，适合做位运算
// float64 比 float32的位数更多更安全
func testUintAndFloat32() {
	var i int8 = 127
	fmt.Println(i+1 == -128)
	var f float32 = 1 << 24
	fmt.Println(f == f+1)

}

// testArray 数组介绍
func testArray() {
	array := [...]int{1, 2, 3, 9: 10} // 数组需要指定个数[n]int，当n=...会自动解析个数，{1, 9:10}表示index=9, value=10
	fmt.Println(array)
	modifyArray := func(array *[10]int, i, v int) { array[i] = v }
	// slice, map 是特殊的结构体，内部数据使用指针，可以直接复制
	modifyArray(&array, 2, 200) // 函数参数是复制一份，对于数据较大的变量一般使用指针传递，只需复制一份指针即可通过地址操作原变量。
	fmt.Println(array)
}

// testSlice 切片测试说明
func testSlice() {
	// 初始化数值100
	array := [...]int{100: 0}
	for i := 1; i <= 100; i++ {
		array[i-1] = i
	}
	// slice结构包含 len cap *array
	// len表示当前*array的长度
	// cap表示slice的可用长度，当len>cap时会申请内存空间，提高cap的长度
	// *array 指向底层数组
	// 切片作为函数参数时，直接复制cap，len，*array，可共享*array
	s1, s2 := array[:10], array[10:20]
	s3 := make([]int, 10, 20) // s3, index最大为9
	s3 = array[5:15]
	s4 := []int{}
	s3[1], s3[6] = 1000, 2000
	fmt.Printf(" s1(%T): %v\n s2(%T): %v\n s3(%T): %v\n s4(%T): %v\n", s1, s1, s2, s2, s3, s3, s4, s4)
}

// testMap Map测试说明
func testMap() {
	var m0 map[string]string
	m1, m2 := map[string]string{}, make(map[string]string)
	fmt.Println(m0 == nil, m1 == nil, m2 == nil)
	m1["m1"], m2["m2"] = "1", "2"
	fmt.Println(m1, m2)
	v1, ok := m1["m2"]
	v2 := m1["m2"]
	fmt.Println(v1, ok, v2)
	_ = &m1 // _ = &m1["m2"] 禁止对map元素取址，map随着元素数量的增长而重新分配更大的内存空间，从而可能导致之前的地址无效。
}
