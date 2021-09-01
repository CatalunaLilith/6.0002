# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement



# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))
    
    def __repr__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        room = []
        for row in range(self.width):
            room.append([])
            for column in range(self.height):
                room[row].append(self.dirt_amount)
        self.room = room
            
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        old_dirt_amount = self.room[math.floor(pos.get_x())][math.floor(pos.get_y())]
        new_dirt_amount = old_dirt_amount - capacity
        if new_dirt_amount <0:
            new_dirt_amount = 0
        self.room[math.floor(pos.get_x())][math.floor(pos.get_y())] = new_dirt_amount

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return self.room[m][n] == 0
        
    
    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        clean_tiles = 0
        for row in self.room:
            for item in row:
                if item == 0:
                    clean_tiles += 1
        return clean_tiles
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        try:
            self.room[math.floor(pos.get_x())][math.floor(pos.get_y())]
            return True
        except:
            return False
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.room[m][n]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        
        
    def print_room(self):
        for row in self.room:
            print(str(row))
            
            
# aroom = RectangularRoom(5,4,4)
# apos = Position(2,3)
# aroom.clean_tile_at_position(apos, 5)
# aroom.clean_tile_at_position(Position(4,2), 5)
# print(aroom.is_tile_cleaned(0,2))
# print(aroom.is_tile_cleaned(2,3))
# print(aroom.get_num_cleaned_tiles())
# print(aroom.is_position_in_room(Position(6,3)))
# print(aroom.get_dirt_amount(2,3))
# aroom.print_room()


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        direction: an int from 0 to 360; the degrees from North of the orientation of the robot
        position: a Position object; the robot's position inside the room
        """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        #random direction (0 to 360)
        self.direction = 360 * random.random()
        #random position (in room w by h)
        have_a_pos = False
        while have_a_pos == False:
            a_pos = Position((self.room.width*random.random()),(self.room.height*random.random()))
            if (self.room).is_position_valid(a_pos):
                self.position = a_pos
                have_a_pos = True
        # self.position = Position((self.room.width*random.random()),(self.room.height*random.random()))

        
    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction
    
    def get_robot_speed(self):
        return self.speed
    
    def get_robot_room(self):
        return self.room
    
    def get_robot_capacity(self):
        return self.capacity

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width * self.height
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        # try:
        #     self.room[pos.get_x()][pos.get_y()]
        #     return True
        # except:
        #     return False
        return pos.get_x() >= 0 and pos.get_x() < self.width and pos.get_y() >= 0 and pos.get_y() < self.height

        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        return Position((self.width*random.random()),(self.height*random.random()))

# an_empty_room = EmptyRoom(5,4,4)
# apos = Position(2,3)
# an_empty_room.clean_tile_at_position(apos, 5)
# an_empty_room.clean_tile_at_position(Position(4,2), 2)
# print(an_empty_room.is_tile_cleaned(0,2))
# print(an_empty_room.is_tile_cleaned(2,3))
# print(an_empty_room.get_num_cleaned_tiles())
# print(an_empty_room.is_position_in_room(Position(1,3)))
# print(an_empty_room.get_dirt_amount(4,2))
# print(an_empty_room.is_position_valid(Position(6,1)))
# an_empty_room.print_room()



class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             
                
    def get_furniture_tiles(self):
        return self.furniture_tiles
        
    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        return (m, n) in self.get_furniture_tiles()
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        return self.is_tile_furnished(math.floor(pos.get_x()),math.floor(pos.get_y()))

        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        return (self.is_position_furnished(pos) == False) and pos.get_x() >= 0 and pos.get_x() < self.width and pos.get_y() >= 0 and pos.get_y() < self.height

        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        num_furnished_tiles = len(self.get_furniture_tiles())
        num_total_tiles = self.width * self.height
        return num_total_tiles - num_furnished_tiles
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        x=1
        while x == 1:
            random_position = Position((self.width*random.random()),(self.height*random.random()))
            if self.is_position_valid(random_position):
                return random_position

# a_furnished_room = FurnishedRoom(5,4,3)
# a_furnished_room.add_furniture_to_room()
# print(a_furnished_room.get_furniture_tiles())
# print(a_furnished_room.is_tile_furnished(0,8))
# apos = Position(2,3)
# print(a_furnished_room.is_position_furnished(Position(2,2.1)))
# print(a_furnished_room.is_position_valid(Position(0,1)))
# print(a_furnished_room.is_position_valid(Position(0,1)))
# print(a_furnished_room.is_position_valid(Position(1,1)))
# print(a_furnished_room.is_position_valid(Position(1,2)))
# print(a_furnished_room.is_position_valid(Position(2,1)))
# print(a_furnished_room.is_position_valid(Position(2,2)))
# print(a_furnished_room.is_position_valid(Position(3,1)))
# print(a_furnished_room.is_position_valid(Position(4.32432342,3.324342314)))
# print(a_furnished_room.get_num_tiles())
# print(a_furnished_room.get_random_position())

# a_furnished_room.clean_tile_at_position(apos, 5)
# a_furnished_room.clean_tile_at_position(Position(4,2), 2)
# print(a_furnished_room.is_tile_cleaned(0,2))
# print(a_furnished_room.is_tile_cleaned(2,3))
# print(a_furnished_room.get_num_cleaned_tiles())
# print(a_furnished_room.is_position_in_room(Position(1,9)))
# print(a_furnished_room.get_dirt_amount(4,2))
# print(a_furnished_room.is_position_valid(Position(3,3)))
# a_furnished_room.print_room()

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        #get new_pos with given direction and speed
        new_pos = self.get_robot_position().get_new_position(self.get_robot_direction(), self.get_robot_speed())
        if (self.get_robot_room()).is_position_valid(new_pos): #if new pos is valid
            #move to new pos and clean tile
            self.set_robot_position(new_pos)
            (self.get_robot_room()).clean_tile_at_position(new_pos, self.get_robot_capacity())
        else: #(new pos invalid)
            #get new random direction
            self.set_robot_direction(360 * random.random())

# Uncomment this line to see your implementation of StandardRobot in action!
test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)


# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        if self.gets_faulty():
            self.set_robot_direction(360 * random.random())
        #if not faulty, copy normal behaviour
        else:
            StandardRobot.update_position_and_clean(self)
        
    
# test_robot_movement(FaultyRobot, FurnishedRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    num_ticks_list = []
    # for each num_trials
    for trial in range(num_trials):
        #innitialize the trial
        a_room = EmptyRoom(width, height, dirt_amount)
        robot_list = []
        num_ticks = 0 
        for num in range(num_robots):
            #make a robot with speed, capacity, (default:random pos and direction)
            robot_list.append(robot_type(a_room, speed, capacity))
        #run the trial
        while (a_room.get_num_cleaned_tiles() / (width*height)) < min_coverage:
            for robot in robot_list:
                robot.update_position_and_clean()
            num_ticks += 1
        num_ticks_list.append(num_ticks)
    average_num_ticks = sum(num_ticks_list) / len(num_ticks_list)
    return average_num_ticks

# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 2, 2, 3, 1.0, 1, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.8, 50, FaultyRobot)))


# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
"""
(run_simulation(1, 1.0, 1, 20, 20, 3, 0.8, 50, StandardRobot)))
outputs avg time steps: 2066.1
(run_simulation(1, 1.0, 1, 20, 20, 3, 0.8, 50, FaultyRobot)))
outputs avg time steps: 2479.98

