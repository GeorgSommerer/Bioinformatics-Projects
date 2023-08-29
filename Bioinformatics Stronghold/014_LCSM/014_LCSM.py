#014 - LCSM - Finding a Shared Motif:

#Goal: Find a shared motif between multiple DNA strings.
#My approach: This is equal to finding a longest common substring, whose length can be found via binary search.
    #Start with the length of the shortest string as the max and 0 as the min. Then calculate the average and check for every substring of the shortest string if it is a common substring.
    #If there is a common substring of this length, make the old average the new min and therefore increase the new average. If there is not, make the old average the new max and decrease the new average.

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

#Checks if a common substring exists.
def find_motif_help(code,m):
    for i in range(len(code[0])-m+1):
        candidate = code[0][i:m+i]
        is_in_all = True
        for j in range(1,len(code)):
            if code[j].find(candidate)==-1:
                is_in_all = False
                break
        if is_in_all == True:
            return candidate
    return ""

#Main function, conducting the binary search.      
def find_motif(inp):
    code = sorted(codetolist(inp),key=len)
    l = 0
    r = len(code[0])
    while l+1<r:
        m = int((l+r)/2)
        print(str(l) + " " + str(m) + " " + str(r))
        res = find_motif_help(code,m)
        if res=="":
            r = m
        else:
            l = m
    return find_motif_help(code,m)

print(find_motif("rosalind_lcsm.txt"))