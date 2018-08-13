#include <iostream>
#include <string>
using namespace std;
int main()
{
string str="01234567890000";
int a;
a=str.find("0");
cout<<a<<endl;//返回0
a=str.find("123");
cout<<a<<endl;//返回1
a=str.find("456");
cout<<a<<endl;//返回4
return 0;
}
