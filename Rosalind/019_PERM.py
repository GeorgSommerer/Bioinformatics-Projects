#019 - PERM - Enumerating Gene Orders:
#Goal: Return all permutations of a certain length.
#My approach: While there is a permutations function in itertools, I decided to try to write one myself.
    #Start with a list of all permutations, containing just [1].
    #For each integer >1, add it to each sublist of the permutations list, then using list_shift to shift the elements of each sublist, adding the shifted versions.
    #This creates every possible permutation.
    #For example: [1] becomes [1,2]. Shift the elements, adding [2,1].
        #[1,2],[2,1] becomes [1,2,3],[2,1,3]. Shift the elements in each sublist again: [1,2,3] becomes [3,1,2], which is added, then [2,3,1], which is also added.
        #Likewise, [2,1,3] becomes [3,2,1], then [1,3,2], which are added as well.

import math

def permutation(n):
    amount = math.factorial(n)
    perms = [[1]]
    current_amount = 1
    for i in range(2,n+1):
        for l in perms:    
            l.append(i)
        for j in range(1,i):
            for k in range(current_amount):
                perms.append(list_shift(perms[k],j))
        current_amount*=i
    print(amount)
    for k in perms:
        for i in range(n):
            print(k[i],end=" ")
        print("")
        
def list_shift(elems,j):
    elemsnew = []
    while len(elemsnew)<len(elems):
            elemsnew.append(elems[j])
            if j<len(elems)-1:
                j+=1
            else:
                j=0
    return elemsnew

permutation(5)