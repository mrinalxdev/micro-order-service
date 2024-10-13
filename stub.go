package gomock

import (
	"reflect"
)

type Stub interface {
	Invoke(args []reflect.Value) []reflect.Value
}

type SimpleStub struct {
	returnValue reflect.Value
}

func (s *SimpleStub) Invoke(args []reflect.Value) []reflect.Value{
	return []reflect.Value{s.returnValue}
}