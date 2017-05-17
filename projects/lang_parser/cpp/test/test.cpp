
#include "test.h"

ns::foo::foo()
{
}
void ns::foo::fun()
{
}

bar::bar()
{
	foo f;
	f.fun();
}

