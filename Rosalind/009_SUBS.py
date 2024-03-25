#009 - SUBS - Finding a Motif in DNA:

#Goal: Find all locations of a certain substring in a DNA string.
#My approach: Iterate through the main string. If the substring is found, print the location.

def findmotif(code,motif):
    i=0
    outp = ""
    while i<(len(code)-len(motif)):
        if code[i:len(motif)+i]==motif:
           outp+=(str(i+1) + " ") 
        i+=1
    return outp

f = open("rosalind_subs.txt","r")
print(findmotif(f.readline().strip(),f.readlines()[0].strip()))