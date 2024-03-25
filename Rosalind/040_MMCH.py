#040 - MMCH - Perfect Matchings and RNA Secondary Structures

#Goal: Find the total number of perfect matchings of basepair edges given an unequal amount of unequal amount of bases.
#My approach: For each base pair, this is equal to finding the number of ordered k-combinations in n, where k is the minimum and n the maximum of the two bases.
    #(The idea is that k is the limiting factor and that in any case, all k have to bond to an amount of n equal to k).
    #The number of basepair edges is equal to the product of GC and AU.

from math import factorial

#Takes a string from a txt file in FASTA format.
def multiline_code(inp):
    f = open(inp,"r")
    return "".join(f.read().splitlines()[1:])

#(Probably) due to the size of the result, it is possible that the returned number is wrong. In that case, use the following code and enter the resulting equation into an online calculator like https://keisan.casio.com/calculator
def max_matchings(inp):
    seq = multiline_code(inp)
    if seq.count("G")<seq.count("C"):
        k1 = seq.count("G")
        n1 = seq.count("C")
    else:
        k1 = seq.count("C")
        n1 = seq.count("G")
    if seq.count("A")<seq.count("U"):
        k2 = seq.count("A")
        n2 = seq.count("U")
    else:
        k2 = seq.count("U")
        n2 = seq.count("A")
    print("("+str(n1)+"!*"+str(n2)+"!)/(("+str(n1)+"-"+str(k1)+")!*("+str(n2)+"-"+str(k2)+")!)")
    return int((factorial(n1)*factorial(n2))/(factorial(n1-k1)*factorial(n2-k2)))

print(max_matchings("rosalind_mmch.txt"))