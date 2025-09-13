#pragma once
#include <string>
#include <vector>
#include <map>
#include <cstdint>

class BWT
{
public:
    /**
    * @brief: Creates the BWT of the input text (text cannot contain any characters with a lower ASCII value than $).
    * @param text The text the BWT should be applied to.
    */
    void setText(const std::string& text);

    /**
    * @brief: Creates a suffix array based on the input text.
    * @param text The text that was input, with a $ sign affixed at the end. */
    void constructSA(const std::string& text);

    /**
    * @brief: Returns the BWT string.
    * @return the BWT.
    */
    std::string getBWT() const;

    /**
    * @brief: Returns the suffix array.
    * @return the SA. */
    std::vector<uint32_t> getSA() const;

    /**
    * @brief: Creates the compressed run-length encoding version of the text; for examepl, the string "aaa" would be simply written as "3a", and "111" as "3\1".
    * @return the compressed RLE.
    */
    std::string encodeRLE();

    /**
    * @brief: Takes the RLE version of the text and converts it back to the original text.
    * @param rle The compressed RLE that is returned by encodeRLE.
    * @return the original text.
    */
    std::string decodeRLE(std::string rle);

    /**
    * @brief: Fills the lexicographically ordered rankAll matrix containing the number of occurences of each character at every position of the BWT, as well as cumrank, the total number of times lexicographically smaller characters appear in the entire text.
    */
    void setRanks();

    /**
    * @brief: Prints the BWT, the sorted BWT, the rankAll matrix, and the SA.
    * @param sorted_bwt the sorted BWT.
    */
    void printMatrix(const std::string& sorted_bwt) const;

    /**
    * @brief: Using the BWT, the sorted BWT, and ranks of each character, the LF map regenerates the original text.
    * @return the original text.
    */
    std::string LFmap(std::string bwt);
    std::string LFmap();
    /**
    * @brief: The FM index uses backwards matching to find all positions of a pattern in the text in O(n) time via the suffix array information.
    * @param pat the pattern that should be matched in the text.
    * @return a list of all 1-based occurences in the text.
    */
    std::vector<uint32_t> FMindex(std::string& pat);
protected:
    std::string bwt = {};
    std::string rle{};
    std::vector<uint32_t> sa{};
    std::map<char,std::vector<uint32_t>> rankAll{};
    std::map<char,uint32_t> cumRank{};
    std::map<char,uint32_t> count{};

};