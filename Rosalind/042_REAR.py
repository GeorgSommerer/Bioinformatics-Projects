#042 - REAR - Reversal Distance

#Goal: Find the reversal distance between two permutations, which is equal to the amount of rotations required to transform them into each other.
#I took the code from: https://medium.com/@matthewwestmk/calculating-reversal-distance-using-parks-exact-greedy-algorithm-87c62d690eef


def performReversal(sequence, start_index, end_index):
    prefix = sequence[:start_index]
    reversed_subsequence = sequence[start_index:end_index][::-1]
    suffix = sequence[end_index:]
    return prefix + reversed_subsequence + suffix

def findBreakpoints(sequence, target_sequence):
    breakpoints = []
    for index in range(len(sequence)-1):
        current_element = sequence[index]
        adjacent_element = sequence[index+1]
        if abs(target_sequence.index(current_element) - target_sequence.index(adjacent_element)) != 1:
            breakpoints.append(index+1)
    return breakpoints

def findMinimumBreakpointReversals(sequences, target_sequence):
    reversals = []
    for sequence in sequences:
        breakpoints = findBreakpoints(sequence, target_sequence)
        for start_index_i in range(len(breakpoints)-1):
            for end_index_i in range(start_index_i+1, len(breakpoints)):
                reversals.append(performReversal(sequence, breakpoints[start_index_i], breakpoints[end_index_i]))
    min_bp = len(target_sequence)
    minimum_reversals = []
    for reversal in reversals:
        num_breakpoints = len(findBreakpoints(reversal, target_sequence))
        if num_breakpoints < min_bp:
            min_bp = num_breakpoints
            minimum_reversals = [reversal]
        elif num_breakpoints == min_bp:
            minimum_reversals.append(reversal)
    return minimum_reversals

def getReversalDistance(sequence, target_sequence):
    sequence = ["-"] + sequence + ["+"]
    target_sequence = ["-"] + target_sequence + ["+"]
    reversals = 0
    current_sequences = [sequence]
    while target_sequence not in current_sequences:
        current_sequences = findMinimumBreakpointReversals(current_sequences, target_sequence)
        reversals += 1
    return reversals

if __name__ == "__main__":
    with open("rosalind_rear.txt","r") as f:
        inputs = []
        for line in f:
            inputs.append([line.strip().split(" "),f.readline().strip().split(" ")])
            f.readline()
    for input in inputs:
        print(getReversalDistance(input[0], input[1]))