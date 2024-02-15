#include "Alignment.hpp"

int main(int argc, const char* args[]){
    if (argc==3){
        Alignment al = Alignment(args[1],args[2]);
        al.compute(3,-1,-2,false);
        std::string a1; std::string gaps; std::string a2;
        al.getAlignment(a1,gaps,a2);
    }
    else if (argc==6){
        Alignment al = Alignment(args[1],args[2]);
        int match = std::stoi(args[3]); int mismatch = std::stoi(args[4]); int gap = std::stoi(args[5]);
        al.compute(match, mismatch, gap,false);
        std::string a1; std::string gaps; std::string a2;
        al.getAlignment(a1,gaps,a2);
    }
    else if (argc==7){
        Alignment al = Alignment(args[1],args[2]);
        int match = std::stoi(args[3]); int mismatch = std::stoi(args[4]); int gap = std::stoi(args[5]);
        al.compute(match, mismatch, gap,true);
        std::string a1; std::string gaps; std::string a2;
        al.getAlignment(a1,gaps,a2);
    }
    else{
        std::cout << "unexpected input\n";
        exit(1);
    }
}