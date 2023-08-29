#034 - CORR - Error Correction in Reads

#Goal: Each string appears either >=2 times (itself or its reverse complement), which should be kept, or appear once and have a hamming distance to one of the strings appearing multiple times, which should be fixed.
#My approach: Mark all sequences with a 0, standing for "not confirmed to be correct."
    #If it has a 0 attached, compare it with all the following sequences or its reverse complement. If a match is found, mark both of them with 1 and continue until the end.
    #Afterwards, look at all that are still marked with 0 and compare them with every other string or its reverse complement. If the hamming distance is 1, output the wrong and then the corrected version.

#Converts a txt file in FASTA format to a list of the sequences.
def codetolist(inp):
    codelist=[]
    f = open(inp, "r")
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

#From 003:
def reverse_complement(seq):
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

#From 006:
def point_mutations(base, test):
    ctr = 0
    for i in range(len(base)):
        if base[i] != test[i]:
            ctr+=1
    return ctr

def hamming_correction(inp):
    seq = codetolist(inp)
    #Mark all with 0.
    for i in range(len(seq)):
        seq[i] = [seq[i],0]
    #Look for duplicates.
    for i in range(len(seq)):
        if seq[i][1]==0:
            is_double = False
            for j in range(i+1,len(seq)):
                if seq[i][0]==seq[j][0] or seq[i][0]==reverse_complement(seq[j][0]):
                    seq[j][1]=1
                    is_double = True
        else:
            continue
        if is_double == True:
            seq[i][1]=1
    g = open("rosalind_corr_output.txt","w")
    #Correct the incorrect sequences.
    for i in range(len(seq)):
        if seq[i][1]==0:
            for j in range(len(seq)):
                if point_mutations(seq[i][0],seq[j][0]) == 1 and seq[j][1]==1:
                    g.write(seq[i][0] + "->"+seq[j][0]+"\n")
                    break
                elif point_mutations(seq[i][0],reverse_complement(seq[j][0])) == 1 and seq[j][1]==1:
                    g.write(seq[i][0] + "->"+reverse_complement(seq[j][0])+"\n")
                    break
    g.close()

hamming_correction("rosalind_corr.txt")