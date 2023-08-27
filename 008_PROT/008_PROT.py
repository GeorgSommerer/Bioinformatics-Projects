#008 - PROT - Translating RNA into Protein:

#Goal: Convert an RNA string into a protein string.
#My approach: Create a dictionary relating codons and amino acids. Then, check if the RNA string starts with the starting codon AUG.
    #If that is the case, go through the string in triplets and append the corresponding 1 letter code to the protein string.
    #If a stop codon is encountered, abort the translation and return the protein string.

#Dict assigning the 1 letter code of each amino acid to every corresponding codon.
codons_to_as_dict = {
        "UUU":"F",
        "UUC":"F",
        "UUA":"L",
        "UUG":"L",
        "UCU":"S",
        "UCC":"S",
        "UCA":"S",
        "UCG":"S",
        "UAU":"Y",
        "UAC":"Y",
        "UGU":"C",
        "UGC":"C",
        "UGG":"W",
        "CUU":"L",
        "CUC":"L",
        "CUA":"L",
        "CUG":"L",
        "CCU":"P",
        "CCC":"P",
        "CCA":"P",
        "CCG":"P",
        "CAU":"H",
        "CAC":"H",
        "CAA":"Q",
        "CAG":"Q",
        "CGU":"R",
        "CGC":"R",
        "CGA":"R",
        "CGG":"R",
        "AUU":"I",
        "AUC":"I",
        "AUA":"I",
        "AUG":"M",
        "ACU":"T",
        "ACC":"T",
        "ACA":"T",
        "ACG":"T",
        "AAU":"N",
        "AAC":"N",
        "AAA":"K",
        "AAG":"K",
        "AGU":"S",
        "AGC":"S",
        "AGA":"R",
        "AGG":"R",
        "GUU":"V",
        "GUC":"V",
        "GUA":"V",
        "GUG":"V",
        "GCU":"A",
        "GCC":"A",
        "GCA":"A",
        "GCG":"A",
        "GAU":"D",
        "GAC":"D",
        "GAA":"E",
        "GAG":"E",
        "GGU":"G",
        "GGC":"G",
        "GGA":"G",
        "GGG":"G",
        "UAG":"Stop",
        "UAA":"Stop",
        "UGA":"Stop"
    }

def toprotein(inp):
    f = open(inp, "r")
    code = f.readline().strip()
    if(code[:3] == "AUG"):
        asseq="M"
        i=3
        while True:
            nextcodon=code[i:i+3]
            i+=3 
            if nextcodon == "UAA" or nextcodon == "UAG" or nextcodon == "UGA":
                break
            else:
                asseq+=codons_to_as_dict[nextcodon]
        return asseq
    else:
        return ""   

print(toprotein("rosalind_prot.txt"))