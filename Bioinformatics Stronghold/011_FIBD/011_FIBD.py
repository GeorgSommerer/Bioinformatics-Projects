#011 - FIBD - Mortal Fibonacci Rabbits:

#Goal: Similar to #004, except that all rabbits die after m months and k=1.
#My approach: We start with 1 pair of young rabbits, which will turn into mature rabbits the next generation.
    #The amount of rabbits is equal to R_n+r_n-r_{n-m+1}, where r represents the rabbits born and R the rabbits that turned adult.
    #Since R_i=F_{i-1} and r_i=F_{i-2}, we can deduct the recursive equation F_n=F_{n-1}+F_{n-2}-F_{n-m-1}.

def fibomortal(n,m):
    alive = [1,1]
    for i in range(2,n):
        temp = alive[i-1] + alive[i-2]
        if i == m:
            temp-=1
        if i > m:
            temp=temp-alive[i-m-1]
        alive.append(temp)
    return alive[-1]

print(fibomortal(87,16))