given these otherwise basic inputs of one robot, speed 1.0, capacity 1, 
and the arbitrary but simple inputs dirt_amount 3, and trials 50.
The StandardRobot runs in 83% of the time that the Faulty Robot does. 
Interestingly the FaultyRobot does eventually get the job done, 
in a calculatably longer time frame 
But the FaultyRobot is not so much slower that a busy consumer distracted by daily life
would nessesarily notice. 
Perhaps this batch wont need to be recalled, but can get away with some lesser compensation?
"""
#
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
"""
all of these simulations are run with the specified coverage .8, 2 robots, and room dimentions. 
and a default speed 1.0, capacity 1, dirt_amount 3, trials 50

print (str(run_simulation(2, 1.0, 1, 10, 30, 3, 0.8, 50, StandardRobot)))
792.96
print (str(run_simulation(2, 1.0, 1, 10, 30, 3, 0.8, 50, FaultyRobot)))
996.2
for an area of 10*30=300, in a 3:1 rectangle
The StandardRobot runs in 80% of the time that the Faulty Robot does.

print (str(run_simulation(2, 1.0, 1, 20, 15, 3, 0.8, 50, StandardRobot)))
784.42
print (str(run_simulation(2, 1.0, 1, 20, 15, 3, 0.8, 50, FaultyRobot)))
948.42
for an area of 20*15=300 in a ~1.3:1 rectangle (near a square)
The StandardRobot runs in 83% of the time that the Faulty Robot does.

print (str(run_simulation(2, 1.0, 1, 25, 12, 3, 0.8, 50, StandardRobot)))
794.46
print (str(run_simulation(2, 1.0, 1, 25, 12, 3, 0.8, 50, FaultyRobot)))
972.32
for an area of 20*12=240, in a ~2:1 rectangle 
The StandardRobot runs in 81% of the time that the Faulty Robot does.

print (str(run_simulation(2, 1.0, 1, 50, 6, 3, 0.8, 50, StandardRobot)))
842.4
print (str(run_simulation(2, 1.0, 1, 50, 6, 3, 0.8, 50, FaultyRobot)))
1213.34
for an area of 50*6=300, in ~8:1 a rectangle (very narrow)
The StandardRobot runs in 69% of the time that the Faulty Robot does.

notably the narrow 50:6 rectangle takes longer for either robot to clean, 
and takes the FaultyRobot an ever larger time proportionally to clean the room.

print (str(run_simulation(2, 1.0, 1, 50, 6, 3, 0.8, 50, StandardRobot)))
851.88
print (str(run_simulation(2, 1.0, 1, 50, 6, 3, 0.8, 50, FaultyRobot)))
1158.12
for an area of 150*1=300, in 150:1 a rectangle (extremely narrow)
The StandardRobot runs in 73% of the time that the Faulty Robot does.
This is again even slower for either robot type, 
the proportions of time seems to stay in the same range, 
it does not get even worst as predicted
"""
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
# show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')

anim = ps3_visualize.RobotVisualization(1, 20, 20, False, 0.2)