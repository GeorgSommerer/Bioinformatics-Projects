#025 - LONG - Genome Assembly as Shortest Superstring

#Goal: Construct a shortest superstring containing all the given strings by gluing them together along their overlaps.
#My approach: Start with an arbitrary string. While there are still strings not attached to this string, do the following:
    #Go through every other string and continuously save the length of the biggest overlap as well as the side of the overlap (left or right of the first string).
    #Attach the string with the biggest overlap on the correct side of the first string and remove it from the list.
    #In the end, given the assumption that they can all be glued together to one chromosome, the list should be empty and all string glued together.

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

def shortest_superstring(inp):
    seqs = codetolist(inp)
    shortest = seqs.pop()
    while len(seqs)>0:
        overlap_place = 0
        overlap_length = 0
        overlap_side=""
        for i in range(len(seqs)):
            #Check how many bases overlap to the right of the starting string.
            temp_len_back = 0
            j=1
            while min(len(shortest[len(shortest)-j:]),len(seqs[i][j-1:]))!=0:
                if shortest[-j:] == seqs[i][:j]:
                   temp_len_back = j
                j+=1
            #Check how many bases overlap to the left of the starting string.
            temp_len_front = 0
            m=1
            while min(len(shortest[m-1:]),len(seqs[i][len(seqs[i])-m:]))!=0:
                if seqs[i][-m:] == shortest[:m]:
                   temp_len_front = m
                m+=1
            #If a new biggest overlap is found, save the length, the position of the overlapping string, and the side.
            if overlap_length<temp_len_back or overlap_length<temp_len_front:
                overlap_place = i
                if temp_len_front > temp_len_back:
                    overlap_side="f"
                    overlap_length = temp_len_front
                else:
                    overlap_side = "b"
                    overlap_length=temp_len_back
        #Remove the string with the biggest overlap from the list and attach it to the first string.
        if overlap_side=="f":
            shortest = seqs[overlap_place] + shortest[overlap_length:]
            seqs.remove(seqs[overlap_place])
        elif overlap_side=="b":
            shortest = shortest + seqs[overlap_place][overlap_length:]
            seqs.remove(seqs[overlap_place])
        else:
            print("error")
            break
    return(shortest)
            
f = open("rosalind_long_output.txt","w")
f.write(shortest_superstring("rosalind_long.txt"))
f.close()