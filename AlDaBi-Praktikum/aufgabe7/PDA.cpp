#include "PDA.hpp"

PDA::PDA(const Language l){

    std::stack<char> new_stack;
    new_stack.push('S');
    pda_stack.swap(new_stack);
    current_state = State::IN_PROGRESS;
    switch (l){
        case Language::BRACKETS:
        break;
        default:
        nonterminals = {'S','V','W','X','Y'};
        transitions = {
            {'S',{"aVu","cVg","gVc","uVa"}},
            {'V',{"aWu","cWg","gWc","uWa"}},
            {'W',{"aXu","cXg","gXc","uXa"}},
            {'X',{"gYa"}},
            {'Y',{"aa","ca"}}
        };
    }
}

PDA::State PDA::next(const char a){
    if (current_state == State::FAIL){
        return current_state;
    }
    else if (pda_stack.empty()){
        if (a == '$'){
            current_state = State::SUCCESS;
            return current_state;
        }
        else {
            current_state = State::FAIL;
            return current_state;
        }
    } 
    if (std::count(nonterminals.begin(),nonterminals.end(),pda_stack.top())){
        bool found_transition = false;
        for (std::string out : transitions.at(pda_stack.top())){
            if (out[0] == a){
                found_transition = true;
                pda_stack.pop();
                for (unsigned i{0};i<out.size()-1;i++){
                    pda_stack.push(out[out.size()-i-1]);
                }
                break;
            }
        }
        if (!found_transition){
            current_state = State::FAIL;
        }
    }
    else if (pda_stack.top() == a){
        pda_stack.pop();
    }
    else{
        current_state = State::FAIL;
    }
    return current_state;
}

void PDA::reset(){
    std::stack<char> new_stack;
    new_stack.push('S');
    pda_stack.swap(new_stack);
    current_state = State::IN_PROGRESS;
}
/*
int main(){
    std::string text{"gccgcaaggc$"};
    PDA my_pda;
    PDA::State b;
    for (char a : text){
        b = my_pda.next(a);
    }
    std::cout << static_cast<int>(b)<<"\n";
}*/