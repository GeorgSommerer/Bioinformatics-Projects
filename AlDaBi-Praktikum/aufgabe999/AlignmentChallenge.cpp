#include "AlignmentChallenge.h"

Alignment::Alignment(const int match, const int mismatch, const int gap){
    this->match=match;
    this->mismatch=mismatch;
    this->gap=gap;
}

int Alignment::compute(const std::vector<std::string>& seqs, const int threads){
    int total_score{};
    std::array<int,22801> DP_vec_all{};
    for (unsigned i=1;i<151;i++){
        *(DP_vec_all.begin()+i)=i*gap;
        *(DP_vec_all.begin()+i*151)=i*gap;
    }
    #pragma omp parallel for num_threads(threads) schedule(auto)
    for (auto it_m = seqs.cbegin(); it_m<seqs.cend();++it_m){
        int score_of_m{};
        std::array<int,22801> DP_vec=DP_vec_all;
        for (auto it_n=it_m+1;it_n<seqs.cend();++it_n){
            for (unsigned i=1;i<151;i++){
                const char current_m=*((*it_m).cbegin()+i-1);
                for (unsigned j=1;j<151;j++){
                    int fromUpLeft{};
                    if(current_m==*((*it_n).cbegin()+j-1)){
                        fromUpLeft=*(DP_vec.begin()+(i-1)*151+j-1)+match;
                    }
                    else{
                        fromUpLeft=*(DP_vec.begin()+(i-1)*151+j-1)+mismatch;
                    }   
                    *(DP_vec.begin()+i*151+j)=std::max(std::max(fromUpLeft,*(DP_vec.begin()+i*151+j-1)+gap),*(DP_vec.begin()+(i-1)*151+j)+gap);
                }
            }
            score_of_m+=DP_vec[DP_vec.size()-1];
        }
        #pragma omp critical
        {
            total_score+=score_of_m;
        }
    }
    return total_score;
}