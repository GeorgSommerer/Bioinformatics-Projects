#pragma once
#include <vector>
#include <cstdint>
#include <string>
#include <tuple>
#include <map>
#include <bits/stdc++.h>

class HMM{
public:

    /**
    @brief: Initializes the HMM with predefined transition and emission probabilities
    @param symbols: The list of emittable characters. The position in this list corresponds to the position in the column entries in the emission matrix.
    @param states: The names of the states of the HMM. The first state must be the beginning/end state. The position in the vector corresponds to the position in the entries of the transition matrix, the row entries of the emission matrix, and the column entries in the matrices created temporarily in the algorithm methods.
    @param transition_matrix: The rows represent the outgoing states, the columns the incoming states.
    @param emission_matrix: The rows represent the states, the columns the symbols.
    */
    HMM(std::vector<char> symbols, std::vector<char> states, std::vector<std::vector<float>> transition_matrix, std::vector<std::vector<float>> emission_matrix);
    
    /**
    @brief: Initializes an HMM with a given state layout using Baum-Welch training on the training set.
    @param train_set: The list of sequences that is used to train the HMM.
    @param states: The names of the states of the HMM (as above).
    */
    HMM(std::vector<std::string> train_set, std::vector<char> states);

    /**
    @brief: Destructor for the HMM.
    */
    ~HMM(){};

    /**
    @brief: Generates a random text from the HMM.
    @len: The length of the text; will run until end state is reached if not specified.
    */
    std::tuple<std::string,std::string> generate_random(uint len = 0);

    /**
    @brief: Gets the most probable path for a certain string via the Viterbi algorithm.
    @query: The query string.
    @return: The most probable path.
    */
    std::vector<std::string> Viterbi(std::string query);

    /**
    @brief: Gets the log probability that a certain string is generated via the Forward algorithm.
    @query: The query string.
    @return: The log probability.
    */
    float Forward(std::string query);
    std::vector<std::vector<float>> Forward_Matrix(std::string query);


    /**
    @brief: Gets the log probability that a certain string is generated via the Backward algorithm.
    @query: The query string.
    @return: The log probability.
    */
    float Backward(std::string query);
    std::vector<std::vector<float>> Backward_Matrix(std::string query);


    /**
    @brief: Gets the log probability for each possible state for each symbol in the query via Posterior Decoding.
    @query: The query string.
    @return: The matrix of all the log probabilities.
    */
    std::vector<std::vector<float>> Posterior_Decoding(std::string query);

protected:
    std::vector<char> symbols;
    std::vector<char> states;
    std::vector<std::vector<float>> transition_matrix;
    std::vector<std::vector<float>> emission_matrix;
    std::map<uint16_t,char> symbol_pos{};
    std::map<uint16_t,char> state_pos{};
};