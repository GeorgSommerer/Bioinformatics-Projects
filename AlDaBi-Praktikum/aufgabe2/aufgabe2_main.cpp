#include "aufgabe2.hpp"
#include <algorithm>
#include <iostream>
#include <numeric>
#include <stdint.h>
#include <cmath>
#include <tuple>

int main(int argc, const char* argv[]) {
    std::vector<uint32_t> sa;
    std::vector<uint32_t> hits;
    if (argc<2){
        std::cout << "unexpected input\n";
        return(1);
    }
    else if (argc==2){
        construct(sa, argv[1]);
        for (uint32_t elem:sa){
            std::cout << elem << "\n";
        }
    }
    else{    
        construct(sa,argv[1]);
        for (int i=2;i<argc;++i){
            find(argv[i],sa,argv[1],hits);
            std::cout << argv[i]<<":";
            for (uint32_t & elem : hits) {
                std::cout << " "<< elem;
            }
            std::cout << "\n";
        }
    }    
}