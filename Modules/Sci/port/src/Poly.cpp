#include <Fluids.hpp>

Poly::Poly() {
	/*		text = node.text;
			text = re.sub('[\s\n]*','',text);
			split = re.split(",", node.text);*/

	//		self.a = np.array([]);

	//print 'poly tag =', node.tag, "attr =",node.attrib

	//print 'poly text=%r' % node.text
	//print 'split {0}'.format( split )

	// process coefficients
	/*		for(s in split) {
			v = float(s);
			self.a = np.append(self.a, v);*/
	//	}

	//print "a =",self.a
}
double				Poly::eval(double X) {
	//print "X",X

	std::vector<double> Y(X, a_.size());
	//auto Y = np.array( [X]*len(self.a) );

	auto z = sum( mul(a_, pow( Y, range(a_.size())) ));

	return z;
}
std::vector<double>		Poly::eval(std::vector<double> X) {
	//print "X",X
	std::vector<double> Z;
	for(auto x : X) {

		Z.push_back(eval(x));

	}
	return Z;
}
double				Poly::integrate(std::vector<double> X) {
	auto Y = eval(X);
	auto Z = integ(X, Y);
	return Z;
}
void				Poly::print() {
	
	std::cout << std::setw(8) << " " << "poly" << std::endl;

	for(auto a : a_) {
		std::cout << std::setw(12) << " " << a << std::endl;
	}

}

