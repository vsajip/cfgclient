package main

import (
	"fmt"
	"github.com/vsajip/go-cfg-lib/config"
	"io"
	"strings"
)

func main() {
	s := "{key: 'Hello, world!'}"
	var r io.Reader = strings.NewReader(s)
	cfg := config.NewConfig()
	err := cfg.Load(&r)
	if err == nil {
		v, err := cfg.Get("key")
		if err == nil {
			fmt.Println(v)
		}
	}
}
