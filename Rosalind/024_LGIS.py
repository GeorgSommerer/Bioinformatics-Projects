#024 - LGIS - Longest Increasing Subsequence:

#Goal: Return a longest increasing subsequence, as well as a longest decreasing subsequence.
#My approach: At every step, add the new element to the tail of every saved list, if possible (if it is bigger (increasing) or smaller (decreasing) than the tail element)
    #It doesn't make sense at any point to have two strings of the same length, since the one with the smaller tail element will always be able to grow more.
    #For example, if we have a string X,X,5 and a string X,X,3, they can both grow if a number >5 comes next, but the latter one can also grow if 4 comes next.
    #Therefore, keep the list with the smaller tail element, if there are multiple lists with the same length.
    #In the end, return the longest of these lists.

def max_by_weight(sequence):
    maximum = sequence[0]
    for item in sequence:
        if item[1] > maximum[1]:
            maximum = item
    return maximum[0]

def incr_sub_help(pi):
    candidates = [[pi[0]]]
    for k in range(1,len(pi)):
        toadd = []
        #Save a list of all elements to which the new one can be added, as well as their length.
        for i in range(len(candidates)):
            if candidates[i][-1]<pi[k]:
                toadd.append([i,len(candidates[i])])
        #If the new element can't be added, it must be the smallest thus far. Therefore, remove all 1 element lists and add the new element as a 1 element list.
        if toadd == []:
            for m in candidates:
                if len(m)==1:
                    candidates.remove(m)
            candidates.append([pi[k]])
        #Else, find the longest list and append the new element to it. If this new list is as long as any old lists, remove those, since their tail will be bigger.
        else:
            newcand = candidates[max_by_weight(toadd)]
            newcand.append(pi[k])
            for m in candidates:
                if len(m)==len(newcand):
                    candidates.remove(m)
            if newcand not in candidates:
                candidates.append(newcand)
            #Restore the list to which the new element was added.
            candidates.append(newcand[:-1])
    return(max(candidates,key=len))

def incr_sub(inp):
    f = open(inp,"r")
    n = f.readline().strip()
    p = f.readline().split()
    #Since the function (especially max_weight) are written to work with strings, I have to convert every number to a string, making sure they all have the same length by adding zeroes in front of 1-, 2- and 3-digit numbers.
    #Increasing:
    pi1 = []
    for k in p:
        while len(k)<len(str(n)):
            k = "0" + k
        pi1.append(k)
    pi2 = pi1[::-1]
    p = incr_sub_help(pi1)
    #In order to print the correct results, the previously added zeroes have to be removed.
    pi1 = []
    for k in p:
        while k[0]=="0":
            k = k[1:]
        pi1.append(k)
    print(" ".join(pi1))
    #Decreasing:
    p = incr_sub_help(pi2)
    pi2 = []
    for k in p:
        while k[0]=="0":
            k = k[1:]
        pi2.append(k)
    print(" ".join(pi2[::-1]))

incr_sub("rosalind_lgis.txt")