#include "BWT.h"
#include <cstdint>
#include <numeric>
#include <algorithm>
#include <iostream>
#include <string>


void BWT::setText(const std::string& text){
    constructSA(text + "$");
    for (const uint32_t& i : sa)
        if (i==0){
            bwt += '$';
        }
        else{
            bwt += text[i-1];
        }
}

void BWT::constructSA(const std::string& text){
    sa.resize(text.size());
    std::iota(sa.begin(),sa.end(),0);
    auto comparevecs = [text](uint32_t a, uint32_t b){
        uint32_t i=0;
        while (text[a+i]==text[b+i] && a+i<text.size() && b+i<text.size()){
            i++;
        }
        if (a+i==text.size()){
            return true;
        }
        if (b+i==text.size()){
            return false;
        }
        else{
            return text[a+i]<text[b+i];
        }
    };
    std::sort(sa.begin(),sa.end(),comparevecs);
}

std::string BWT::getBWT() const{
    return bwt;
}


std::vector<uint32_t> BWT::getSA() const{
    return sa;
}

std::string BWT::encodeRLE(){
    uint i = 0;
    std::string rle{};
    while (i<bwt.size()){
        char c_current = bwt[i];
        uint l_current = 1;
        while (bwt[i]==bwt[i+1]){
            i++;
            l_current++;
        }
        if (int(c_current)>=48 && int(c_current)<=57){
            rle += std::to_string(l_current) + "\\" + c_current;
        }
        else {
            rle += std::to_string(l_current) + c_current;
        }
        i++;
    }
    return rle;
}

std::string BWT::decodeRLE(std::string rle){
    std::string back_bwt = "";
    uint i = 0;
    while (i<rle.size()){
        uint l_start = i;
        uint l_len = 0;
        while (int(rle[i])>=48 && int(rle[i])<=57){
            i++;
            l_len++;
        }
        uint32_t l_current = std::stoi(rle.substr(l_start,l_len));
        if (rle[i]=='\\'){
            i++;
        }
        char c_current = rle[i++];
        std::string str_current = std::string(l_current, c_current);
        back_bwt += str_current;
    }
    return LFmap(back_bwt);
}

void BWT::setRanks(){
    std::vector<uint32_t> empty(bwt.size(),0);

    for (uint i = 0; i<bwt.size();i++){
        if (count.count(bwt[i])==0){
            count[bwt[i]] = 0;
            rankAll[bwt[i]] = empty;
        }
        count[bwt[i]]++;
        for (auto const & [c, n]: count){
            rankAll[c][i] = n;
        }
    }

    uint32_t n_current = 0;
    for (auto const & [c,n] : count){
        cumRank[c] = n_current; // cumRank becomes equal to the no. of occurences of all previous symbols
        n_current += n;
        
    }
}

void BWT::printMatrix(const std::string& sorted_bwt) const{
    std::cout << "   ";
    for (char c : sorted_bwt){
        std::cout << c << " ";
    }
    std::cout << std::endl << "   ";
    for (char c : bwt){
        std::cout << c << " ";
    }
    std::cout << std::endl;
    for (auto const & [c,n]:rankAll){
        std::cout << c << ": ";
        for (uint32_t i : n){
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "   ";
    for (uint32_t i : sa){
        std::cout << i << " ";
    }

    std::cout << std::endl << "Cumulative:" << std::endl;
    for (auto const & [c, n]: cumRank){
        std::cout << c << " " << n << std::endl;
    }
    std::cout << "Count:" << std::endl;
    for (auto const & [c, n]: count){
        std::cout << c << " " << n << std::endl;
    }
}



std::string BWT::LFmap(std::string bwt){
    if (rankAll.size()==0){
        setRanks();
    }
    std::string sorted_bwt = bwt;
    std::sort(sorted_bwt.begin(),sorted_bwt.end());

    //printMatrix(sorted_bwt);

    std::string text = "";
    uint32_t pos = 0;
    for (uint i = bwt.size()-1; i>0; i--){
        text = bwt[pos] + text;
        pos = cumRank[bwt[pos]] + rankAll[bwt[pos]][pos] - 1;
    }
    return text;
}

std::string BWT::LFmap(){
    std::string this_bwt = this -> bwt;
    return LFmap(this_bwt);
}

std::vector<uint32_t> BWT::FMindex(std::string& pat){
    std::vector<uint32_t> hits{};
    if (cumRank.count(pat[pat.size()-1])==0){
        std::cout << "Pattern not found in text." << std::endl;
        return hits;
    }
    
    uint32_t pos_lower = cumRank[pat[pat.size()-1]];
    uint32_t pos_upper = pos_lower + count[pat[pat.size()-1]] - 1;

    for (int i = pat.size()-2; i>=0; i--){
        if (cumRank.count(pat[i])==0){
            std::cout << "Pattern not found in text." << std::endl;
            return hits;
        }
        pos_lower = cumRank[pat[i]] + rankAll[pat[i]][pos_lower] - 1;
        pos_upper = cumRank[pat[i]] + rankAll[pat[i]][pos_upper] - 1;
    }
    for (uint i = pos_lower; i <= pos_upper; i++){
        hits.push_back(sa[i]);
    }

    if (hits.size()==0){
        std::cout << "Pattern not found in text." << std::endl;
    }
    else{
        std::sort(hits.begin(),hits.end());
    }
    return hits;
}