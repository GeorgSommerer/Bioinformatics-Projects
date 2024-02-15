#include "aufgabe2.hpp"
#include <algorithm>
#include <iostream>
#include <numeric>
#include <stdint.h>
#include <cmath>
#include <tuple>

void construct(std::vector<uint32_t> & sa, const std::string& text) {
    if (text.size()!=0) {
        sa.resize(text.size());
        std::iota(sa.begin(),sa.end(),0);
        auto comparevecs = [text] (uint32_t a, uint32_t b) {
            uint32_t i{};
            while (text[a+i]==text[b+i]&&a+i<text.size()&&b+i<text.size()){
                i++;
            }
            if (a+i==text.size()) {
                return true;
            }
            if (b+i==text.size()) {
                return false;
            }
            else {
                return text[i+a]<text[i+b];
            }
        };
        std::sort(sa.begin(),sa.end(), comparevecs);
            /*Zeit an meinem eigenen Rechner: ca. 3300ms>100ms. Ich weiß aber auch nicht, wie man die Zeit reduzieren würde,
            wenn man wirklich std::sort verwendet.
            Im Array selbst werden ja nur Zahlen sortiert, wie von der Aufgabenstellung verlangt.
            Aber bei der Sortierung muss man ja zwangsläufig die Substrings miteinander vergleichen, was Zeit kostet.
            Und ich glaube nicht, dass im Allgemeinen eine bessere Implementierung für das lexikographische Vergleichen als in das
            aus der STL existiert.*/
    }
    else {
        sa = {};
    }
}

/*std::tuple<bool,uint32_t> compare_with_text_lp(const std::string& query, const std::string& text,uint32_t start_compare,const uint32_t start_in_text){
    bool b;
    while(query[start_compare]==text[start_compare+start_in_text]&&start_compare<query.size()&&start_compare<text.size()){
        start_compare++;
    }
    if (start_compare==query.size()){
        b=false;
    }
    else if (start_compare==text.size()){
        b=true;
    }
    else{
        if (query[start_compare]<=text[start_compare+start_in_text]){
            b=false;
        }
        else{
            b=true;
        }
    }
    return std::tie(b,start_compare);
}*/

std::tuple<bool,uint32_t> compare_with_text_lp(const std::string& query, const std::string& text,uint32_t start_compare,const uint32_t start_in_text){
    bool b;
    while (query[start_compare]==text[start_compare+start_in_text]&&start_compare<query.size()&&start_compare<text.size()){
        //std::cout << query[start_compare]<<"=="<<text[start_compare+start_in_text]<<"\n";
        start_compare++;
    }
    if (query[start_compare]<=text[start_compare+start_in_text]||query.size()<start_compare){
        //std::cout << query[start_compare]<<"<="<<text[start_compare+start_in_text]<<"\n";
        b=false;
    }
    else{
        //std::cout << query[start_compare]<<">"<<text[start_compare+start_in_text]<<"\n";
        b=true;
    }
    return std::tie(b,start_compare);
}
std::tuple<bool,uint32_t> compare_with_text_rp(const std::string& query, const std::string& text,uint32_t start_compare,const uint32_t start_in_text){
    bool b;
    while(query[start_compare]==text[start_compare+start_in_text]&&start_compare<query.size()&&start_compare<text.size()){
        start_compare++;
    }
    if (start_compare==query.size()){
        if (query[start_compare-1]==text[start_compare+start_in_text-1]){
            b=false;
        }
        else{//?
            b=true;
        }
    }
    else if (start_compare==text.size()){
        b=false;
    }
    else{
        if (query[start_compare]>=text[start_compare+start_in_text]){
            b=false;
        }
        else{
            b=true;
        }
    }
    return std::tie(b,start_compare);
}
/*
std::tuple<bool,uint32_t> compare_with_text_rp(const std::string& query, const std::string& text,uint32_t start_compare,const uint32_t start_in_text){
    bool b;
    while (query[start_compare]==text[start_compare+start_in_text]&&start_compare<query.size()&&start_compare<text.size()){
        //std::cout << query[start_compare]<<"=="<<text[start_compare+start_in_text]<<"\n";
        start_compare++;
    }
    if (query[start_compare]>=text[start_compare+start_in_text]||(query[start_compare-1]==text[start_compare+start_in_text-1]&&query.size()<start_compare)){
        //std::cout << query[start_compare]<<">="<<text[start_compare+start_in_text]<<"\n";
        b=false;
    }
    else{
        //std::cout << query[start_compare]<<"<"<<text[start_compare+start_in_text]<<"\n";
        b=true;
    }
    return std::tie(b,start_compare);
}*/

uint32_t generate_lcp(const std::string& str1,const std::string& str2,const uint32_t start_in_text1,const uint32_t start_in_text2){
    uint32_t i{};
    while (str1[start_in_text1+i]==str2[start_in_text2+i]&&start_in_text1+i<str1.size()&&start_in_text2+i<str2.size()){
        i++;
    }
    return i;
}

