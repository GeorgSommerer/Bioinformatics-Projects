#include "ACTrie.hpp"

ACTrie::ACTrie(const std::vector<std::string>& needles){
    if (needles.size()==0){
        throw std::logic_error("Der Needle-Vektor darf nicht leer sein.");
    }
    for (std::string needle : needles){
        for (char c : needle){
            if (int(c)<65||int(c)>90){
                throw std::invalid_argument("Die Needles dürfen nur Großbuchstaben von A bis Z enthalten.");
            }
        }
    }
    this->needles = needles;
    //Trie-Konstruktion:
    ACNode root{false,'0',0,0,0,0,{},{},0};
    trie = {root};
    for (unsigned i{}; i<needles.size();i++){
        Index parent = 0;
        Index current = 0;
        for (unsigned j{};j<needles[i].size();j++){
            bool add_new = true;
            for (auto find_children : trie[current.pos()].i_children){
                if (trie[find_children.pos()].c_current == needles[i][j]){
                    add_new = false;
                    current = find_children.pos();
                    break;
                }
            }
            if (add_new){
                current = trie.size();
                trie[parent.pos()].i_children.push_back(current);
                ACNode new_node{false,needles[i][j],current,0,0,parent,{},{},trie[parent.pos()].depth+1};
                trie.push_back(new_node);
            }
            if (j==needles[i].size()-1){
                trie[current.pos()].is_terminal=true;
                trie[current.pos()].needle_indices.push_back(i);
            }
            parent = current;
        }
    }
    for (ACNode& node : trie){
        std::sort(node.i_children.begin(),node.i_children.end(),[this](Index a, Index b){return trie[a.pos()].c_current < trie[b.pos()].c_current;});
    }
    //Erzeugen der Suffix-Links:
    std::vector<Index> queue{};
    for (Index child : trie[0].i_children){
        queue.insert(queue.end(),trie[child.pos()].i_children.begin(),trie[child.pos()].i_children.end());
    }
    while (queue.size()!=0){
        std::vector<Index> next_queue{};
        for (unsigned i{};i<queue.size();i++){
            bool at_root = false;
            next_queue.insert(next_queue.end(),trie[queue[i].pos()].i_children.begin(),trie[queue[i].pos()].i_children.end());
            bool supplied = false;
            Index current = queue[i];
            Index parent_suffix=trie[trie[current.pos()].parent.pos()].suffix_link;
            while ((supplied==false)&(at_root==false)){
                for (auto suffix_children : trie[parent_suffix.pos()].i_children){
                    if (trie[suffix_children.pos()].c_current == trie[current.pos()].c_current){
                        supplied = true;
                        trie[current.pos()].suffix_link=suffix_children;
                        //trie[current.pos()].needle_indices.insert(trie[current.pos()].needle_indices.end(),trie[suffix_children.pos()].needle_indices.begin(),trie[suffix_children.pos()].needle_indices.end()); //Diese Zeile würde dafür sorgen, dass in Needle-Indices auch alle Nadeln, die durch die Output-Links gefunden würden, in diesem Vektor gespeichert würden.
                        bool find_output_link = trie[suffix_children.pos()].is_terminal;
                        while ((!find_output_link)&(suffix_children.pos()!=0)){
                            suffix_children = trie[suffix_children.pos()].suffix_link;
                            find_output_link = trie[suffix_children.pos()].is_terminal;
                        }
                        trie[current.pos()].output_link=suffix_children;
                        break;
                    }
                } 
                Index new_parent_suffix = trie[parent_suffix.pos()].suffix_link;
                if (new_parent_suffix.pos() == parent_suffix.pos()){
                    at_root=true;
                }
                parent_suffix=new_parent_suffix;
            }
        }
        queue=next_queue;
    }
    /*for (auto node : trie){
        std::cout << "=============\n";
        std::cout << "Terminal?: " << node.is_terminal << "\n";
        std::cout << "Char: " << node.c_current << "\n";
        std::cout << "Index: " << node.i_current.pos() << " ("<<trie[node.i_current.pos()].c_current <<")\n";
        std::cout << "Suffix-Link: " << node.suffix_link.pos() << " ("<<trie[node.suffix_link.pos()].c_current <<")\n";
        std::cout << "Output-Link: " << node.output_link.pos() << " ("<<trie[node.output_link.pos()].c_current <<")\n";
        std::cout << "Parent: " << node.parent.pos() << " ("<<trie[node.parent.pos()].c_current <<")\n";
        std::cout << "Kinder:";
        for (auto child : node.i_children){
            std::cout << " " << child.pos() << " ("<<trie[child.pos()].c_current <<"),";
        }
        std::cout << "\n";
        std::cout << "Needles:";
        for (auto child : node.needle_indices){
            std::cout << " " << child.pos() << " ("<<needles[child.pos()] <<"),";
        }
        std::cout << "\n";
        std::cout << "Tiefe: " << node.depth << "\n";
    }*/
}


std::string ACTrie::getTree() const{
    std::string res="0"+getTree_help(0);
    return res;
}

std::string ACTrie::getTree_help(Index current) const{
    std::string res="";
    for(Index child : trie[current.pos()].i_children){
        res+="(";
        res+=trie[child.pos()].c_current;
        if (trie[child.pos()].i_children.size()!=0){
            res+=getTree_help(child);
        }
        res+=")";
    }
    return res;
}


void ACTrie::setQuery(const std::string& haystack){
    this->haystack = haystack;
    current_pos_haystack=0;
    current_node=0;
}


bool ACTrie::next(std::vector<Hit>& hits){
    hits = {};
    bool found_new = false;
    char current_c_haystack{};
    while (current_pos_haystack<haystack.size()&&found_new==false){
        current_c_haystack=haystack[current_pos_haystack];
        bool at_root = false;
        bool found_next = false;
        while(at_root==false&&found_next==false){
            if ((trie[current_node.pos()].suffix_link.pos())==current_node.pos()){
                at_root=true;
            }
            for (auto find_children : trie[current_node.pos()].i_children){
                if (trie[find_children.pos()].c_current == current_c_haystack){
                    found_next = true;
                    current_node = find_children.pos();
                    break;
                }
            }
            if (!found_next){
                current_node = trie[current_node.pos()].suffix_link;
            }
        }
        if (trie[current_node.pos()].output_link.pos()!=0||trie[current_node.pos()].is_terminal){
            found_new=true;
            Index traceback = current_node;
            do{
                for (Index needle : trie[traceback.pos()].needle_indices){
                    Hit new_hit(needle.pos(),current_pos_haystack-trie[traceback.pos()].depth+1);
                    hits.push_back(new_hit);
                }
                traceback=trie[traceback.pos()].output_link;
            }while(trie[traceback.pos()].output_link.pos()!=traceback.pos());
        }
        current_pos_haystack++;
    }
    return found_new;
}

/*
int main(){
    std::vector<std::string> needles{"TT","ATT","ATT","A"};
    ACTrie test_trie = ACTrie(needles);
    std::cout << test_trie.getTree() << "\n";
    std::string haystack="GATTACA";
    test_trie.setQuery(haystack);
    std::vector<Hit> hits{};
    bool not_finished = true;
    while (not_finished){
        not_finished = test_trie.next(hits);
    }
    for (Hit hit : hits){
        std::cout << needles[hit.index] << " " << hit.pos << "\n";
    }
}*/