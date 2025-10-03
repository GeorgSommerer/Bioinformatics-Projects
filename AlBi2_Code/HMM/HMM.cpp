#include "HMM.h"

HMM::HMM(std::vector<char> symbols, std::vector<char> states, std::vector<std::vector<float>> transition_matrix, std::vector<std::vector<float>> emission_matrix){
    this -> symbols = symbols;
    this -> states = states;
    this -> transition_matrix = transition_matrix;
    this -> emission_matrix = emission_matrix;
    this -> symbol_pos = {};

    uint16_t spot = 0;
    for (char symbol : symbols){
        symbol_pos[spot++] = symbol;
    }

    spot = 0;
    for (char state : states){
        state_pos[spot++] = state;
    }
};

    
HMM::HMM(std::vector<std::string> train_set, std::vector<char> states){
    //Collect symbols and initialize symbol/state pos
    // Initialize matrices w/ pseudocounts
    // Apply algorithms in EM fashion
};


std::tuple<std::string,std::string> HMM::generate_random(uint len){
    uint current_len = 1; //current_len is the length after the next loop (so that it is always >0)
    uint16_t current_state = 0;
    std::string res_symbol = "";
    std::string res_state = "";

    std::default_random_engine gen;
    gen.seed(42);
    std::uniform_real_distribution<double> distribution(0.0,1.0);
    double t_rand = distribution(gen);
    double e_rand = distribution(gen);

    for (uint16_t i = 0; i < states.size(); i++){ //find starting state
        t_rand -= transition_matrix[0][i];
        if (t_rand<0){
            current_state = i;
            break;
        }
    }    

    do{
        if (current_state == 0){
            break;
        }

        res_state += state_pos[current_state];

        e_rand = distribution(gen);
        for (uint16_t i = 0; i < symbols.size(); i++){
            e_rand -= emission_matrix[current_state][i];
            if (e_rand<0){
                res_symbol += symbol_pos[i];
                break;
            }
        }   

        do{ //if len!=0 (if the length is fixed), reroll the transition rng value until it doesn't point to the end state
            t_rand = distribution(gen);
        }
        while (len != 0 && t_rand <= transition_matrix[current_state][0]);

        for (uint16_t i = 0; i < states.size(); i++){
            t_rand -= transition_matrix[current_state][i];
            if (t_rand<0){
                current_state = i;
                break;
            }
        }  
        current_len++;
    }
    while(current_len <= len || len == 0);

    return std::tie(res_symbol,res_state);
};

/*
std::vector<std::string> HMM::Viterbi(std::string query){

};


float HMM::Forward(std::string query){
    return std::move(Forward_Matrix(query))[query.size()-1][0];
};

    
std::vector<std::vector<float>> HMM::Forward_Matrix(std::string query){

};


float HMM::Backward(std::string query){
    return std::move(Backward_Matrix(query))[query.size()-1][0];
};


std::vector<std::vector<float>> HMM::Backward_Matrix(std::string query){

};


std::vector<std::vector<float>> HMM::Posterior_Decoding(std::string query){

};


protected:
    std::vector<char> symbols;
    std::vector<std::string> states;
    std::vector<std::vector<float>> transition_matrix;
    std::vector<std::vector<float>> emission_matrix;
    enum class symbol_pos{};
    enum class state_pos{};
};*/