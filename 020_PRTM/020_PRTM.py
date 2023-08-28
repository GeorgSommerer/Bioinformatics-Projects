#020 - PRTM - Calculating Protein Mass:

#Goal: Return the total weight of a protein.
#My approach: This is as simple as adding the weights of each amino acid of the protein string together.

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

def protein_mass(inp):
    mass = 0
    f = open(inp, "r")
    seq = f.readline().strip()
    for n in seq:
        mass+=protein_mass_dict[n]
    return mass

print(protein_mass("rosalind_prtm.txt"))