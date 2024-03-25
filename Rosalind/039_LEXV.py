#039 - LEXV - Ordering Strings of Varying Length Lexicographically

#Goal: Print all strings from an lexicographically ordered alphabet: if s=t[1:m], then s<t; otherwise (s!=t) compare indexwise and compare if the letters are not the same at the same index.
#My approach: Using recursively implemented nested for-loops, we can print all strings in the right order.

def lex_order_help(lexicon,k,n,f):
    if len(n)<k:
        for i in range(len(lexicon)):
            f.write(n+lexicon[i]+"\n")
            lex_order_help(lexicon,k,n+lexicon[i],f)

def lex_order(inp,outp):
    g=open(inp,"r")
    temp = g.read().splitlines()
    lexicon = temp[0].split()
    f=open(outp,"w")
    lex_order_help(lexicon,int(temp[1]),"",f)
    f.close()

lex_order("rosalind_lexv.txt","rosalind_lexv_output.txt")