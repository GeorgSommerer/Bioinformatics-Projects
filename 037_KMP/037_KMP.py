#037 - KMP - Speeding Up Motif Finding

#Goal: Find the failure array of an input string, which indicates substrings that are equal to a part of the beginning of the string.
#My approach: Employ KMP algorithm:
    #Go through the sequence; if a base matches the first base, add it to a list of currently ongoing substrings.
        #Check the next bases and add them to each of the substrings where the match is ongoing; if it is interrupted, delete the substring.
        #Print the length of the longest ongoing substring.

#Takes a string from a txt file in FASTA format.
def multiline_code(inp):
    f = open(inp,"r")
    return "".join(f.read().splitlines()[1:])

def failure_array(inp):
    seq = multiline_code(inp)
    result = [0]
    substrings = []
    for i in range(1,len(seq)):
        substringsnew = []
        for j in substrings:
            if seq[j[-1]+1]==seq[len(j)]:
                j.append(i)
                substringsnew.append(j)
        if seq[i]==seq[0]:
            substringsnew.append([i])
        if substringsnew==[]:
            result.append(0)
            substrings = []
        else:
            substrings=substringsnew
            result.append(len(substrings[0]))
    f = open("rosalind_kmp_output.txt","w")
    f.write(' '.join(map(str, result)))

failure_array("rosalind_kmp.txt")