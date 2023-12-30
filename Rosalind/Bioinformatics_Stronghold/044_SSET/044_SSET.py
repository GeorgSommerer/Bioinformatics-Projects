#044 - SSET - Counting Subsets

#Goal: Find the amount of subsets of a set of size n, modulo 1000000
#This is equal to the size of the power set, which is equal to 2**n.

def powerset(inp):
    f = open(inp,"r")
    n = int(f.readline().strip())
    return pow(2,n,1000000)

print(powerset("rosalind_sset.txt"))