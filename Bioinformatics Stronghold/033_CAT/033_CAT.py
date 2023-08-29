#033 - CAT - Catalan Numbers and RNA Secondary Structures:

#Goal: Find the number of noncrossing perfect matchings of basepair edges modulo 1000000.
#My approach: First, start at one end of the graph and find all bases that pair with that first base.
    #Using the properties of the Catalan numbers, calculate for each one with an odd index in the list (meaning an even index in the string)
        #recursively the sum of arrangements from 1 to i-1 and from i+1 to the end.
    #If no possible arrangement can be found (which is the case if U!=A or C!=G), return 0. Otherwise, return 1.
    #Also, keep a list of the catalan numbers for subgraphs that have already been calculated to increase speed.

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

#Assigns each base of an RNA its counterpart.
def opposite_base(base):
    if base == "A":
        return "U"
    elif base == "U":
        return "A"
    elif base == "G":
        return "C"
    elif base == "C":
        return "G"

#Calculates the number recursively.
def noncrossing_perfect_matchings_help(seq,a,b,dp):
    if seq[a:b].count("A")!=seq[a:b].count("U")or seq[a:b].count("G")!=seq[a:b].count("C"):
        return 0
    if a >= b:
        return 1
    if (a,b) in dp:
        return dp[(a,b)]
    else:
        pairings = 0
        i=a
        while i<b:
            if seq[i]==opposite_base(seq[a]):
                pairings += (noncrossing_perfect_matchings_help(seq,a+1,i,dp)*noncrossing_perfect_matchings_help(seq,i+1,b,dp))%1000000
            i+=1
        dp[(a,b)]=pairings
        return pairings 
    
#Start function.
def noncrossing_perfect_matchings(inp):
    seq = codetolist(inp)[0]
    return noncrossing_perfect_matchings_help(seq,0,len(seq),{})%1000000

print(noncrossing_perfect_matchings("rosalind_cat.txt"))
            