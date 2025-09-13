#include <iostream>
#include "BWT.h"

int main(int argc, const char* argv[]){
    if (argc != 3){
        std::cout << argv[0] << " <TEXT> <PATTERN>" << std::endl; 
        return 1;
    }
    BWT b;
    b.setText(argv[1]);
    std::cout << "BWT: " << b.getBWT() << std::endl;
    std::string rle = b.encodeRLE();
    std::cout << "Encoded: " << rle << std::endl;
    std::cout << "Decoded: " << b.decodeRLE(rle) << std::endl;

    std::string pat = argv[2];
    std::vector<uint32_t> hits = b.FMindex(pat);
    std::cout << "Hits: ";
    for (uint32_t hit : hits){
        std::cout << hit << " ";
    }
    std::cout << std::endl;

    return 0;
}