#include <iostream>
#include <fstream>
#include <string.h>

using namespace std;

int main()
{
	ofstream ofs;
	ofs.open("test.bin", ios::out | ios::binary );
	
	double x[] = {1,2,3,4,5,1,2,1,2,1};
	
	
	double a = 0;
	
	int n = 10;
	int size = n*sizeof(double);
	
	char buffer[size];
	
	memcpy(&buffer,&x,size);
	
	cout << size << "\n";
	
	ofs.write(buffer,size);
	
	ofs.close();
	
	
	
	return 0;
}