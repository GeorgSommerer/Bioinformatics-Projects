#include "Alignment.hpp"

Alignment::Alignment(const std::string& seq_v, const std::string& seq_h) {
    this -> seq_v = seq_v;
    this -> seq_h = seq_h;
    score = 0;
    computed=false;    
    a1 = "";
    gaps = "";
    a2 = "";
    /*Ich habe mich für 2 Vektoren mit Bools, anstatt 1 Vektor mit Enums entschieden.
    Wenn Up_vec & Left_vec true sind, dann geht man nach links oben.
    Wenn beide false sind, endet das Alignment.
    Diese Variante müsste für fast alle Alignments platzgünstiger sein:
        1 Enum-Vektor benötigt 24+4(n+1)(m+1) Bytes Speicher
        2 Bool-Vektoren benötigen 2(24+(n+1)(m+1)) Bytes Speicher, was bereits für (n+1)(m+1)>=12 effizienter ist.
    */
}

int Alignment::getScore() const{
    if (computed){
        return this->score;
    }
    else{
        throw std::invalid_argument("Compute wurde nicht ausgeführt");
    }
}


void Alignment::getAlignment(std::string& a1, std::string& gaps, std::string& a2) const{
    if (computed){
        a1 = this->a1; a2 = this->a2; gaps = this->gaps;
        std::cout << a1 <<"\n" << gaps << "\n" << a2 << "\nscore:" << getScore()<<"\n";
    }
    else{
        throw std::invalid_argument("Compute wurde nicht ausgeführt");
    }
}


void Alignment::compute(const int match, const int mismatch, const int gap, const bool local_align) {
    std::vector<int> DP_vec((seq_v.size()+1)*(seq_h.size()+1),0);
    std::vector<bool> Up_vec((seq_v.size()+1)*(seq_h.size()+1),false);
    std::vector<bool> Left_vec((seq_v.size()+1)*(seq_h.size()+1),false);
    computed=true;
    if (!local_align||(local_align && gap>0)){
        for (unsigned i=1;i<=seq_h.size();i++){ //Befüllen der 1. Zeile
            DP_vec[i]=i*gap;
            Left_vec[i]=true;
        }
        for (unsigned i=1;i<=seq_v.size();i++){ //Befüllen der 1. Spalte
            DP_vec[i*(seq_h.size()+1)]=i*gap;
            Up_vec[i*(seq_h.size()+1)]=true;
        }  
    }
    int fromUpLeft{}; int fromUp{}; int fromLeft{}; int AlignEnd_v{}; int AlignEnd_h{};
    for (unsigned i=1;i<=seq_v.size();i++){
        for (unsigned j=1;j<=seq_h.size();j++){ //Gehe zeilenweise durch die Matrix
            if(seq_v[i-1]==seq_h[j-1]){ //Bei Match
                fromUpLeft = DP_vec[(i-1)*(seq_h.size()+1)+j-1]+match;
            }
            else{ //Bei Mismatch
                fromUpLeft = DP_vec[(i-1)*(seq_h.size()+1)+j-1]+mismatch;
            }
            fromLeft=DP_vec[i*(seq_h.size()+1)+j-1]+gap; //Gap in seq_v
            fromUp=DP_vec[(i-1)*(seq_h.size()+1)+j]+gap; //Gap in seq_h
            int maxVal{};
            if (!local_align){
                maxVal=std::max({fromUpLeft,fromLeft,fromUp});
            }
            else{
                maxVal=std::max({fromUpLeft,fromLeft,fromUp,0}); //Bei Smith-Waterman: Alle Werte sind >=0
            }
            if (maxVal==fromUpLeft){ //Zeige ins Feld links oben
                DP_vec[i*(seq_h.size()+1)+j]=fromUpLeft;
                Left_vec[i*(seq_h.size()+1)+j]=true;
                Up_vec[i*(seq_h.size()+1)+j]=true;
            }
            else if (maxVal==fromUp){ //Zeige ins Feld oben
                DP_vec[i*(seq_h.size()+1)+j]=fromUp;
                Up_vec[i*(seq_h.size()+1)+j]=true;
            }
            else if (maxVal==fromLeft){ //Zeige ins Feld links
                DP_vec[i*(seq_h.size()+1)+j]=fromLeft;
                Left_vec[i*(seq_h.size()+1)+j]=true;
            }
            else{ //Nur bei Smith-Waterman aufgerufen
                DP_vec[i*(seq_h.size()+1)+j]=0; 
            }
            if (local_align&&DP_vec[i*(seq_h.size()+1)+j]>DP_vec[AlignEnd_v*(seq_h.size()+1)+AlignEnd_h]){ //Wird bei Smith-Waterman genutzt, um das Ende des lokalen Alignments zu tracken
                AlignEnd_h=j;
                AlignEnd_v=i;
            }
        }
    }
    //Traceback; a1 gehört zu seqV, a2 zu seqH
    a1.clear(); a2.clear(); gaps.clear();
    unsigned traceback{};
    if (!local_align){ //Needleman-Wunsch: Starte im letzten Feld der Matrix
        AlignEnd_v=seq_v.size()-1;
        AlignEnd_h=seq_h.size()-1;
        traceback = DP_vec.size()-1;
    }
    else{ //Smith-Waterman: Starte am Feld mit dem höchsten Score
        traceback = AlignEnd_v*(seq_h.size()+1)+AlignEnd_h;
        AlignEnd_h-=1;AlignEnd_v-=1;
    }
    Alignment::score = DP_vec[traceback]; //Score kennt man bereits
    while (Left_vec[traceback]||Up_vec[traceback]){ //Solange man nach links, linksoben oder oben weitergehen kann, wird der Traceback fortgesetzt
        if (Left_vec[traceback]&&Up_vec[traceback]){ //Man geht nach links oben
            if (seq_h[AlignEnd_h]==seq_v[AlignEnd_v]){ //Match
                gaps = "|" + gaps;
            }
            else{ //Mismatch
                gaps = " " + gaps;
            }
            a1=seq_v[AlignEnd_v]+a1;
            AlignEnd_v--;
            a2 = seq_h[AlignEnd_h]+a2;
            AlignEnd_h--;
            traceback-=(seq_h.size()+2);
        }
        else if (Up_vec[traceback]){ //Man geht nach oben
            gaps = " " + gaps;
            a1=seq_v[AlignEnd_v]+a1;
            AlignEnd_v--;
            a2 = "-"+a2;
            traceback-=(seq_h.size()+1);
        }
        else if (Left_vec[traceback]){ //Man geht nach links
            gaps = " " + gaps;
            a1="-"+a1;
            a2 = seq_h[AlignEnd_h]+a2;
            AlignEnd_h--;
            traceback--;
        }
    }
}
/*
int main() {
    Alignment al = Alignment("IMISSMISSISSIPPI","MYMISSISAHIPPIE");
    al.compute(3,-4,-1,true);
    std::string g{"garb"};
    al.getAlignment(g,g,g);
    al.compute(3,-4,-6,false);
}*/ 