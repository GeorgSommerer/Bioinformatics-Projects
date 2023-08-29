#018 - ORF - Open Reading Frames:

#Goal: Output every distinct open reading frame (ORF) of the input dna sequence.
#My approach: An ORF is equal to a sequence from a start codon to the first stop codon of the sequence or its reverse complement.
    #Therefore, find every start codon in the string and traverse it, until you reach a stop codon or the end of the string, and translate each codon into its corresponding amino acid.

#Assigns the 1 letter code of each amino acid to every corresponding codon.
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

#Assigns a list of every codon to the corresponding amino acid.
as_to_codons_dict = {
    "F":['UUU', 'UUC'],
    "L":['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'],
    "S":['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],
    "Y":['UAU', 'UAC'],
    "C":['UGU', 'UGC'],
    "W":['UGG'],
    "P":['CCU', 'CCC', 'CCA', 'CCG'],
    "H":['CAU', 'CAC'],
    "Q":['CAA', 'CAG'],
    "R":['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
    "I":['AUU', 'AUC', 'AUA'],
    "M":['AUG'],
    "T":['ACU', 'ACC', 'ACA', 'ACG'],
    "N":['AAU', 'AAC'],
    "K":['AAA', 'AAG'],
    "V":['GUU', 'GUC', 'GUA', 'GUG'],
    "A":['GCU', 'GCC', 'GCA', 'GCG'],
    "D":['GAU', 'GAC'],
    "E":['GAA', 'GAG'],
    "G":['GGU', 'GGC', 'GGA', 'GGG'],
    "Stop":['UAA','UAG','UGA']
}

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

#From 002 - Is necessary, because the dictionaries are for RNA, not for DNA
def transcribe(seq):
    ct=0
    for i in seq:
        seq=seq.replace("T","U")
        ct+=1
    return seq

#From 003
def reverse_complement(seq):
    out = ""
    for i in seq:
        if i == 'T':
            out = out + "A"
        elif i == 'A':
            out = out + "T"
        elif i == 'G':
            out = out + "C"
        elif i == 'C':
            out = out + "G"
    return out[::-1]

def find_ORFs(inp):
    inps = [transcribe(codetolist(inp)[0]),transcribe(reverse_complement(codetolist(inp)[0]))]
    seqs = []
    for w in range(2):
        i = 0
        cd = 0
        startc=[]
        #Go through the string and find every AUG codon.
        while cd!=-1:
            cd = inps[w].find("AUG",i)
            if cd!=-1:
                startc.append(cd)
            i=cd+3
        #Go through every AUG codon and translate starting from it.
        for n in startc:
            outp = ""
            for i in range(n,len(inps[w]),3):
                if inps[w][i:i+3] in codons_to_as_dict.keys() and inps[w][i:i+3] not in as_to_codons_dict["Stop"]:
                    outp+=codons_to_as_dict[inps[w][i:i+3]]
                else:
                    break
                #Don't output it, if it doesn't end with a stop codon.
                if (i+3==len(inps[w]) and inps[w][i:i+3] not in as_to_codons_dict["Stop"]):
                    outp = ""
            #Output every unique protein string that ends with a stop codon.
            if outp not in seqs and outp!="":
                seqs.append(outp)
    for n in seqs:
        print(n)

find_ORFs("rosalind_orf.txt")