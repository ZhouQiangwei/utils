#include <iostream>
#include <string>
#include <math.h>
using namespace std;
int calmapq(int l){
        int avg=154;
        int std=46;
        int i = (int)(-4.343 * log(.5 * erfc(M_SQRT1_2 * fabs(l - avg) / std)) + .499);
	std::cout << M_SQRT1_2 << "\t" << erfc(M_SQRT1_2 * fabs(l - avg) / std) << std::endl;
	return i;
}
int main()
{
	std::cout << calmapq(1) << "\t" << calmapq(150) << std::endl;
	std::cout << calmapq(200) << "\t" << calmapq(250) << std::endl;
	return 0;
}
