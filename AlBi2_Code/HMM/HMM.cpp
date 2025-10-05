#include "HMM.h"
#include <string>

HMM::HMM(const std::vector<char>& symbols, const std::vector<char>& states, const std::vector<std::vector<double>>& transition_matrix, const std::vector<std::vector<double>>& emission_matrix){
    this -> symbols = symbols;
    this -> states = states;
    this -> transition_matrix = transition_matrix;
    this -> emission_matrix = emission_matrix;

    uint16_t spot = 0;
    for (char symbol : symbols){
        symbol_pos[spot] = symbol;
        symbol_pos_back[symbol] = spot++;
    }

    spot = 0;
    for (char state : states){
        state_pos[spot++] = state;
    }
};

HMM::HMM(const HMMvals& hmmvals){
    this -> symbols = hmmvals.symbols;
    this -> states = hmmvals.states;
    this -> transition_matrix = hmmvals.transition_matrix;
    this -> emission_matrix = hmmvals.emission_matrix;

    uint16_t spot = 0;
    for (char symbol : symbols){
        symbol_pos[spot] = symbol;
        symbol_pos_back[symbol] = spot++;
    }

    spot = 0;
    for (char state : states){
        state_pos[spot++] = state;
    }
};
    
HMM::HMM(const std::vector<std::string>& train_set, const std::vector<char>& states){
    //Approach for Baum-Welch (not yet implemented):
    //Collect symbols and initialize symbol/state pos
    // Initialize matrices w/ pseudocounts
    // Apply algorithms in EM fashion
};


std::tuple<std::string,std::string> HMM::generate_random(uint len) const{
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

        res_state += state_pos.at(current_state);

        e_rand = distribution(gen);
        for (uint16_t i = 0; i < symbols.size(); i++){
            e_rand -= emission_matrix[current_state][i];
            if (e_rand<0){
                res_symbol += symbol_pos.at(i);
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


std::tuple<std::string,double> HMM::Viterbi(const std::string& query) const{
    std::vector<double> prob_cols(states.size()-1,0);
    std::vector<std::vector<double>> prob_matrix(query.size(),prob_cols);


    std::vector<uint16_t> tb_cols(states.size()-1,0);
    std::vector<std::vector<uint16_t>> tb_matrix(query.size()-1,tb_cols);

    for (uint j = 1; j < states.size(); j++){
        prob_matrix[0][j-1] = (transition_matrix[0][j]*emission_matrix[j][symbol_pos_back.at(query[0])]);
    }    
    
    for (uint i = 1; i < query.size(); i++){
        for (uint j = 1; j < states.size(); j++){
            double transition_val = prob_matrix[i-1][0]*(transition_matrix[1][j]);
            uint16_t transition_origin = 1;
            for (uint k = 2; k < states.size(); k++){
                double new_val = prob_matrix[i-1][k]*(transition_matrix[k][j]);
                if (transition_val < new_val){
                    transition_val = new_val;
                    transition_origin = k;
                }
            }
            prob_matrix[i][j-1] = transition_val*(emission_matrix[j][symbol_pos_back.at(query[i])]);
            tb_matrix[i-1][j-1] = transition_origin;
        }
    }

    double prob = prob_matrix[query.size()-1][0]*(transition_matrix[1][0]);
    uint16_t transition_origin = 1;
    for (uint k = 2; k < states.size(); k++){
        double new_val = prob_matrix[query.size()-1][k-1]*(transition_matrix[k][0]);
        if (prob < new_val){
            prob = new_val;
            transition_origin = k;
        }
    }
    
    std::string path(1,state_pos.at(transition_origin));
    for (int i = query.size()-2; i >= 0; i--){
        path = state_pos.at(transition_origin) + path;
        transition_origin = tb_matrix[i][transition_origin-1];
    }

    return std::tie(path,prob);
};

double HMM::Forward(const std::string& query) const{
    return std::get<double>(std::move(Forward_Matrix(query)));
};

    
std::tuple<std::vector<std::vector<double>>,double> HMM::Forward_Matrix(const std::string& query) const{
    std::vector<double> prob_cols(states.size()-1,0);
    std::vector<std::vector<double>> prob_matrix(query.size(),prob_cols);

    for (uint j = 1; j < states.size(); j++){
        prob_matrix[0][j-1] = (transition_matrix[0][j]*emission_matrix[j][symbol_pos_back.at(query[0])]);
    }    
    
    for (uint i = 1; i < query.size(); i++){
        for (uint j = 1; j < states.size(); j++){
            double transition_val = prob_matrix[i-1][0]*(transition_matrix[1][j]);
            for (uint k = 2; k < states.size(); k++){
                transition_val += prob_matrix[i-1][k-1]*(transition_matrix[k][j]);
            }
            prob_matrix[i][j-1] = transition_val*(emission_matrix[j][symbol_pos_back.at(query[i])]);
        }
    }

    double prob = prob_matrix[query.size()-1][0]*(transition_matrix[1][0]);
    for (uint k = 2; k < states.size(); k++){
        prob += prob_matrix[query.size()-1][k-1]*(transition_matrix[k][0]);
    }

    return std::tie(prob_matrix, prob);
};


double HMM::Backward(const std::string& query) const{
    return std::get<double>(std::move(Backward_Matrix(query)));
};


std::tuple<std::vector<std::vector<double>>,double> HMM::Backward_Matrix(const std::string& query) const{
    std::vector<double> prob_cols(states.size()-1,0);
    std::vector<std::vector<double>> prob_matrix(query.size(),prob_cols);

    for (uint j = 1; j < states.size(); j++){
        prob_matrix[query.size()-1][j-1] = transition_matrix[j][0];
    }    

    
    for (int i = query.size()-2; i >= 0; i--){
        for (uint j = 1; j < states.size(); j++){
            double transition_val = prob_matrix[i+1][0]*(transition_matrix[j][1])*(emission_matrix[1][symbol_pos_back.at(query[i+1])]);
            for (uint k = 2; k < states.size(); k++){
                transition_val += prob_matrix[i+1][k-1]*(transition_matrix[j][k])*(emission_matrix[k][symbol_pos_back.at(query[i+1])]);
            }
            prob_matrix[i][j-1] = transition_val;
        }
    }

    double prob = prob_matrix[0][1]*(transition_matrix[0][1])*(emission_matrix[1][symbol_pos_back.at(query[0])]);
    for (uint k = 2; k < states.size(); k++){
        prob += prob_matrix[0][k-1]*(transition_matrix[0][k])*(emission_matrix[k][symbol_pos_back.at(query[0])]);
    }

    return std::tie(prob_matrix,prob);
};


std::vector<std::vector<double>> HMM::Posterior_Decoding(const std::string& query) const{
    auto [forward_matrix, prob] = Forward_Matrix(query);
    std::vector<std::vector<double>> backward_matrix = std::get<0>(std::move(Backward_Matrix(query)));

    std::vector<double> post_cols(states.size()-1,0);
    std::vector<std::vector<double>> post_matrix(query.size(),post_cols);

    for (uint i = 0; i < query.size(); i++){
        for (uint j = 1; j < states.size(); j++){
            post_matrix[i][j-1] = forward_matrix[i][j-1]*backward_matrix[i][j-1]/prob;
        }
    }

    return post_matrix;
};