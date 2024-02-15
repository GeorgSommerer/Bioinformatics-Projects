#include <omp.h>
#include "BLAST_Neighborhood.hpp"
#include "a4_util.h"

int main(int argc,const char* args[]){
    if (argc!=6){
        throw std::invalid_argument("Invalid Input");
    }
    ScoreMatrix mat = ScoreMatrix();
    mat.load(args[2]);
    BLAST_Neighborhood bl = BLAST_Neighborhood();
    double start = omp_get_wtime();
    std::vector<NHResult> res = bl.generateNeighborhood(args[1],mat,std::stoi(args[3]),std::stoi(args[4]),std::stoi(args[5]));
    double end = omp_get_wtime();
    for (auto elem : res){
        std::cout << elem.infix << ":";
        for (auto elem2 : elem.neighbors) {
            std::cout << " (" << elem2.first << ", " << elem2.second << ")";
        }
        std::cout << "\n";
    }
    std::cout << "time: " << end-start << "s\n";
}
