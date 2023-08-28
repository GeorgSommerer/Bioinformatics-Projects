#016 - MPRT - Finding a Protein Motif:

#Goal: For every protein possessing the N-glycosylation motif N{P}[ST]{P}, output its access ID and the locations in the protein string where it can be found.
#My approach: First, retrieve the 1 letter sequence for each protein from the UniProt database and list them up.
    #From that, simply check for each string if it contains the motif (N, not P, S or T, not P) and print the protein's name and locations, if there are any.

import requests

#Reads the amino acid sequences from uniprot.org corresponding to the FASTA ids inputted through a txt file.
def aslist_from_uniprot_IDs(ids):
    f = open(ids,"r")
    outp=[]
    for line in f:
        coderaw = requests.get("https://rest.uniprot.org/uniprotkb/"+(line.split("_"))[0].strip()+".fasta").text
        tooutp = ""
        for i in range(1,len(coderaw.splitlines())):
            tooutp+=coderaw.splitlines()[i]
        outp.append(tooutp)
    f.close()
    return outp

def N_glycos_motif(inp):
    aslist = aslist_from_uniprot_IDs(inp)
    f = open(inp, "r")
    names = f.readlines()
    print(names)
    for i in range(len(names)):
        res = []
        for j in range(len(aslist[i])-3):
            if aslist[i][j]=="N" and aslist[i][j+1]!="P" and (aslist[i][j+2]=="S" or aslist[i][j+2]=="T") and aslist[i][j+3]!="P":
                res.append(j+1)
        if res != []:
            print(names[i].strip())
            for n in res:
                print(str(n),end=" ")
            print("")

N_glycos_motif("rosalind_mprt.txt")