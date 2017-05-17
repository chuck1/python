#ifndef PROPERTY_HPP
#define PROPERTY_HPP

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

class Property {
	public:
		Property();
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("polys", polys_);
		}
		void					print();
	public:
		std::vector< Poly >		polys_;

};




#endif


