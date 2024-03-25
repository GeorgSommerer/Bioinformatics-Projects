#036 - KMER - k-Mer Composition

#Goal: Find the 4-mer composition (the amount of 4-combinations lexicographically) of a DNA sequence.
#My approach: Using the cartesian product, create a dictionary of all 4 combinations, with a 0 assigned for each.
    #Then go through the input string and add 1 for each 4-mer found.
    #Lastly, output all the values from the dictionary.

from itertools import product

#Takes a string from a txt file in FASTA format.
def multiline_code(inp):
    f = open(inp,"r")
    return "".join(f.read().splitlines()[1:])

def k_mers(inp):
    seq = multiline_code(inp)
    kmers_list = list(product("ACGT",repeat=4))
    kmers_dict = {}
    for i in kmers_list:
        kmers_dict[("".join(i))]=0
    for i in range(len(seq)-3):
        kmers_dict[(seq[i:i+4])]+=1
    for v in kmers_dict.values():
        print(v,end=" ")

k_mers("rosalind_kmer.txt")