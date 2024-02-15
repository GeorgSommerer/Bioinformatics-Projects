#include "ACTrie.hpp"

int main(int argc,const char* args[]){
    if (argc<2){
        throw std::invalid_argument("Invalid input");
    }   
    std::string haystack=args[1];
    std::vector<std::string> needles{};
    for (int i=2;i<argc;i++){
        needles.push_back(args[i]);
    }
    ACTrie this_trie = ACTrie(needles);
    std::cout << this_trie.getTree() << "\n";
    
    this_trie.setQuery(haystack);
    std::vector<Hit> hits{};
    std::vector<std::vector<Hit>> got{};
    while (this_trie.next(hits)){
        got.push_back(hits);
    }
    std::cout << "Hits (position in query, pattern):\n";
    for (std::vector<Hit> hit2 : got){
        for (Hit hit : hit2){
            std::cout << "pos" << hit.pos << ", " << needles[hit.index] << "\n";
        }
    }
}