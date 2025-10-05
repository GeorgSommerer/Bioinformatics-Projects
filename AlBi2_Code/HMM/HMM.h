#pragma once
#include <vector>
#include <cstdint>
#include <string>
#include <tuple>
#include <map>
#include <bits/stdc++.h>
#include <cmath>

struct HMMvals{
    std::vector<char> states{};
    std::vector<char> symbols{};
    std::vector<std::vector<double>> transition_matrix{};
    std::vector<std::vector<double>> emission_matrix{};
};

class HMM{
public:

    /**
    @brief: Initializes the HMM with predefined transition and emission probabilities.
    @param symbols: The list of emittable characters. The position in this list corresponds to the position in the column entries in the emission matrix.
    @param states: The names of the states of the HMM. The first state must be the beginning/end state. The position in the vector corresponds to the position in the entries of the transition matrix, the row entries of the emission matrix, and the column entries -1 in the matrices created temporarily in the algorithm methods.
    @param transition_matrix: The rows represent the outgoing states, the columns the incoming states.
    @param emission_matrix: The rows represent the states, the columns the symbols.
    */
    HMM(const std::vector<char>& symbols, const std::vector<char>& states, const std::vector<std::vector<double>>& transition_matrix, const std::vector<std::vector<double>>& emission_matrix);
    

    /**
    @brief: Initializes the HMM with predefined transition and emission probabilities packed in a struct.
    @param hmmvals: The struct containing states, symbols, transition matrix and emission matrix.
    */
    HMM(const HMMvals& hmmvals);

    /**
    @brief: Initializes an HMM with a given state layout using Baum-Welch training on the training set.
    @param train_set: The list of sequences that is used to train the HMM.
    @param states: The names of the states of the HMM (as above).
    */
    HMM(const std::vector<std::string>& train_set, const std::vector<char>& states);

    /**
    @brief: Destructor for the HMM.
    */
    ~HMM(){};

    /**
    @brief: Generates a random text from the HMM.
    @len: The length of the text; will run until end state is reached if not specified.
    */
    std::tuple<std::string,std::string> generate_random(uint len = 0) const;

    /**
    @brief: Gets the most probable path for a certain string via the Viterbi algorithm.
    @query: The query string.
    @return: The most probable path and the probability of this path.
    */
    std::tuple<std::string,double> Viterbi(const std::string& query) const;

    /**
    @brief: Gets the log probability that a certain string is generated via the Forward algorithm.
    @query: The query string.
    @return: The log probability.
    */
    double Forward(const std::string& query) const;
    std::tuple<std::vector<std::vector<double>>,double> Forward_Matrix(const std::string& query) const;


    /**
    @brief: Gets the log probability that a certain string is generated via the Backward algorithm.
    @query: The query string.
    @return: The log probability.
    */
    double Backward(const std::string& query) const;
    std::tuple<std::vector<std::vector<double>>,double> Backward_Matrix(const std::string& query) const;


    /**
    @brief: Gets the log probability for each possible state for each symbol in the query via Posterior Decoding.
    @query: The query string.
    @return: The matrix of all the log probabilities.
    */
    std::vector<std::vector<double>> Posterior_Decoding(const std::string& query) const;

protected:
    std::vector<char> symbols;
    std::vector<char> states;
    std::vector<std::vector<double>> transition_matrix;
    std::vector<std::vector<double>> emission_matrix;
    std::map<uint16_t,char> symbol_pos{};
    std::map<char,uint16_t> symbol_pos_back{};
    std::map<uint16_t,char> state_pos{};
};