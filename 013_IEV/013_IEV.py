#013 - IEV - Calculating Expected Offspring:

#Goal: Out of a population of arbitrary amounts AA-AA, AA-Aa, AA-aa, Aa-Aa, Aa-aa and aa-aa couples, return the expected offspring displaying the dominant phenotype.
#My approach: For AA-AA, AA-Aa, and AA-aa, the probability is 1. For Aa-Aa, it is 75%, for Aa-aa 50%, and for aa-aa 0%.
    #The sum of these times the respective amounts of couples is equal to the expected value for 1 offspring; since every couple has 2 children, multiply this value by 2.

def exp_dominant(a,b,c,d,e,f):
    return 2*(a*1+b*1+c*1+d*0.75+e*0.5+f*0)

print(exp_dominant(19351,19746,19140,18655,19819,16872))