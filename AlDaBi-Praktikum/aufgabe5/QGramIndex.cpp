#include "QGramIndex.hpp"
#include "a5_util.hpp"

QGramIndex::QGramIndex(const std::string& text, const uint8_t q){
    if (q<1||q>13){
        throw std::invalid_argument("Invalid q!");
    }
    this->q=q;
    this->text=text;
    suftab.resize(text.size()-1);
    dir.resize(pow(4,q)+1); //Leere q-Gramm-Tabelle
    uint32_t hval=hash(text.substr(0,q)); //Befülle die q-Gramm-Tabelle
    dir[hval]++;
    for (unsigned i{};i<text.size()-q;i++){
        hval=hashNext(hval,text[i+q]);
        dir[hval]++;    
    }
    for (unsigned j{1};j<dir.size();j++){ //Bilde die kumulative Summe
        dir[j]+=dir[j-1];
    }
    hval=hash(text.substr(0,q)); //Bilde die fertige q-gramm-Tabelle und den fertigen suftab
    dir[hval]--;
    suftab[dir[hval]]=0;
    for (unsigned k{};k<text.size()-q;k++){ 
        hval=hashNext(hval,text[k+q]);
        dir[hval]--;
        suftab[dir[hval]]=k+1;
    } 
}

const std::string& QGramIndex::getText() const{
    return text;
}

 std::vector<uint32_t> QGramIndex::getHits(const uint32_t h) const{
    if (h>=dir.size()-1){
        throw std::invalid_argument("Invalid h!");
    }
    std::vector<uint32_t> hits{};
    for (uint32_t i{dir[h]};i<dir[h+1];i++){
        hits.push_back(suftab[i]);
    }
    return hits;
 }


uint8_t QGramIndex::getQ() const{
    return q;
}

uint32_t QGramIndex::hash(const std::string& qgram) const{
    if (qgram.size()!=q||qgram.size()>text.size()){
        throw std::invalid_argument("Invalid qgram!");
    }
    uint32_t hval{ordValue(qgram[0])};
    for (unsigned i=1;i<qgram.size();i++){
        hval<<=2;
        hval|=ordValue(qgram[i]);
    }
    return hval;
}

uint32_t QGramIndex::hashNext(const uint32_t prev_hash, const char new_pos) const{
    uint32_t hval = (prev_hash<<2) & ~(~0<<(2*getQ()));
    return hval|=ordValue(new_pos);
}

/*
int main(){
    QGramIndex qgram = QGramIndex("GATTACA",2);
    std::vector<uint32_t> res = qgram.getHits(qgram.hash("AT"));
    for (auto elem : res){
        std::cout << elem << "\n";
    }
}*/

//g++ -Wall -pedantic -O2 -D_GLIBCXX_ASSERTIONS -g -fsanitize=address -fopenmp QGramIndex.cpp a5_util.cpp -o qgram
