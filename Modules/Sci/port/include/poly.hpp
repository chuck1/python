#ifndef POLY_HPP
#define POLY_HPP

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



class Poly {
	public:
		Poly();
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("a", a_);
		}
		double				eval(double X);
		std::vector<double>		eval(std::vector<double> X);
		double				integrate(std::vector<double> X);
		void				print();
		
		/**
		 * polynomial coefficients
		 */
		std::vector<double>	a_;
};



#endif


