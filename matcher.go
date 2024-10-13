package gomock

import (
	"reflect"
)

type Matcher interface {
	Match(args []reflect.Value) bool
}

type ExactMatcher struct {}

func (m *ExactMatcher) Match(args []reflect.Value) bool {
	// TODO : matching logic
}