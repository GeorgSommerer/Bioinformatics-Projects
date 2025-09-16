#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <algorithm>
#include <stdlib.h>

struct scoring_scheme{
    scoring_scheme(): pair(1),nonpair(0){}
    int pair, nonpair;
};

class nus{
public:
    /**
    * @brief: Creates an instance of the class with a set RNA and a variable scoring scheme.
    * @param rna: The string of RNA.
    * @param scores: The scoring scheme (default 1 for matching base pair and 0 for non-paired base).
    */
    nus(const std::string& rna, ulong gap_size, const struct scoring_scheme scores = scoring_scheme());

    ~nus(){};

    /**
    * @brief: Resets the scoring scheme.
    * @param scores: The new scoring scheme.
    */
    void setSS(const struct scoring_scheme scores);
    
    /**
    * @brief: Performs the Nussinov algorithm and fills matrix containing the scores, as well as a matrix containing the next field(s) in the traceback.
    * @param gap_size: The minimal distance between two bases in the primary structure to be able to perform a base pairing.
    * @return the secondary structure in bracket representation, as well as the final score.
    */
    std::tuple<std::string, int> fillMatrix();

    /**
    * @brief: Recursively generates the secondary (sub-)structure in bracket representation based on the traceback matrix.
    * @param i: The starting row of the substructure.
    * @param j: The starting column of the substructure.
    * @return the secondary (sub-)structure.
    */
    std::string traceback(uint i, uint j) const;
    

    
protected:
    std::string rna{};
    ulong gap_size{};
    struct scoring_scheme scores{};
    std::vector<std::vector<int>> score_matrix{};
    std::vector<std::vector<int>> traceback_matrix{};
};