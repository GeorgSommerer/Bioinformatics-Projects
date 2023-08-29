#015 - LIA - Independent Alleles:

#Goal: Starting with two Aa Bb organisms, calculate the probability that >=N Aa Bb organisms will belong to the k-th generation if each offspring also mates with an Aa Bb organism.
#My approach: No matter the partner, the probability having an Aa child with an Aa partner is always 50%, the same for a Bb child with a Bb partner.
    #Therefore, this problem can be expressed as the 

import math

def amount_AaBb(k, N):
    outp = 0
    for i in range(N):
        outp+=((0.25)**i)*((0.75)**(2**k-i))*(math.factorial(2**k)/(math.factorial(i)*(math.factorial(2**k-i))))
    return 1-outp

#print(amount_AaBb(6,16))