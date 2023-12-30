#021 - REVP - Locating Restriction Sites:

#Goal: Return the position and length of every reverse palindrome in a string with length between 4 and 12.
#My approach: Go through the list, until you find 2 complementary bases (i and i+1) next to each other. Then, go back 1 base and see if i-1 and i+2 are the same, and so on.
    #Return, if the length of this palindrome is between 4 and 12.

#Converts a txt file in FASTA format to a list of the sequences.
def codetolist(inp):
    codelist=[]
    f = open(inp, "r")
    name = (f.readline())
    while ">" in name:
        code = (f.readline()).strip()
        code2 = (f.readline()).strip()
        while (">" not in code2) and (("G" or "C" or "A" or "T") in code2):
            code+=code2
            code2 = (f.readline()).strip()
        codelist.append(code)
        name = code2
    return codelist

#From 003:
def reverse_complement(seq):
    out = ""
    for i in seq:
        if i == 'T':
            out = out + "A"
        elif i == 'A':
            out = out + "T"
        elif i == 'G':
            out = out + "C"
        elif i == 'C':
            out = out + "G"
    return out[::-1]

def reverse_palindrome(inp):
    code = codetolist(inp)[0]
    res = []
    for i in range(1,len(code)-1):
        j=1
        while j-1<i and code[i-j:i]==reverse_complement(code[i:i+j]):
            if j>=2 and j<=6:
                res.append([i+1-j,2*j])
            j+=1
    res.sort()
    for n in res:
        print (str(n[0]) + " " + str(n[1]))
    
reverse_palindrome("rosalind_revp.txt")