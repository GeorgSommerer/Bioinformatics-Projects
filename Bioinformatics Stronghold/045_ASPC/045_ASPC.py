#045 - ASPC - Introduction to Alternative Splicing

#Goal: Find the sum of combinations n over k for all k with m<=k<=n, modulo 1000000.
#My approach: Simply calculate the sum.

from math import factorial

def sum_of_combinations(inp):
    f = open(inp,"r")
    tmp = f.readline().split()
    n = int(tmp[0])
    m = int(tmp[1])
    sum = 0
    for k in range(m,n+1):
        sum+=int(factorial(n)//(factorial(k)*factorial(n-k)))%1000000
    return int(sum)%1000000

print(sum_of_combinations("rosalind_aspc.txt"))