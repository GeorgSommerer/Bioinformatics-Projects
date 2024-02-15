#include "PDA.hpp"

int main(int argc, const char* args[]){
    if (argc!=2){
        throw std::invalid_argument("Missing input");
    }
    std::string text = args[1];
    PDA my_pda;
    text+='$';
    PDA::State b{};
    for (char a : text){
        b = my_pda.next(a);
    }
    switch (b){
        case PDA::State::FAIL:
            std::cout << "REJECT\n";
            break;
        case PDA::State::SUCCESS:
            std::cout << "ACCEPT\n";
            break;
        default:
            throw std::logic_error("Dieser Fall sollte nicht eintreten.");
    }
}