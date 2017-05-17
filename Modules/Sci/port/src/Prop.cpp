#include <Fluids.hpp>


Property::Property() {
	//print 'prop tag=',node.tag

	/*for(child in list(node)) {
	  self.poly.append( Poly( child ) );
	  }*/

}
void		Property::print() {
	for(auto p : polys_) {
		p.print();
	}
}



