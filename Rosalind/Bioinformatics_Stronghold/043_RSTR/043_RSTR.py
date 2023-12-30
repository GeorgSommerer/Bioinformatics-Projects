#043 - RSTR - Matching Random Motifs

#Goal: Find the probability that if N random DNA string are constructed using the GC-content x, at least one of the strings equals the input string s.
#My approach: This is the same as 1-the probability of no such string being constructed.
    #This probability in turn is equal to 1-the probability of such a string being constructed to the power of the amount of strings.

def random_motif(inp):
    f = open(inp,"r")
    tmp = f.readline().split()
    N = int(tmp[0])
    x = float(tmp[1])
    seq = f.readline().strip()
    gc = seq.count("G") + seq.count("C")
    at = seq.count("A") + seq.count("T")    
    print(round(1-(1-((x/2)**gc)*((1-x)/2)**at)**N,3))

random_motif("rosalind_rstr.txt")