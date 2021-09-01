###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #highly analogous to knapsack problem of fastMaxVal
    #return smallest #eggs to make target weight = len(list of eggs)
    avail_weight = target_weight
    egg_weights.sort()
    #TODO: figure out how to make this happen once
    possible_eggs_list = [((str(egg)+" ")  * int((target_weight/int(egg)))).split() for egg in egg_weights]
    possible_eggs_list = [egg for egg_sublist in possible_eggs_list for egg in egg_sublist]
    if avail_weight in memo:
        eggs_list = memo[avail_weight]
    elif avail_weight == 0 or len(egg_weights)==0:
        eggs_list =  [0]
    elif int(possible_eggs_list [0]) > avail_weight:
        eggs_list = dp_make_weight(possible_eggs_list [1:], avail_weight, memo)
    else:
        next_egg = int(possible_eggs_list [0])
        #take next item, recursive call for next step
        withVal = dp_make_weight(possible_eggs_list [1:], (avail_weight-next_egg), memo)
        withVal += [next_egg]
        #not take next item, recursive call for next step
        withoutVal = dp_make_weight(possible_eggs_list [1:], avail_weight, memo)
        #pick if take
        if withVal > withoutVal:
            eggs_list = [withVal] + [next_egg]
            print("with")
            print(possible_eggs_list)
        else:
            eggs_list = withoutVal
            print("without")
            print(possible_eggs_list)
        
    memo[avail_weight] = eggs_list
    
    return eggs_list
    
dp_make_weight([1, 5, 10, 25], 99, memo = {})


"""
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
"""