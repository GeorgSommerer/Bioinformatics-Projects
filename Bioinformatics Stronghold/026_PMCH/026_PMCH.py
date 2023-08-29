#026 - PMCH - Perfect Matchings and RNA Secondary Structures:

#Goal: Find the total possible number of perfect matchings of basepair edges in the bonding graph, given that A=U and C=G
#My approach: The amount of possible combinations for AU-Pairs is count(A)! = count(U)! and for GC-Pairs count(C)! = count(G)!.

import math

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
def perfect_matchings(inp):
    seqs = codetolist(inp)[0]
    return math.factorial(seqs.count("A"))*math.factorial(seqs.count("G"))

print(perfect_matchings("rosalind_pmch.txt"))