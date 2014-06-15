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


/*import os
  import math
  import re
  import sys
  from lxml import etree
  import numpy as np*/

//modules_dir = os.environ["HOME"] + '/Documents/Programming/Python/Modules/'
//media_dir = modules_dir + 'Sci/media/'

static char const * const modules_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/";
static char const * const media_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/Sci/media/";


/*void get_child_by_attr(root,attr,value) {
  for child in list(root) {
  if(child.get(attr) == value)
  return child;
  }
  return None;
  }*/
/*
   void process_element(root) {
//print root.tag
for child in list(root):
process_element(child)
}
*/

std::vector<int>		range(int stop);
std::vector<double>		linspace(double a, double b, int n);
std::vector<double>		mul(std::vector<double> a, std::vector<double> b);
double				sum(std::vector<double> a);
std::vector<double>		pow(std::vector<double>& a, std::vector<int> b);
double				integ(std::vector<double>X, std::vector<double> Y);

class Poly {
	public:
		Poly();
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("a", a_);
		}
		double				eval(double X);
		std::vector<double>		eval(std::vector<double> X);
		double		integrate(std::vector<double> X);

		/**
		 * polynomial coefficients
		 */
		std::vector<double>	a_;
};
class Property {
	public:
		Property();
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("polys", polys_);
		}
	public:
		std::vector< Poly >		polys_;

};

class Fluid {
	public:
		Fluid(std::string filename);
		void					load(std::string filename);
		void					save(std::string filename);

		Fluid();
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


