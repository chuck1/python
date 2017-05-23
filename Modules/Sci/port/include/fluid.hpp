#ifndef FLUID_HPP
#define FLUID_HPP

#include <vector>
#include <cassert>
#include <cmath>
#include <memory>
#include <map>
#include <fstream>

#include <boost/serialization/nvp.hpp>
#include <boost/serialization/map.hpp>
#include <boost/serialization/shared_ptr.hpp>
#include <boost/serialization/vector.hpp>

#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>


#include <decl.hpp>

class Fluid {
	public:
		Fluid();
		void					load(std::string filename);
		void					save(std::string filename);
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("props", props_);
		}
		double		get(std::string prop_name, double T);
		void		list();
		double		enthalpy_change(double T0, double T1);
		double		get_Pr(double T);
	public:
		std::map< std::string, Property >	props_;
};



#endif


