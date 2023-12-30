#041 - PDST - Creating a Distance Matrix

#Goal: Return the distance matrix, using the p-distance based on the percentage of differing symbols.
#My approach: Compare the strings pairwise and determine their hamming distance. Divide the result by the string length.

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

#From 006:
def point_mutations(base, test):
    ctr = 0
    for i in range(len(base)):
        if base[i] != test[i]:
            ctr+=1
    return ctr

def p_distance(inp):
    seqs = codetolist(inp)
    for k in seqs:
        for l in seqs:
            if k==l:
                print("0.0",end=" ")
            else:
                print(point_mutations(k,l)/len(k),end=" ")
        print()

p_distance("rosalind_pdst.txt")