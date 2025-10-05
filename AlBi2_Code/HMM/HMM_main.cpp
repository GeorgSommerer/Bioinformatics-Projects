#include "HMM.h"

int main(){    

    HMMvals u12{{'0','1','2'},{'A','C','G','T'},{{0,0.75,0.25},{0.25,0.5,0.25},{0.25,0.5,0.25}},{{0,0,0,0},{0.25,0.25,0.125,0.375},{0.125,0.25,0.5,0.125}}};
    HMM myHMM_u12(u12);

    auto [res_symbols, res_states] = myHMM_u12.generate_random(10);
    std::cout << "Path generated from HMM:" << std::endl;
    std::cout << res_symbols << std::endl;
    std::cout << res_states << std::endl;
    
    std::string query = "TC";
    auto [states, prob_v] = myHMM_u12.Viterbi(query);
    std::cout << "Most probable path for " << query << ": " << states << " with a probability of " << prob_v << std::endl;


    std::cout << "Probability of the query being generated: " << std::get<1>(myHMM_u12.Forward_Matrix(query)) << std::endl;
    /*for (auto vec : matrix){
        for (auto elem : vec){
            std::cout << elem << " ";
        }
        std::cout << std::endl;
    }

    auto [matrix2,prob2] = myHMM_u12.Backward_Matrix("TC");
    for (auto vec : matrix2){
        for (auto elem : vec){
            std::cout << elem << " ";
        }
        std::cout << std::endl;
    }
    std::cout << prob2 << std::endl;
    */

    std::vector<std::vector<double>> post = myHMM_u12.Posterior_Decoding(query);
    std::cout << "Results of posterior decoding: " << std::endl;
    for (auto vec : post){
        for (auto elem : vec){
            std::cout << elem << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}