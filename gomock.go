package gomock

import (
	"reflect"
)

type Mock interface {
	Stub(methodName string, stub Stub)

	Verify(methodName string) bool
}

func NewMock(t interface{}) Mock{
	//TODO : Mock object creation logic
}