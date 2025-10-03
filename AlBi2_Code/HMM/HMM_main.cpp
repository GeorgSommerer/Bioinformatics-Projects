#include "HMM.h"

int main(){
    std::vector<char> states = {'0','f','u'};
    std::vector<char> symbols = {'1','2','3','4','5','6'};
    std::vector<std::vector<float>> transition_matrix = {{0,0.5,0.5},{0.005,0.9,0.095},{0.005,0.095,0.9}};
    std::vector<std::vector<float>> emission_matrix = {{0,0,0,0,0,0},{1.0/6,1.0/6,1.0/6,1.0/6,1.0/6,1.0/6},{1.0/10,1.0/10,1.0/10,1.0/10,1.0/10,1.0/2}};
    HMM myHMM(symbols,states,transition_matrix,emission_matrix);
    auto [res_symbols, res_states] = myHMM.generate_random(10);
    std::cout << res_symbols << std::endl;
    std::cout << res_states << std::endl;
    return 0;
}