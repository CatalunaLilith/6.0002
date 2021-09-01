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

def dp_make_weight(egg_weights, target_weight, eggs_list, memo = {}):
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
    print('-----------')
    print("egg_weights is:")
    print(egg_weights)
    print('-----------')
    print("type of eggs_list is:")
    print(type(eggs_list))
    print("eggs_list is:")
    print(eggs_list)
    print("sum of eggs_list is:")
    print(sum(eggs_list))
    print('-----------')
    print("memo is:")
    print(memo)
    print('-----------')
    if target_weight in memo:
        eggs_list = memo[target_weight]
    elif target_weight == 0 or len(egg_weights) == 0:
        #TODO: maybe just return eggs_list
        eggs_list =  [0]
    elif target_weight == 1:
        eggs_list = 1
    elif sum(eggs_list) >= target_weight:
        #Explore right branch only (dont take first egg)
        eggs_list = dp_make_weight(egg_weights[:-1], target_weight, eggs_list, memo)
        #return eggs_list
    else:
        next_egg = egg_weights[-1]
        #Explore left branch(take first egg)
        temp_eggs_list = eggs_list.copy()
        temp_eggs_list.append(next_egg)
        with_egg = dp_make_weight(egg_weights[:-1], (target_weight - next_egg), temp_eggs_list, memo)
        with_egg.append(next_egg)
        #Explore right branch (dont take first egg)
        without_egg = dp_make_weight(egg_weights[:-1], target_weight, eggs_list, memo)
        #Choose better branch
        if with_egg > without_egg:
            eggs_list = with_egg
        else:
            eggs_list = without_egg
        
    
    memo[target_weight] = eggs_list
    return eggs_list
    
    

def init_dp_make_weight(egg_weights, target_weight, memo = {}):
    egg_weights.sort()
    possible_eggs_list = [((str(egg)+" ")  * int((target_weight/egg))).split() for egg in egg_weights]
    possible_eggs_list = [egg for egg_sublist in possible_eggs_list for egg in egg_sublist]
    possible_eggs_list = [ int(egg) for egg in possible_eggs_list ]
    eggs_list = []
    return dp_make_weight(possible_eggs_list, target_weight, eggs_list, memo = {})

    
init_dp_make_weight([1, 5, 10, 25], 99, memo = {})


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