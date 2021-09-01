###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================
import site
import pdb
counter=[0]

# Problem 1 


def dp_make_weight(egg_weights, target_weight, eggs_list =[], memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #return smallest #eggs to make target weight = len(list of eggs)
    if target_weight in memo:
        eggs_list = memo[target_weight]
    elif target_weight == 0 or len(egg_weights) == 0:
        print("an input is zero, something went wrong")
    elif target_weight == 1:
        eggs_list = [1]
    elif sum(eggs_list) == target_weight:
        return len(eggs_list)
    elif sum(eggs_list) > target_weight:
        raise Exception("SOMETHING WENT WRONG sum(eggs_list) > target_weight ")
    else:
        next_egg = egg_weights[-1]
        #Choose better branch
        if (sum(eggs_list) + next_egg) <= target_weight:
            #Explore left branch(take first egg)
            temp_eggs_list = eggs_list.copy()
            temp_eggs_list.append(next_egg)
            with_egg = dp_make_weight(egg_weights[:-1], (target_weight), temp_eggs_list, memo)
            eggs_list = with_egg
        else:
            #Explore right branch (dont take first egg)
            without_egg = dp_make_weight(egg_weights[:-1], target_weight, eggs_list, memo)
            eggs_list = without_egg
    memo[target_weight] = eggs_list
    return eggs_list
    
    

def init_dp_make_weight(egg_weights, target_weight, memo = {}):
    egg_weights.sort()
    possible_eggs_list = [((str(egg)+" ")  * int((target_weight/egg))).split() for egg in egg_weights]
    possible_eggs_list = [egg for egg_sublist in possible_eggs_list for egg in egg_sublist]
    possible_eggs_list = [ int(egg) for egg in possible_eggs_list ]
    #eggs_list = []
    return dp_make_weight(possible_eggs_list, target_weight, eggs_list = [], memo = {})





# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = [1, 5, 10, 25]
    target_weight = 99
    print("Egg weights = [1, 5, 10, 25]")
    print("target_weight = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", init_dp_make_weight(egg_weights, target_weight, memo = {}))
    print()
