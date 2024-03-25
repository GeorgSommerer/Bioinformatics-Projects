#006 - HAMM - Counting Point Mutations:

#Goal: Find the amount of point mutations between two sequences.
#My approach: This is equal to the hamming distance of the sequences. Iterate through them and count the amount of different chars.

def point_mutations(base, test):
    ctr = 0
    for i in range(len(base)):
        if base[i] != test[i]:
            ctr+=1
    return ctr

f = open("rosalind_hamm.txt","r")
print(point_mutations(f.readline().strip(),f.readlines()[0].strip()))