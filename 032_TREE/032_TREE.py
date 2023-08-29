#032 - TREE - Completing a Tree:

#Goal: Starting with a number of connected components in form of an adjacency list, output the number of edges that can be added to produce a tree.
    #Since Amount of Edges = Amount of Nodes - 1 in a tree, the number of edges that can be added is equal to Amount of Nodes - 1 - Current Amount of Edges.

def complete_tree(inp):
    f = open(inp,"r")
    t = f.read().splitlines()
    print(int(t[0])-len(t[1:])-1)

complete_tree("rosalind_tree.txt")