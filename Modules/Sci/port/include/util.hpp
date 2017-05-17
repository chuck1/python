#ifndef UTIL_HPP
#define UTIL_HPP

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



#endif


