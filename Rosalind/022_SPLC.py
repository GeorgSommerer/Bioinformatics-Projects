#022 - SPLC - RNA Splicing:

#Goal: Transcribe a DNA string, splice the introns and translate it into a protein string.
#My approach: Sort the list in descending order, meaning that the DNA string that is to be translated is at the front.
    #Then, go through each intron and look for it in the string. If it is found, the string before is an exon and is added to a different string.
    #Then, look for the next occurrence of this intron, adding exons along the way. If the introns doesn't appear anymore, the remaining string is an exon.
    #Repeat for every introns, using the string remaining after removing the previous introns as the base.
    #Finally, transcribe and translate the final string. The Transcription and translation are the same as in 002 and 008.

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

#From 008:
def toprotein(code):
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

#From 002:  
def transcribe(seq):
    ct=0
    for i in seq:
        seq=seq.replace("T","U")
        ct+=1
    return seq

def splicing(inp):
    code = sorted(codetolist(inp),key=len)[::-1]
    for k in code[1:]:
        new_code0 = ""
        i=0
        old_i = 0
        while i<(len(code[0])-len(k)):
            if code[0][i:].find(k)!=-1:
                new_code0 += code[0][old_i:code[0][i:].find(k)]
                old_i = i
                i+=len(k)+code[0][i:].find(k)
            else:
                new_code0 += code[0][i:]
                i=len(code[0])
        code[0] = new_code0
    return toprotein(transcribe(code[0]))
   
print(splicing("rosalind_splc.txt"))