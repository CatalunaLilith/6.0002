###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    with open(filename) as f:
        raw_cow_data = f.read()
    cow_list = raw_cow_data.split("\n")
    cow_dict = {}
    #split each cow at ","
    for cow in cow_list:
        cow_holder = cow.split(",")
        cow_dict[cow_holder[0]] = cow_holder[1]
    return cow_dict


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_dict = cows.copy()
    trip_list_list = []
    
    while cow_dict:
        # innitialize trip
        trip_list = []
        trip_weight = 10
        #first cow
        acow = max(cow_dict, key=lambda key: cow_dict[key])
        trip_list.append(acow)
        trip_weight -= int(cow_dict[acow])
        del cow_dict[acow]
        #additional cow(s)
        if trip_weight >= 1:
            cow_list = [(k, v) for k, v in cow_dict.items()] 
            cow_list.sort(key=lambda x: x[1])
            cow_list.reverse()
            for bcow in cow_list:
                if int(bcow[1]) <= trip_weight:
                      trip_list.append(bcow[0])
                      trip_weight -= int(cow_dict[bcow[0]])
                      del cow_dict[bcow[0]]
        trip_list_list.append(trip_list)
    return trip_list_list
                

    
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_dict = cows.copy()
    partitions_list = []
    weight_limit = 10
    #make partitions_list, a list of lists of valid trips
    for partition in get_partitions(cow_dict):
        for trip in partition:
            trip_weight = 0
            #calculate trip_weight
            for cow in trip:
                trip_weight += int(cow_dict[cow])
            if trip_weight > weight_limit:
                break
            partitions_list += [partition]
    #find best partition
    return max(partitions_list)


        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    greedy_cow_transport(load_cows("ps1_cow_data.txt"), 10)
    end = time.time()
    print("Greedy algorythm run time is:")
    print (end - start)
    
    start = time.time()
    brute_force_cow_transport(load_cows("ps1_cow_data.txt"), 10)
    end = time.time()
    print("Brute force algorythm run time is:")
    print (end - start)
    
compare_cow_transport_algorithms()
print("brute force:")
print(brute_force_cow_transport(load_cows("ps1_cow_data.txt"), 10))
print("greedy:")
print(greedy_cow_transport(load_cows("ps1_cow_data.txt"), 10))