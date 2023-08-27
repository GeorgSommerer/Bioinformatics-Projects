#007 - IPRB - Mendel's First Law:

#Goal: Find the probability that two randomly selected mating organisms will produce an individual possessing a dominant allele, if the population has
    #k homozygous dominant, m heterozygous and n homozygous recessive individuals.
#My approach: The probabilities for an Aa child to be born are equal to the sum of probabilities on this table: https://i.postimg.cc/HLZxZdWv/table.png
    #By rearranging the equation, we get the equation I used in the function.

def dominant(k,m,n):
    t = k+m+n
    return 1-((4*n*m+4*n*n-4*n+m*m-m)/(4*t*t-4*t))

print(dominant(23,29,30))