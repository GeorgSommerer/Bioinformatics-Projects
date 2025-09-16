#include "Nussinov.h"

int main(int argc, const char* argv[]){
    if (argc != 3){
        std::cout << argv[0] << " <RNA> <GAP SIZE>" << std::endl;
        return 1;
    }
    nus myNus{argv[1], std::stoul(argv[2])};
    auto [str, score] = myNus.fillMatrix();
    std::cout << str << ", " << score << std::endl;
}

