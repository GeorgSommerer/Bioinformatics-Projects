#include <omp.h>
#include "BLAST_Neighborhood.hpp"
#include "a4_util.h"


void BLAST_Neighborhood::findNeighborsRecursive(const int pos, const int word_size,int score,int score_threshold,NHResult& substring,std::string word,const std::vector<char> alphabet,const ScoreMatrix& matrix, int threads){
    if (pos==word_size){
        if (score>=score_threshold){
            substring.neighbors.emplace_back(word,score);
        }
    }    
    else{
        for (unsigned x=0;x<alphabet.size();++x){
            int scorenew = score+matrix.score(substring.infix[pos],alphabet[x]);
            findNeighborsRecursive(pos+1,word_size,scorenew,score_threshold,substring,word+alphabet[x],alphabet,matrix, threads);
        }
    }
}

std::vector<NHResult> BLAST_Neighborhood::generateNeighborhood(const std::string& query, const ScoreMatrix& matrix, const int word_size, const int score_threshold, const int threads){
    if (word_size<1){
        throw std::invalid_argument("word_size ist <1");
    }
    if (threads<=0){
        throw std::invalid_argument ("Die Anzahl an Threads ist <1");
    }
    if (word_size>int(query.size())){
        return {};
    }
    const std::vector <char> alphabet{'A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y'};
    std::vector<NHResult> res{};
    for (unsigned i=0;i<=query.size()-word_size;i++){
        res.push_back({query.substr(i,word_size),{}});
    }
    #pragma omp parallel num_threads(threads)
    {
    #pragma omp for nowait schedule(auto)
    for (unsigned i=0;i<=query.size()-word_size;++i){
        for (unsigned x=0;x<alphabet.size();++x){
            int score{matrix.score(res[i].infix[0],alphabet[x])};
            findNeighborsRecursive(1,word_size,score,score_threshold,res[i],std::string(1,alphabet[x]),alphabet,matrix,threads);
        }
    }
    }
    return res;
}
/*
int main(){
    ScoreMatrix mat = ScoreMatrix();
    mat.load("blosum62");
    BLAST_Neighborhood bl = BLAST_Neighborhood();
    bl.generateNeighborhood("AAHILNMY",mat,3,14,1);
}*/
