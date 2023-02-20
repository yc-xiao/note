package example

import (
	"fmt"
	"reflect"
)

// Movie 表
type Movie struct {
	Title, Subtitle string
	Year            int
	Color           bool
	Actor           map[string]string
	Oscars          []string
	Sequel          *string
}

func display(data interface{}) {
	value := reflect.ValueOf(data)
	_display(value.Type().Name(), value)
}

func _display(path string, v reflect.Value) {
	switch v.Kind() {
	case reflect.Invalid:
		fmt.Printf("%s=nil\n", path)
	case reflect.Array, reflect.Slice:
		for i := 0; i < v.Len(); i++ {
			_display(fmt.Sprintf("%s[%d]", path, i), v.Index(i))
		}
	case reflect.Map:
		for _, k := range v.MapKeys() {
			vk := v.MapIndex(k)
			_display(fmt.Sprintf("%s[%s]", path, k.String()), vk)
		}
	case reflect.Struct:
		for i := 0; i < v.NumField(); i++ {
			vf := v.Field(i)

			_display(fmt.Sprintf("%s.%s", path, v.Type().Field(i).Name), vf)
		}
	case reflect.Ptr:
		if v.IsNil() {
			fmt.Printf("%s=nil\n", path)
		} else {
			_display(fmt.Sprintf("(*%s)", path), v.Elem())
		}
	default:
		fmt.Printf("%s = %s\n", path, v)
	}
}

// TestReflect 测试反射
func TestReflect() {
	strangelove := Movie{
		Title:    "Dr. Strangelove",
		Subtitle: "How I Learned to Stop Worrying and Love the Bomb",
		Year:     1964,
		Color:    false,
		Actor: map[string]string{
			"Dr. Strangelove":            "Peter Sellers",
			"Grp. Capt. Lionel Mandrake": "Peter Sellers",
			"Pres. Merkin Muffley":       "Peter Sellers",
			"Gen. Buck Turgidson":        "George C. Scott",
			"Brig. Gen. Jack D. Ripper":  "Sterling Hayden",
			`Maj. T.J. "King" Kong`:      "Slim Pickens",
		},

		Oscars: []string{
			"Best Actor (Nomin.)",
			"Best Adapted Screenplay (Nomin.)",
			"Best Director (Nomin.)",
			"Best Picture (Nomin.)",
		},
	}
	display(strangelove)
}
