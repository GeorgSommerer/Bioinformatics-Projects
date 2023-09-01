#042 - REAR - Reversal Distance

#Goal: Find the reversal distance between two permutations, which is equal to the amount of rotations required to transform them into each other.
#My approach: Brute force: Go through all possible 9! possible rotations, and repeat the same for each step until a solution is found.
    #Also, only look at rotations that lead to new permutations.

#While this function does return correct results, it is too slow to find reversal distances >=4 in a reasonable amount of time.
#If I have time, I will try to implement this myself: https://medium.com/@matthewwestmk/calculating-reversal-distance-using-parks-exact-greedy-algorithm-87c62d690eef
def rev_dist_help(template,rev):
    rev_old = []
    i=0
    for x in range(4):
        print(x)
        rev_new = []
        for n in rev:
            for l in range(2,11): #l indicates the length of the shift
                for p in range(11-l): #p indicates the starting position of the shift
                    reved = n[:p] + (n[p:p+l])[::-1] + n[p+l:]
                    if reved == template:
                        return i
                    else:
                        if reved not in rev_new and reved not in rev and reved not in rev_old:
                            rev_new.append(reved)
        for m in rev:
            if m not in rev_old:
                rev_old.append(m)
        rev = rev_new
        i+=1

def rev_dist(inp):
    f = open(inp,"r")
    for i in range(1):
        print(i)
        template = f.readline().split()
        rev = [f.readline().split()]
        print(template)
        print(rev)
        f.readline()
        if template == rev[0]:
            print("0",end=" ")
        else:
            print(rev_dist_help(template,rev),end=" ")
        

rev_dist("rosalind_rear.txt")