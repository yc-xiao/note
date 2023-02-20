package example

import "fmt"

// InputDevice 定义接口方法Input
type InputDevice interface {
	Input(string)
}

// OutputDevice 定义接口方法Output
type OutputDevice interface {
	Output() string
}

// IODevice 定义接口方法Input和Output
type IODevice interface {
	InputDevice
	OutputDevice
}

// Device 设备，提供方法Input和Output，可作为接口IODevice
type Device struct {
	value string
}

// Input Device 提供方法Input，可作为接口InputDevice
func (d *Device) Input(s string) {
	d.value = s
}

// Output Device 提供方法Output，可作为接口OutputDevice
func (d *Device) Output() string {
	return d.value
}

// Int InputDevice接口
func Int(i InputDevice, s string) {
	i.Input(s)
}

// Out OutputDevice
func Out(o OutputDevice) string {
	return o.Output()
}

func testIODevice(d IODevice, s string) {
	Int(d, s)
	outValue := Out(d)
	fmt.Println(outValue)
}

// TestInterface 接口测试
func TestInterface() {
	// 接口规定方法，只要满足接口方法就可以作为接口
	d := &Device{}
	testIODevice(d, "2333")

	// 变量支持接口的方法，将变量赋给接口(变量的类型，变量的值)
	var io IODevice = d
	// 接口断言，假设已知接口内变量的类型，可以通过接口断言获取变量的值 in.(T)
	dv, ok := io.(*Device)
	fmt.Println(dv, ok)
	// 接口断言，当T为接口时，断言成功后。得到对应的接口变量，可使用接口的规定的方法。
	iv, ok := io.(OutputDevice)
	fmt.Println(iv, ok, iv.Output())
	// 接口断言
	type A interface {
		Ax()
	}
	fail, ok := io.(A)
	fmt.Println(fail, ok)
}
