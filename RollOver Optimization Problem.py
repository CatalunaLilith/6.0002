"""
The “Roll-over” Optimization Problem
Score	=	((60	–	(a+b+c+d+e))*F	+	a*ps1	+	b*ps2	+	c*ps3	+	d*ps4	+	e*ps5	
Objec<ve:	
Given	values	for	F,	ps1,	ps2,	ps3,	ps4,	ps5	
Find	values	for	a,	b,	c,	d,	e	that	maximize	score	
Constraints:	
								a,	b,	c,	d,	e	are	each	10	or	0	
a	+	b	+	c	+	d	+	e	≥	20
"""

def genSubsets(L):
    """L is a list of elements
    returns the powerset of L"""
    if len(L) == 0:
        return [[]]
    smaller = genSubsets(L[:-1])
    extra = L[-1:]
    new = []
    for small in smaller:
        new.append(small + extra)
    return smaller + new 


def RollOver(F, ps1, ps2, ps3, ps4, ps5):
    """returns list [a, b, c, d, e] representing the values to give a maximal score given the inputed grades
    Score=((60–(a+b+c+d+e))*F + a*ps1 + b*ps2 + c*ps3 + d*ps4 + e*ps5
    a,b,c,d,e must be 10 or 0
    a+b+c+d+e >= 20"""
    best_score = 0 
    power_set = genSubsets(["a", "b", "c", "d", "e"])
    power_set_copy = power_set.copy()
    #remove elements that dont meet criteria a+b+c+d+e >= 20
    for elem in power_set_copy:
         if len(elem)<2:
             power_set.remove(elem)
    #iterates over remainign power_set to find set that gives highest score
    for subset in power_set:
        #create list of values of ["a", "b", "c", "d", "e"]
        subset_values = []
        for char in "abcde":
            if char in subset:
                subset_values.append((10))
            else: 
                subset_values.append((0))
        #calculate score 
        a = subset_values[0]
        b = subset_values[1]
        c = subset_values[2]
        d = subset_values[3]
        e = subset_values[4]
        subset_score = (60-(a+b+c+d+e))*F + a*ps1 + b*ps2 + c*ps3 + d*ps4 + e*ps5
        #update bests
        if subset_score > best_score:
            best_score = subset_score
            best_set = subset
    return best_set
