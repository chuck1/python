#include <Fluids.hpp>

//char const * modules_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/";
//char const * media_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/Sci/media/";

std::vector<int>	range(int stop) {
	std::vector<int> ret;
	for(int i = 0; i < stop; i++) {
		ret.push_back(i);
	}
	return ret;
}
std::vector<double>	linspace(double a, double b, int n) {
	std::vector<double> ret;
	for(int i = 0; i < n; ++i) {
		ret.push_back(a + (b-a)/((double)(n-1)) * ((double)i));
	}
	return ret;
}
std::vector<double>	mul(std::vector<double> a, std::vector<double> b) {
	assert(a.size() == b.size());
	std::vector<double> ret;
	for(auto i : range(a.size())) {
		ret.push_back(a[i] * b[i]);
	}
	return ret;
}
double	sum(std::vector<double> a) {
	double ret = 0;
	for(auto d : a) {
		ret += d;
	}
	return ret;
}
std::vector<double>	pow(std::vector<double>& a, std::vector<int> b) {
	assert(a.size() == b.size());
	std::vector<double> ret;
	for(auto i : range(a.size())) {
		ret.push_back(pow(a[i], b[i]));
	}
	return ret;
}

double	integ(std::vector<double>X, std::vector<double> Y) {
	double ret = 0;
	for(unsigned int i = 1; i < X.size(); i++) {
		ret += ((Y[i] + Y[i-1]) * (X[i] - X[i-1]) * 0.5);
	}
	return ret;
}


