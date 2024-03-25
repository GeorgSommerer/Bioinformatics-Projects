#001 - DNA - Counting DNA Nucleotides:

#Goal: Count the amount of nucleotides.
#My approach: Create a Dictionary containing each nucleotide and the amount of occurences, then iterate through the sequence, adding to each dictionary entry when the respective base is encountered.

def nuc_count(inp):
    f = open(inp, "r")
    seq = f.readline().strip()
    nucs = {
        "A": 0,
        "C": 0,
        "G": 0,
        "T": 0
    }
    for i in seq:
        nucs[i]+=1
    print(str(nucs["A"]) + " " + str(nucs["C"]) + " " + str(nucs["G"]) + " " + str(nucs["T"]))

nuc_count("rosalind_dna.txt")