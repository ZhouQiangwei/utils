#include <iostream>
#include <stdlib.h>
#include <string>
#include <zlib.h>
 
using namespace std;
 
int main(int argc, char **argv){
        if(argc != 2){
                cerr << "example command: exe file.tar.gz" << endl;
                return 0;
        }
        gzFile gzfp = gzopen(argv[1], "rb");
        if(!gzfp)
                return 0;
        char buf[32];
        while(gzgets(gzfp, buf, 31)){
                cout << "str: " << buf << endl;
                cout << "num: " << atof(buf) << endl;
        }
        return 0;
}
