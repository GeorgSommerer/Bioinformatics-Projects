#003 - REVC - Complementing a Strand of DNA:

#Goal: Return the reverse complement of a DNA sequence.
#My approach: Iterate through the sequence, creating a string containing the respective complementary bases along the way, then return it in reverse order.

def reverse_complement(inp):
    f = open(inp, "r")
    seq = f.readline().strip()
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

print(reverse_complement("rosalind_revc.txt"))