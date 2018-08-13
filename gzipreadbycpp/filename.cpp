#include <iostream>  
#include <algorithm>  
#include <string.h>  
#include <assert.h>  
  
std::string GetFilePosfix(const char* path)  
{ 
    std::cout << strlen(path) << std::endl;
    std::string str(path); 
    str=str.substr(str.length()-2,2);
    std::cout << str << std::endl;
    std::transform(str.begin(),str.end(),str.begin(),::tolower);  
    return str;  
}  
  
bool IsSupportPos(const std::string& posfix,const std::string& support)  
{  
    std::string str(";");  
    str.append(posfix).append(";");  
  
    if(support.find(str)!=std::string::npos)  
    {  
        return true;  
    }  
    return false;  
}  
  
int main(int argc, char const *argv[])  
{  
    const char* POSFIX = ";jpg;png;bmp;jpeg;gif;";  
    const char* path = "E:\\picture\\11.ggIf";  
      
    std::string posfix = GetFilePosfix(path);  
    std::cout << posfix << std::endl;  
//    assert(!IsSupportPos(posfix,POSFIX));  
  
    path = "E:\\picture\\11.gIf";  
    posfix = GetFilePosfix(path);  
    std::cout << posfix << std::endl;  
 //   assert(IsSupportPos(posfix,POSFIX));  
  
  
    return 0;  
}  
