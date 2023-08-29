#027 - PPER - Partial Permutations:

#Goal: Find the total number of partial permutations (permutations of k elements randomly selected from n elements, with n>=k).
#My approach: First, calculate the amount of subsets of n with k elements, meaning all k-combinations, which is equal to n!/(k!(n-k)!).
    #There are k! possibilities of arranging the k elements of each of those combinations.
    #The k! cancel each other out, leaving us with n!/(n-k)!, or the falling factorial of n over k.

import math

def partial_permutations(n,k):
    return int((math.factorial(n)/math.factorial(n-k))%1000000)

print(partial_permutations(84,9))