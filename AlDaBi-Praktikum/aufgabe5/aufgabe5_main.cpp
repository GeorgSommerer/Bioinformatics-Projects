#include "QGramIndex.hpp"
#include "a5_util.hpp"

int main(int argc,const char* args[]){
    if (argc!=3){
        throw std::invalid_argument("Invalid input");
    }   
    std::string text{};
    std::string query{args[2]};
    std::ifstream genome_file(args[1]);
    getline(genome_file,text);
    QGramIndex qgram = QGramIndex(text,query.size());
    std::vector<uint32_t> hits{qgram.getHits(qgram.hash(query))};
    std::cout << query <<":";
    for (uint32_t hit :  hits){
        std::cout << " " << hit;
    }
    std::cout << "\n";
    genome_file.close();
}