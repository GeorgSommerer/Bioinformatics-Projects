#046 - EDIT - Edit Distance:

#Goal: Find the amount of substitutions, insertion, and deletions necessary to transform the two input protein sequences into one another.
#My approach: Calculate the Levenshtein distance using the Wagner-Fisher-Algorithm in a similar manner as in 038 - LCSQ.
    #But this time, we don't need to trace back any sequence, so 1 matrix suffices.

import numpy as np

def codetolist(inp):
    codelist=[]
    f = open(inp, "r")
    name = (f.readline())
    while ">" in name:
        code = (f.readline()).strip()
        code2 = (f.readline()).strip()
        while (">" not in code2) and len(code2)!=0:
            code+=code2
            code2 = (f.readline()).strip()
        codelist.append(code)
        name = code2
    return codelist

def edit_distance(inp):
    prots = codetolist(inp)
    s1 = prots[0]
    s2 = prots[1]
    #Set up matrix:
    leven_matrix = np.tile(0,(len(s1)+1,len(s2)+1))
    for i in range(len(s1)+1):
        leven_matrix[i][0]=i
    for i in range(len(s2)+1):
        leven_matrix[0][i]=i
    #Compute the content of the matrix:
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if s1[i-1]==s2[j-1]:
                leven_matrix[i][j]=leven_matrix[i-1][j-1]
            else:
                leven_matrix[i][j]=min(leven_matrix[i-1][j-1],leven_matrix[i-1][j],leven_matrix[i][j-1])+1
    return leven_matrix[i][j]

print(edit_distance("rosalind_edit.txt"))