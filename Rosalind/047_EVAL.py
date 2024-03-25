#047 - EVAL - Expected Number of Restriction Sites

#Goal: For each GC content, calculate the expected number of times the input string s will appear in a random DNA string t of length n.
#My approach: For s to appear in t, all of the bases have to match, meaning that we multiply the probabilities for each base dictated by the GC content.
    #This is possible for every position in t from 1 to len(t)-len(s)+1, so the result is multiplied by len(t)-len(s)+1.

def restriction_sites_number(n,s,B):
    gc = s.count("G")+s.count("C")
    at = len(s)-gc
    for i in B:
        print(((i/2)**gc)*(((1-i)/2)**at)*(n-len(s)+1),end=" ")

f = open("rosalind_eval.txt","r")
n = int(f.readline().strip())
s = f.readline().strip()
B = list(map(float,f.readline().split()))
restriction_sites_number(n,s,B)