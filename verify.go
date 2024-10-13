package gomock

import (
	"reflect"
)

type Verifier interface {
	Verify(methodName string) bool
}

type SimpleVerfier struct {
	called map[string]bool
}

func (v *SimpleVerfier) Verify(methodName string) bool {
	// TODO : verification logic
}