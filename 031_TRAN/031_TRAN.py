#031 - TRAN - Transitions and Transversions

#Goal: Find the number of transitions (point mutations of purine <-> purine or pyrimidine <-> pyrimidine) divided by the number of transversions (purine <-> pyrimidine).
#My approach: Whenever A and G or T and C have been swapped, add 1 to the transition counter.
    #Whenever A and T, A and C, C and G or G and T have been swappe, add 1 to the transversion counter.

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

def transition_transversion(inp):
    s1 = codetolist(inp)[0]
    s2 = codetolist(inp)[1]
    transitions = 0
    transversions = 0
    no_change=0
    for i in range(len(s1)):
        if s1[i]=="A" and s2[i]=="G" or s2[i]=="A" and s1[i]=="G" or s1[i]=="T" and s2[i]=="C" or s2[i]=="T" and s1[i]=="C":
            transitions+=1
        elif s1[i]=="A" and s2[i]=="C" or s2[i]=="A" and s1[i]=="C" or s1[i]=="T" and s2[i]=="G" or s2[i]=="T" and s1[i]=="G" or s1[i]=="A" and s2[i]=="T" or s2[i]=="A" and s1[i]=="T" or s1[i]=="C" and s2[i]=="G" or s2[i]=="C" and s1[i]=="G":
            transversions+=1
        else:
            no_change+=1
    return(transitions/transversions)

print(transition_transversion("rosalind_tran.txt"))