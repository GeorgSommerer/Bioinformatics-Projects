#012 - GRPH - Overlap Graphs:

#Goal: Return the names of all sequences with an adjacency of 3, meaning that the last 3 bases of one string correspond to the first 3 bases of another string.
#My approach: Go through every pair in the list and output their names if they are 3-adjacent.

#Converts a txt file in FASTA format to a dictionary, where the sequences are assigned to the corresponding names.
def codetodict(inp):
    genes = {}
    f = open(inp, "r")
    name = (f.readline())
    while ">" in name:
        code = (f.readline()).strip()
        code2 = (f.readline()).strip()
        while (">" not in code2) and (code2!="") and (("G" or "C" or "A" or "T") in code2):
            code+=code2
            code2 = (f.readline()).strip()
        genes[name.strip(">\n")] = code
        name = code2
    return genes

def overlap(inp,k):
    code = codetodict(inp)
    keylist = list(code.keys())
    valuelist = list(code.values())
    for i in range(len(valuelist)):
        for j in range(len(valuelist)):
            if valuelist[i][len(valuelist[i])-k:len(valuelist[i])] == valuelist[j][:k] and i!=j:
                print(keylist[i] + " " + keylist[j])

overlap("rosalind_grph.txt",3)