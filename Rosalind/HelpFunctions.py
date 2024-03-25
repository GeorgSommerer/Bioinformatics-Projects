#This file contains functions and data structures useful for reading the code of the datasets downloaded from Rosalind, as well as dictionaries containing information about amino acids, nucleotides, etc.

from enum import Enum
import requests

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

#Assigns the mass to the corresponding amino acid.
protein_mass_dict = {
"A":   71.03711,
"C":   103.00919,
"D":   115.02694,
"E":   129.04259,
"F":   147.06841,
"G":   57.02146,
"H":   137.05891,
"I":   113.08406,
"K":   128.09496,
"L":   113.08406,
"M":   131.04049,
"N":   114.04293,
"P":   97.05276,
"Q":  128.05858,
"R":   156.10111,
"S":   87.03203,
"T":   101.04768,
"V":   99.06841,
"W":   186.07931,
"Y":   163.06333 
}

#Enumerates the DNA bases.
class BasesDNA(Enum):
    A = 0
    C = 1
    G = 2
    T = 3

#Enumerates the RNA bases.
class BasesRNA(Enum):
    A = 0
    C = 1
    G = 2
    U = 3

#Converts a txt file in FASTA format to a list of the sequences.
def codetolist(inp):
    codelist=[]
    with open(inp,"r") as f:
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

#Takes a string from a txt file in FASTA format.
def multiline_code(inp):
    with open(inp,"r") as f:
        multilines = "".join(f.read().splitlines()[1:])
    return multilines

#Converts a txt file in FASTA format to a dictionary, where the sequences are assigned to the corresponding names.
def codetodict(inp):
    genes = {}
    with open(inp, "r") as f:
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

#Returns the 1st line from a txt file.
def first_line_code(inp):
    with open(inp, "r") as f:
        first_line = f.readline().strip()
    return first_line

#Returns the 2nd line from a txt file.
def second_line_code(inp):
    with open(inp, "r") as f:
        second_line = f.readlines()[1].strip()
    return second_line

#Reads the amino acid sequences from uniprot.org corresponding to the FASTA ids inputted through a txt file.
def aslist_from_uniprot_IDs(ids):
    with open(ids, "r") as f:
        outp=[]
        for line in f:
            coderaw = requests.get("https://rest.uniprot.org/uniprotkb/"+(line.split("_"))[0].strip()+".fasta").text
            tooutp = ""
            for i in range(1,len(coderaw.splitlines())):
                tooutp+=coderaw.splitlines()[i]
            outp.append(tooutp)
    return outp

#Assigns each base of an RNA its counterpart.
def opposite_base(base):
    if base == "A":
        return "U"
    elif base == "U":
        return "A"
    elif base == "G":
        return "C"
    elif base == "C":
        return "G"
