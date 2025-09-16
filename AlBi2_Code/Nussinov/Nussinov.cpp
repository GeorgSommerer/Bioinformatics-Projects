#include "Nussinov.h"


nus::nus(const std::string& rna, ulong gap_size, const struct scoring_scheme scores){
    this -> rna = rna;
    this -> gap_size = gap_size;
    this -> scores = scores;
    score_matrix.assign(this-> rna.size(), std::vector<int>(this->rna.size(),0));
    traceback_matrix.assign(this-> rna.size(), std::vector<int>(this->rna.size(),-1));
}

void nus::setSS(const struct scoring_scheme scores){
    this -> scores = scores;
}

std::tuple<std::string, int> nus::fillMatrix(){
    
    for (uint l = gap_size; l<rna.size(); l++){
        for (uint i = 0; i < rna.size()-l; i++){ //go through matrix diagonally; j=i+l, where l is the current offset to the right

            int score_pair = 0;
            int score_multi = 0;
            int traceback_multi = -1;
            // 4 cases in the step of the algorithm
            if ((rna[i] == 'A' && rna[i+l] == 'U') || (rna[i] == 'U' && rna[i+l] == 'A') || (rna[i] == 'G' && rna[i+l] == 'C') || (rna[i] == 'C' && rna[i+l] == 'G')){
                score_pair = score_matrix[i+1][i+l-1] + scores.pair;
            }
            int score_rowgap = score_matrix[i+1][i+l] + scores.nonpair;
            int score_colgap = score_matrix[i][i+l-1] + scores.nonpair;
            for (uint k = i+1; k < i+l; k++){
                int score_multi_cur = score_matrix[i][k] + score_matrix[k+1][i+l];
                if (score_multi_cur > score_multi){
                    score_multi = score_multi_cur;
                    traceback_multi = k;
                }
            }
            //find maximum and adjust matrices accordingly
            std::vector<int> score_list = {score_pair, score_rowgap, score_colgap, score_multi};
            
            int max_score = *std::max_element(score_list.begin(),score_list.end());
            //std::cout << "[" << i << "," << i+l << "], " << rna[i] << rna[i+l] << ", " << max_score<< std::endl;

            if (max_score == score_colgap){
                score_matrix[i][i+l] = score_colgap;
                traceback_matrix[i][i+l] = -2;
            }
            else if (max_score == score_rowgap){
                score_matrix[i][i+l] = score_rowgap;
                traceback_matrix[i][i+l] = -3;
            }
            else if (max_score == score_pair){
                score_matrix[i][i+l] = score_pair;
                traceback_matrix[i][i+l] = -4;
            }
            else if (max_score == score_multi){
                score_matrix[i][i+l] = score_multi;
                traceback_matrix[i][i+l] = traceback_multi;
            }
            else{
                std::cerr << "This case should not occur." << std::endl;
            }
        }
    }
    /*
    for (auto & elem : traceback_matrix){
        for (auto & elem2 : elem){
            std::cout << elem2 << " ";
        }
        std::cout << std::endl;
    }
    for (auto & elem : score_matrix){
        for (auto & elem2 : elem){
            std::cout << elem2 << " ";
        }
        std::cout << std::endl;
    }
        */
    return std::tuple{traceback(0, rna.size()-1),score_matrix[0][rna.size()-1]};
}


std::string nus::traceback(uint i, uint j) const {
    std::string l_structure, r_structure = "";
    bool not_ended = true;
    while (not_ended){
        //std::cout << i << " " << j << "\t" << l_structure << " " << r_structure << std::endl;
        if (traceback_matrix[i][j] == -2){
            r_structure = "*" + r_structure;
            j = j-1;
        }
        else if (traceback_matrix[i][j] == -3){
            l_structure = l_structure + "*";
            i = i+1;
        }
        else if (traceback_matrix[i][j] == -4){
            l_structure = l_structure + "(";
            r_structure = ")" + r_structure;
            i = i+1;
            j = j-1;
        }
        else if (traceback_matrix[i][j] >= 0){
            std::string l_sub = traceback(i,traceback_matrix[i][j]);
            std::string r_sub = traceback(traceback_matrix[i][j]+1,j);
            l_structure = l_structure + l_sub;
            r_structure = r_sub + r_structure;
            break;
        }
        else if (traceback_matrix[i][j] == -1){
            not_ended = false;
            int diff = i-j;
            l_structure = l_structure + std::string(1+abs(diff),'*');
        }
        else{
            std::cerr << "This case should not occur" << std::endl;
        }
    }
    return l_structure + r_structure;
}