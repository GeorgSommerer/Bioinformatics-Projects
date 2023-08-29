#017 - MRNA - Inferring mRNA from Protein:

#Goal: Find the amount of different RNA strings from which a protein could have been translated modulo 1000000.
#My approach: Create a dictionary relating the amino acids to a list of possible codons. Then, multiply the amount of amino acids times the amount of codons for each (times the amount of stop codons).
    #Since mod 1000000 is distributive and simply outputs the first 6 digits, you can take it only once at the end.

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

def to_mRNA_amount(inp):
    f = open(inp, "r")
    code = f.readline().strip()
    res = 1
    for n in code:
        res*=len(as_to_codons_dict[n])
        res=res%1000000
    return (res*3)%1000000

print(to_mRNA_amount("rosalind_mrna.txt"))