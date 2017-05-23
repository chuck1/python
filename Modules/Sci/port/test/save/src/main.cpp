
#include <Fluids.hpp>

int main() {



	Poly poly;
	
	poly.a_.push_back(1.0);

	
	Property prop;

	prop.polys_.push_back(poly);



	Fluid f;

	f.props_["a"] = prop;
	
	f.save("flu1.xml");
	
}

