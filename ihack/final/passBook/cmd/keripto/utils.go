package keripto

import (
	"crypto/md5"
	"fmt"
	"io"
)

func Md5hash(params ...string) string {
	h := md5.New()
	for _, param := range params {
		io.WriteString(h, param)
	}
	res := fmt.Sprintf("%x", h.Sum(nil))
	return res
}

func DecodeBase64(s string) string {
	bytes, _ := StdEncoding.DecodeString(s)
	res := string(bytes)
	return res
}

func EncodeBase64(s string) string {
	bytes := []byte(s)
	res := StdEncoding.EncodeToString(bytes)
	return res
}