uint32_t find_Lp(const std::string& query, const std::vector<uint32_t>& sa, const std::string& text,uint32_t l, uint32_t r, uint32_t L, uint32_t R,std::vector<uint32_t>& lcp_vec){
        //std::cout << "Lp: L: " << L << " R: " << R << " l: " << l << " r: " << r;
    if (R-L<=1) {
        //std::cout << " Lp: " << R << "\n";
        return R;
    }
    else {
        uint32_t M = std::ceil((L+R)*0.5);
        //std::cout << " M: " << M << "\n";
        if (l==r) {
            std::tuple <bool,uint32_t> res = compare_with_text_lp(query,text,l,sa[M]);
            if (std::get<bool>(res)==false){
                R=M;
                r=std::get<uint32_t>(res);
            }
            else {
                L=M;
                l=std::get<uint32_t>(res);
            }
        }
        else if (l<r) {
            //std::cout << "l<r\n";
            uint32_t lcp= *std::min_element(lcp_vec.begin()+M,lcp_vec.begin()+R);
            if (lcp<r){
                L=M;
                l=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp>r){
                R=M;
                r=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp==r){
                std::tuple <bool,uint32_t> res = compare_with_text_lp(query,text,lcp,sa[M]);
                if (std::get<bool>(res)==false){
                    R=M;
                    r=std::get<uint32_t>(res);
                }
                else {
                    L=M;
                    l=std::get<uint32_t>(res);
                } 
            }
        }
        else if (l>r) {
            uint32_t lcp=*std::min_element(lcp_vec.begin()+L,lcp_vec.begin()+M);
            if (lcp<l){
                R=M;
                r=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp>l){
                L=M;
                l=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp==l){
                std::tuple <bool,uint32_t> res = compare_with_text_lp(query,text,lcp,sa[M]);
                if (std::get<bool>(res)==false){
                    R=M;
                    r=std::get<uint32_t>(res);
                }
                else {
                    L=M;
                    l=std::get<uint32_t>(res);
                } 
            }
        }
    }
    return find_Lp(query, sa, text, l, r, L,R,lcp_vec);
}
uint32_t find_Rp(const std::string& query, const std::vector<uint32_t>& sa, const std::string& text,uint32_t l, uint32_t r, uint32_t L, uint32_t R,std::vector<uint32_t>& lcp_vec){
    //std::cout << "Rp: L: " << L << " R: " << R << " l: " << l << " r: " << r;
    if (R-L<=1) {
        //std::cout << " Rp: " << L << "\n";
        return L;
    }
    else {
        uint32_t M = std::ceil((L+R)*0.5);
        //std::cout << " M: " << M << "\n";
        if (l==r) {
            //std::cout <<"l=r\n";
            std::tuple <bool,uint32_t> res = compare_with_text_rp(query,text,l,sa[M]);
            if (std::get<bool>(res)==false){
                L=M;
                l=std::get<uint32_t>(res);
            }
            else {
                R=M;
                r=std::get<uint32_t>(res);
            }
        }
        else if (l<r) {
            uint32_t lcp=*std::min_element(lcp_vec.begin()+M,lcp_vec.begin()+R);
            //std::cout << "lcp: " << lcp << "\n";
            if (lcp<r){
                L=M;
                l=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp>r){
                R=M;
                r=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp==r){
                std::tuple <bool,uint32_t> res = compare_with_text_rp(query,text,lcp,sa[M]);
                if (std::get<bool>(res)==false){
                    L=M;
                    l=std::get<uint32_t>(res);
                }
                else {
                    R=M;
                    r=std::get<uint32_t>(res);
                } 
            }
        }
        else if (l>r) {
            uint32_t lcp=*std::min_element(lcp_vec.begin()+L,lcp_vec.begin()+M);
            if (lcp<l){
                R=M;
                r=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp>l){
                L=M;
                l=std::min(static_cast<uint32_t>(query.size()),lcp);
            }
            else if (lcp==l){
                std::tuple <bool,uint32_t> res = compare_with_text_rp(query,text,lcp,sa[M]);
                if (std::get<bool>(res)==false){
                    L=M;
                    l=std::get<uint32_t>(res);
                }
                else {
                    R=M;
                    r=std::get<uint32_t>(res);
                } 
            }
        }
    }
    return find_Rp(query, sa, text, l, r, L,R,lcp_vec);
}
void find(const std::string& query, const std::vector<uint32_t>& sa, const std::string& text, std::vector<uint32_t>& hits) {
    hits={};
    if ((text.size()>1&&query.size()>=1)||(text.size()==1&&query==text)){
        uint32_t Lp{};
        uint32_t Rp{};
        std::vector<uint32_t>lcp_vec{};
        for(uint32_t i{};i<sa.size()-1;i++){
            lcp_vec.push_back(generate_lcp(text,text,sa[i],sa[i+1]));
        }
        uint32_t l=generate_lcp(query,text,0,sa[0]);
        uint32_t r=generate_lcp(query,text,0,sa[sa.size()-1]);
        if (generate_lcp(query,text,0,sa[0])==query.size()){
            Lp=0;
        }
        else {
            Lp = find_Lp(query, sa, text, l, r, 0, sa.size()-1,lcp_vec);
        }
        if (generate_lcp(query,text,0,sa[sa.size()-1])==query.size()){
            Rp=sa.size()-1;
        }
        else{
            Rp = find_Rp(query,sa,text,l,r,0,sa.size()-1,lcp_vec);
        }
        for (uint32_t i=Lp;i<=Rp;i++){
            hits.push_back(sa[i]);
        }
        std::sort(hits.begin(),hits.end());
    }
}
/*
int main() {
    std::string text = "bananpank";
    std::string query = "ba";
    std::vector<uint32_t> sa{};
    construct(sa, text);
   for (uint32_t elem:sa){
        //std::cout << elem << "\n";
    }
    std::vector<uint32_t> hits{};
    find(query,sa,text,hits);
    //std::cout << query<<":";
    for (uint32_t & elem : hits) {
        //std::cout << " "<< elem;
    }
    //std::cout << "\n";
}*/