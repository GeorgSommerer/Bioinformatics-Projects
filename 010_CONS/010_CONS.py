#010 - CONS - Consensus and Profile:

#Goal: Return a consensus string for a list of input strings, as well as the profile matrix, representing the sum of occurrences of each base at each position over every string.
#My approach: Create a matrix via numpy with a height of 4 (one for each base) and a width equal to the length of the input strings.
    #Then, go through each input string and add 1 for each occurrence to the correct row (facilitated via an enum) and column.
    #Using argmax with axis=0, we receive the row with the highest number for each column, which is converted to the corresponding base via the enum.
    #These bases are connected in order to form a consensus string.

import numpy as np
from enum import Enum

#Enumerates the DNA bases.
class BasesDNA(Enum):
    A = 0
    C = 1
    G = 2
    T = 3

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


def conseq(inp):
    codelist = codetolist(inp)
    codelen = len(codelist[0])
    mat = np.zeros((4,codelen),dtype=int) #A,C,G,T
    for n in codelist:
        for i in range(codelen):
            mat[BasesDNA[n[i]].value][i]+=1
    outp = ""
    maxvals = np.argmax(mat, axis=0)
    for n in maxvals:
        outp += BasesDNA(n).name
    print(outp)
    for i in range(4):
        print(BasesDNA(i).name + ": ",end=""),
        for j in range(codelen):
            print(str(mat[i][j]),end=" "),
        print()

conseq("rosalind_cons.txt")