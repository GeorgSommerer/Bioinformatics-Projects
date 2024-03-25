#028 - PROP - Introduction to Random Strings:

#Goal: For each GC probability inputted, return the common logarithm (log_10) of the probability that a random string constructed with this probability matches the input string.
#My approach: The probability of a base being G or C is i/2, with i being the input, and (1-i)/2 for A or T.
    #The base has to match for every char of the input character, so we take the power equal to the GC content or the AT content respectively.
    #Lastly, return the common logarithm of this number.

import math

def random_array(inp):
    f = open(inp,"r")
    seq = f.readline().strip()
    probs = list(map(float,f.readline().split()))
    gc = seq.count("G") + seq.count("C")
    at = seq.count("A") + seq.count("T")
    for i in probs:
        print(round(math.log10(((i/2)**gc)*((1-i)/2)**at),3),end=" ")

random_array("rosalind_prob.txt")