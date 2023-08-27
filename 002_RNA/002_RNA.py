#002 - RNA - Transcribing DNA into RNA:

#Goal: Turn a DNA sequence into an RNA sequence.
#My approach: Iterate through the input and replace all T with U.

def transcribe(inp):
    f = open(inp, "r")
    seq = f.readline().strip()
    ct=0
    for i in seq:
        seq=seq.replace("T","U")
        ct+=1
    return seq

print(transcribe("rosalind_rna.txt"))