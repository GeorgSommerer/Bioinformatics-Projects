#038 - LCSQ - Finding a Shared Spliced Motif

#Goal: Finding a longest common (discontinuous) subsequence of the input DNA sequences.
#My approach: Create a len(string 1)+1xlen(string 2)+1 matrix, with the 0th row and queue being filled with 0. Via dynamic programming, save the length of subsequences in this matrix.
    #Create another matrix of the same size, with directions.    
    #Compare each pair i,j of elements between the strings. If they are the same, take the value of the field i-1,j-1, add 1 and point to that field.
    #Otherwise, take the bigger value between the fields i-1,j, i,j-1 and point to that field.
    #In the end, the field in the bottom right (len(string 1),len(string 2)) will contain the length of the longest subsequence.
    #Using the direction, trace the base sequence back from the bottom right field, adding a base whenever the length decreases.

import numpy as np

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

def lcs(inp):
    s1 = codetolist(inp)[0]
    s2 = codetolist(inp)[1]
    lcs_matrix_lengths = np.tile(0,(len(s1)+1,len(s2)+1))#1st level: matrix, 2nd level: rows, 3rd level: 3-element entries (length, change to the top, change to the left)
    lcs_matrix_directions = np.tile("",(len(s1)+1,len(s2)+1))
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if s1[i-1]==s2[j-1]:
                lcs_matrix_lengths[i][j] = lcs_matrix_lengths[i-1][j-1]+1
                lcs_matrix_directions[i][j] = "b"
            else:
                up = lcs_matrix_lengths[i-1][j]
                left = lcs_matrix_lengths[i][j-1]
                if up>=left:
                    lcs_matrix_lengths[i][j] = lcs_matrix_lengths[i-1][j]
                    lcs_matrix_directions[i][j] = "u"
                else:
                    lcs_matrix_lengths[i][j] = lcs_matrix_lengths[i][j-1]
                    lcs_matrix_directions[i][j] = "l"
    res = ""
    current = lcs_matrix_lengths[i][j]
    while current!=0:
        if lcs_matrix_directions[i][j]=="b":
            next=lcs_matrix_lengths[i-1][j-1]
            i-=1
            j-=1
        elif lcs_matrix_directions[i][j]=="u":
            next=lcs_matrix_lengths[i-1][j]
            i-=1
        elif lcs_matrix_directions[i][j]=="l":
            next=lcs_matrix_lengths[i][j-1]
            j-=1
        else:
            break
        if next != current:
            res = s1[i] + res
        current = next
    return res




print(lcs("rosalind_lcsq.txt"))
