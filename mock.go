package gomock

import (
	"reflect"
)

type mock struct {
	stubs map[string]Stub
}

func (m *mock) Stub(methodName string, stub Stub){
	m.stubs[methodName] = stub
}

func (m *mock) Verify(methodName string) bool {
	// TODO : method verfication logic
}