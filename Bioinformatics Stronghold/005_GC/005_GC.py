#005 - GC - Computing GC Content:

#Goal: Find the DNA sequence with the highest GC content.
#My approach: Create a dictionary associating each sequence with its FASTA name. Then, create a running variable for the maximum GC-content and the corresponding name
    #and iterate through each entry. If the sum of the amount of G and C divided by the length of the sequence is greater than the current maximum, replace it.

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

def max_gc(inp):
    seq_array = codetodict(inp)
    max_key = ""
    max_val = 0.0
    for k,v in seq_array.items():
        gc_content = (v.count("G")+v.count("C"))*100/len(v.strip())
        if gc_content > max_val:
            max_key = k
            max_val = gc_content
    print(max_key)
    print(max_val)
        
             
max_gc("rosalind_gc.txt")