#029 - SIGN - Enumerating Oriented Gene Orderings:

#Goal: Return the number of signed permutations, where each possible arrangement of + and - signs has to of each permutations of numbers has to be included in the list.
#My approach: The total amount is equal to n!*2**n, with n! representing the arrangements of numbers and 2**n the arrangments of signs.
    #First, create a list of the classic permutations.
    #The arrangements of signs can be represented by binary numbers, with 1 indicating a + and 0 a -.
    #For example, 0101 could represent [-a,b,-c,d] as one signed permutation.
    #So, go through all 2**n binary numbers for each permutation and assign the signs accordingly.

import math
from itertools import permutations

def signed_permutations(n):
    f = open("rosalind_sign_output.txt","w")
    f.write(str(int(math.factorial(n)*(2**n)))+"\n")
    versions = list(permutations(list(range(1,n+1))))
    for k in versions:
        for i in range(2**n):
            sign = bin(i)[2:].zfill(n)
            for j in range(len(k)):
                if str(sign[j])=="0":
                    f.write(str(-k[j])+" ")
                elif str(sign[j])=="1":
                    f.write(str(k[j])+" ") 
            f.write("\n")
    f.close()

signed_permutations(5)