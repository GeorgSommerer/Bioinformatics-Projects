#004 - FIB - Rabbits and Recurrence Relations:

#Goal: Return the total number of rabbit pairs after n months, if we begin with 1 pair and after each month, every pair of reproduction-age rabbits produces a litter of k rabbit pairs.
#My approach: The standard Fibonacci recursion equals F_n=F_{n-1}+F_{n-2}, meaning that the n-th generation will consist of all rabbits that have lived 1 generation ago,
    #as well as all newly born rabbits, which is equal to the amount of rabbits that were adult in the ago times the amount of pairs born per adult pair.
    #This value k is 1 for the standard recursion, but by varying it, we get the general recurive formula F_n=F_{n-1}+k*F_{n-2}.

def fibo(n,k):
    if n==1 or n==2:
        return 1
    else: 
        return fibo(n-1,k) + k*fibo(n-2,k)

print(fibo(28,3))