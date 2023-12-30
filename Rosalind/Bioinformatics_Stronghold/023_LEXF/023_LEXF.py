#023 - LEXF - Enumerating k-mers Lexicographically:

#Goal: Return all strings from an alphabet, ordered lexicographically.
#My approach: This is equal to the n-fold cartesian product, which can be created with the itertools.product function.

from itertools import product

def letter_permutations(elems,n):
    perm = list(product(elems,repeat=n))
    for p in perm:
        print("".join(p))

letter_permutations("ABCDE",4)
