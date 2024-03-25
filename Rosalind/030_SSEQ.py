#030 - SSEQ - Finding a Spliced Motif:

#Goal: Taking a template string and an input string, find the (possibly noncontinous) input string as a subsequence of the template string and return the indices.
#My approach: Go through the template from left to right and start looking for the first base of the input string.
    #Everytime a base is found, output its position in the template and move on to the next base of the input, until it has been parsed completely.

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

def spliced_motif(inp):
    template_seq = codetolist(inp)[0]
    motif = codetolist(inp)[1]
    positions = []
    base_in_motif = 0
    base_in_template = 0
    while base_in_motif<len(motif) and base_in_template<len(template_seq):
        if motif[base_in_motif]==template_seq[base_in_template]:
            positions.append(base_in_template+1)
            base_in_motif+=1
        base_in_template+=1
    for i in positions:
        print(i,end=" ")

spliced_motif("rosalind_sseq.txt")