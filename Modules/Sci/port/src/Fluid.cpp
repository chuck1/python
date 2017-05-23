#include <util.hpp>
#include <poly.hpp>
#include <prop.hpp>
#include <fluid.hpp>

Fluid::Fluid() {}
void					Fluid::load(std::string filename) {
	filename = media_dir + filename;
	
	std::ifstream ifs;
	ifs.open(filename);

	if(!ifs.is_open()) {
		std::cout << "file error" << std::endl;
		exit(1);
	}
	
	boost::archive::xml_iarchive ar(ifs);

	serialize(ar,0);

}
void					Fluid::save(std::string filename) {
	filename = media_dir + filename;

	std::ofstream ofs;
	ofs.open(filename, std::ofstream::out | std::ofstream::trunc);
	
	if(!ofs.is_open()) {
		std::cout << "file error" << std::endl;
		std::cout << filename << std::endl;
		exit(1);
	}

	boost::archive::xml_oarchive ar(ofs);

	serialize(ar,0);

}
double					Fluid::get(std::string prop_name, double T) {
	auto it = props_.find(prop_name);

	if(it == props_.end()) {
		list();
		throw 0;
	}

	Property& prop = it->second;

	auto poly = prop.polys_[0];

	return poly.eval( T );
}
void					Fluid::list() {
	//"""list properties"""
	
	std::cout << "fluid" << std::endl;

	for(auto it : props_) {
		std::cout << it.first << std::endl;
		it.second.print();
	}
}
double		Fluid::enthalpy_change(double T0, double T1) {
	auto X = linspace(T0,T1,100);

	return props_["cp"].polys_[0].integrate( X );
}
double		Fluid::get_Pr(double T) {
	auto cp = get("cp",T);
	auto mu = get("dynamic_viscosity",T);
	auto k = get("thermal_conductivity",T);

	//print cp,mu,k;

	auto Pr = cp * mu / k;
	return Pr;
}


