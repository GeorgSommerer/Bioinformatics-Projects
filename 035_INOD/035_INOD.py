#035 - INOD - Counting Phylogenetic Ancestors

#Goal: Find the number of internal nodes of any unrooted binary tree having n leaves.
#My approach: For i>1 is n=i+2, so i=n-2
    #Proof: Start with 1 internal node, which has to have 3 leaves per definition.
        #Then replace one leaf with an internal node, which has to have 2 leaves itself to be complete.
        #This means that for every internal node added, 1 leaf has to be added in total (i=1,n=3; i=2,n=4; i=3,n=5;...).
    #Alternative proof: Using the handshaking lemma, the sum of the degrees has to be equal to 2*|E| (the amount of edges).
        #The sum of degrees is equal to 3i+n, with i as internal nodes (all having degree 3) and n as leaves (all having degree 1).
        #Since this is a tree, |E|=|N|-1=n+i-1.
        #3i+n=2((n+i)-1)=2n+2i-2
        #i=n-2

def internal_nodes(n):
    return n-2

print(internal_nodes(3609))