#include "aufgabe1.h"
void Horspool::setPattern(const std::string& pat){
    pattern=pat;
    for (char c : pat) {
        lookup_table[c]=size(pat);
    }
    for (unsigned j=0;j<size(pat)-1;j++) {
        lookup_table[pat[j]]=size(pat)-j-1;
    }
/*    for (auto const & [k,v] : lookup_table) {
        std::cout << k << " " << v << "\n";
    }*/
}

const std::string& Horspool::getPattern() const{
    return pattern;
}
std::vector<size_t> Horspool::getHits(const std::string& text) const{
    std::vector<size_t> hits={};
    size_t pos=0;
    if (text.size()==0||size(getPattern())==0){
        return hits;
    }
    while (pos<size(text)-size(getPattern())+1) {
        //std::cout << "pos " << pos << "\n";
        unsigned j=size(getPattern());
        alignCheck_(pos);
        while (j>0&&(text[pos+j-1]==getPattern()[j-1] ||text[pos+j-1]=='?'||getPattern()[j-1]=='?')) {
            //std::cout << "j: " << j << " text: " << text[pos+j-1] << " pattern: " << getPattern()[j-1] << "\n";
            j--;
        }
        if (j==0) {
            hits.push_back(pos);
        }
        //std::cout << "Shifted by: " << text[pos+size(getPattern())-1] << "\n";
        pos+=std::min(getShift_(text[pos+size(getPattern())-1]),getShift_('?'));
    }
    return hits;
}

uint32_t Horspool::getShift_(const char last_char) const{
    if (lookup_table.count(last_char)) {
        return lookup_table.at(last_char);
    }
    else {
        return size(getPattern());
    }
}