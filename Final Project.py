# Andrew Michaud
# Original:
# 11/23/11-12/8/11
# Updated/cleaned:
# 17 Feb 2015
# CS 5 Green
# Final Project


# Comments on my project:

# I tested my code mostly by just running the GA function (usually with 200
# individuals and 10-20 generations), and obseving what happened.  I tried
# changing several variables around, especially the mutation rate and top
# fraction. I also tried messing with the number of states. Some things I
# noticed: A higher mutation rate got good programs quickly, but was also
# likely to mess up those good programs.  Fewer states led to worse programs,
# probably because the function had a harder time making good programs with
# fewer states.

# The best program I ever got was a .95 fitness program. It consistently
# covered .95 of the board, regardless of the starting point, and only ignored
# a strip on one wall of the board (the one behind its direction of motion. It
# moved up and down to cross the room, moving left, and moved all the way to
# the right after reaching the left wall. It did some weird motion that made it
# skip some of the right wall, and then repeated itself. I included it in code
# below, as a program and Picobot. It can be called as bestPicobot.
import random
import time
import math
import visual
from Vector import *
from Shapes import *

# These are various global variables that govern fitness testing and the
# generation of Program and Picobot objects. Specifically:

# These are used to make Picobot and Program objects. There are 23 rows and
# columns because that is the size of the online Picobot grid.
ROWS = 23
COLUMNS = 23
STATES = 5
allowedPatterns = ['xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS', 'xxWS',
                   'xExx', 'xxWx']
# These are variables for evaluating fitness and creating new generations.
TRIALS = 20
STEPS = 500
MUTATIONRATE = 0.02
TOPFRACTION = 0.2
# This is used by the functions I wrote that generate the empty room for the
# Picobot object, and the set of keys for the Program class.
# Ideally, it can be set to any room type and Picobots will evolve to conquer
# it. It works well with an empty room, but I'm still working on the other
# types.  I took out all the code that enabled me to generate code for mazes,
# because it never worked that well and it made things messy.

# Types: "Empty Room"
GRID = "Empty Room"


def GA(popSize, numGen):
    """Runs the genetic algorithm with a set population size and number of
    generations"""
    # These just print information about the testing for the user.
    print "Grid size is "+str(ROWS)+" rows by "+str(COLUMNS)+" columns."
    print "Fitness is measured using "+str(TRIALS)+" random trials and "\
        + str(STEPS) + " steps."
    # An initial program list is created, and several variables are
    # initialized for use later.
    programs = newPop(popSize)
    totalFitness = 0
    avgFitness = 0
    bestFitness = 0

    # This loops over the desired number of generations,
    for gen in range(numGen):

        # creating a new empty fitness dictionary each time.
        fitnessDict = {}

        # The program list is looped over so each program can have its fitness
        # evaluated, and stored in the dictionary.  The programs are stored
        # as values (their fitnesses being the keys) so they can be called back
        # later if they happen to be the best program.
        for program in programs:
            fitness = evaluateFitness(program, TRIALS, STEPS)
            fitnessDict[fitness] = program

        # The keys are taken out as a list, sorted, and reversed so they go
        # from greatest to smallest fitness.
        fitnessList = fitnessDict.keys()
        fitnessList.sort()
        fitnessList.reverse()

        # The best fitness is the maximum item in the list, and the total
        # fitness is the sum of the list.  It is averaged by dividing by the
        # size of the population. The best bot is also defined here.
        bestFitness = max(fitnessList)
        bestBot = Picobot(10, 10, fitnessDict[bestFitness])
        totalFitness = sum(fitnessList)
        avgFitness = totalFitness/popSize

        # Information about the generation is printed, including the fitnesses
        # we've just calculated.
        print "Generation "+str(gen)
        print " Average fitness: "+str(avgFitness)
        print " Best fitness: "+str(bestFitness)+"\n"

        # Helper functions are used to generate the next generation of programs
        # and to mutate a proprtion of the newly created programs.
        programs = nextGen(TOPFRACTION, fitnessDict, fitnessList, popSize)
        mutate(MUTATIONRATE, programs)

    while True:
        # This lets the best Picobot be visualized. It asks the user if he or
        # she wants to visualize the program.
        answer = input("Do you want to see this Picobot visualized? ")

        # If he or she answers one of several versions of yes, the visualize
        # method is run.
        if answer == "Y" or answer == "Yes" or answer == "yes" or answer == "Yeah"\
           or answer == 'y':
            bestBot.visualize()

        # Otherwise, the function just returns the best program, as a set of
        # rules.
        else:
            return fitnessDict[bestFitness]


def nextGen(survivorProp, fitnessDict, fitnessList, popSize):
    """Creates the next generation based on the previous one"""

    # This creates a new generation for GA().
    # These will store programs for us.
    newGen = []
    survivors = []

    # The function decides how many programs survive based on the what percent
    # should survive. It rounds up.
    numSurvivors = int(math.ceil(TOPFRACTION*popSize))

    # As long as there are more spaces, the function adds more to the survivor
    # list. Because fitnessList has been sorted, they are picked in order of
    # fitness.
    for survivor in range(numSurvivors):
        survivors.append(fitnessDict[fitnessList[survivor]])
        print len(fitnessDict)

    # Next, it crosses over two parents at random until it has a population
    # of the right size.
    while len(newGen) < popSize:
        parent1 = random.choice(survivors)
        parent2 = random.choice(survivors)

        # It makes sure two random parents aren't the same parent before
        # crossing over.
        if parent1 != parent2:
            offspring = parent1.crossover(parent2)
            newGen.append(offspring)
    # The list of offpsring are returned at the end.
    return newGen


def mutate(mutProp, programs):
    """Mutates a given percent of a population of programs"""

    # This function starts by determining how many programs should be mutated.
    # It rounds up or down.
    mutNum = int(len(programs)*mutProp)

    # As long as more need to be mutated, programs are chosen at random and
    # mutated, only changing the outcome of one of their rules.
    for index in range(mutNum):
        program = random.choice(programs)
        program.mutate()


def newPop(popSize):
    """Given a population size, returns a population of random Picobot
    programs"""
    # This is a helper program for GA().
    programList = []

    # It creates a random population of programs, up to a given population
    # size.
    for individual in range(popSize):

        # The programs are created, randomized, added to a list, and returned
        # at the end.
        newProg = Program()
        newProg.randomize()
        programList.append(newProg)
    return programList


def evaluateFitness(program, trials, steps):
    """Evaluates the fitness of a Picobot program"""
    # This keeps track of the squares visited.
    totalSquares = 0

    # The function runs the program trials times.
    for trial in range(trials):

        # testBot = Picobot(0, 0, program)
        # It is given to a Picobot object, along with a random starting row and
        # column.
        randRow = random.choice(range(1, ROWS+1))
        randCol = random.choice(range(1, COLUMNS+1))
        testBot = Picobot(randRow, randCol, program)

        # The Picobot is run for the given number of steps and its squares
        # tallied.
        testBot.run(steps)
        totalSquares += testBot.numvisited

    # The squares are averaged then normalized by dividing by first the number
    # of trials, then the number of squares. The fitness is returned in the
    # end.
    avgSquares = totalSquares/(trials*1.0)
    fitness = avgSquares/(ROWS*COLUMNS)
    return fitness


def gridMaker(roomType):
    """Creates an empty room for a Picobot object"""

    # This creates an array for a Picobot.
    array = []

    # The function generates the room for an empty room.
    row = []

    # For an empty room, it starts by creating a wall COLUMNS columns long.
    # Actually, two more, because we want the empty space to have
    # ROWS*COLUMNS spaces.
    for c in range(COLUMNS+2):
        row.append("W")
    array.append(row)
    row = []

    # For the rest of the rows, a wall is appended to the beginning, and
    # empty spaces are added for as many columns as there should be. Another
    # wall is added to the end.  This whole row is added to the array.
    for r in range(ROWS):
        row = []
        row.append("W")
        for c in range(COLUMNS):
            row.append(" ")
        row.append("W")
        array.append(row)
        row = []

    # Another wall is added to the end of the array, the same length as the
    # first. This leaves the Picobot with a walled room with ROWS*COLUMNS
    # empty squares in the middle.
    for c in range(COLUMNS+2):
        row.append("W")
    array.append(row)

    # The array is returned to the Picobot object.
    return array


def keyMaker(roomType):
    """Creates a list of dictionary keys for a Picobot object, based on the room
    type"""
    # This program creates all possible keys for Picobot (all the situations it
    # can find itself in) based on the given room type.

    roomPatterns = allowedPatterns

    # These are all possible directions for movement.
    directions = ['N', 'E', 'W', 'S', 'X']

    # These are variables that will be used shortly.
    allowedDirections = []
    keyList = []

    # The method loops over all patterns and rules to create a rule for
    # every possible situation picobot can find itself in.
    for pattern in roomPatterns:
        for state in range(STATES):

            # This for loop is different. It loops over the pattern the
            # function is currently looking at, and removes the directions that
            # are in that pattern from the list of possible directions.
            # This prevents the method from creating a rule that is not
            # possible to fulfill.
            for char in directions:
                if char not in pattern:
                    allowedDirections.append(char)

            # Each created key is appended to the list we will return, and
            # the allowed directions are reset so they can be recreated.
            keyList.append(((state, pattern), allowedDirections))
            allowedDirections = []

    return keyList


class Program:
    def __init__(self):
        """Initializes a program by creating an empty rules dictionary"""
        self.rulesDict = {}

    def randomize(self):
        """Randomizes a program, filling its dictionary with a set of rules
        that are random but cover every possible Picobot state"""
        # This gives the keys to the program, so it knows the possible states
        # for the current room type. GRID is a global variable we've set above.
        values = keyMaker(GRID)

        # For every key, a random direction and state are chosen.  The keyMaker
        # function provides the possible directions to travel in given the
        # current state.
        for key in values:
            newDirection = random.choice(key[1])
            newState = random.choice(range(STATES))
            self.rulesDict[key[0]] = (newDirection, newState)

    def getMove(self, state, pattern):
        """Given a Picobot's current state, finds its next move"""
        # This function simply uses the rules dictionary to find the next move
        # for the given situation.
        newState = self.rulesDict[(state, pattern)]
        return newState

    def mutate(self):
        """Chooses a rule at random and changes the move and new state"""
        # A random key is chosen.
        victim = random.choice(self.rulesDict.keys())
        directions = ['N', 'E', 'W', 'S', 'X']

        # The old value for that key is stored.
        oldNext = self.rulesDict[victim]
        newNext = oldNext

        # This while loop prevents the same rule from being chosen again.
        while newNext == oldNext:

            # The same process as in the randomize method is used here to
            # choose a new value for this key.
            for char in victim[1]:
                    if char != 'x' and char in directions:
                        directions.remove(char)
            randDirection = random.choice(directions)
            randState = random.choice(range(STATES))
            newNext = (randDirection, randState)

        # The key is assigned the new value the method has chosen.
        self.rulesDict[victim] = newNext

    def crossover(self, other):
        """Creates an offspring program based on two parent programs (self
        and other)"""
        # A random state is chosen for the crossover point, and an offspring
        # program is initialized.
        crossState = random.choice(range(STATES))
        offspring = Program()

        # This loops over every key in the self program, and adds every rule
        # for a state below (or at) our crossover point to the offspring's
        # dictionary.
        for current in self.rulesDict.keys():
            if current[0] <= crossState:
                offspring.rulesDict[current] = self.rulesDict[current]

        # This does the same, but for states above the crossover point and for
        # the "other" program.
        for current in other.rulesDict.keys():
            if current[0] > crossState:
                offspring.rulesDict[current] = other.rulesDict[current]

        # The offspring is returned to whoever called the function.
        return offspring

    def __repr__(self):
        """Prints out the code representing a program"""
        # This is the string that will hold the program.
        code = []

        # The method sorts the keys to make the output look nicer.
        keyList = self.rulesDict.keys()
        keyList.sort()

        # This loops over every key.
        for item in keyList:

            # The tuples for both the keys and the values are broken into
            # strings, and arranged in the way picobot expects its rules
            # to be. This makes it easier to read for the user and enables
            # the code to be pasted directly into the picobot simulator for
            # testing/fun.
            first = str(item[0])+" "+str(item[1])
            second = str(self.rulesDict[item][0]) + " " + \
                str(self.rulesDict[item][1])
            code.append(" -> ".join((first, second)) + "\n")

        # The code is returned at the end.
        return " "+" ".join(code)


class Picobot:
    def __init__(self, picobotrow, picobotcol, program):
        """Initializes a picobot with a row, column, and program."""
        # This sets up the picobot with its row, column, and program.
        self.row = picobotrow
        self.column = picobotcol
        self.program = program

        # It has its initial state set to zero and its visited squares empty,
        # to begin with.
        self.state = 0
        self.visited = []
        self.numvisited = 0

        # The picobot gets an array that represents the current room. gridMaker
        # decides what the room looks like based on what the room is set to.
        self.array = gridMaker(GRID)
        return

    def step(self):
        """Moves the Picobot one step using its program"""
        # The Picobot starts by adding its current room and column to its visited
        # squares, if it hasn't already. It also increments the number of visited
        # squares.
        if (self.row, self.column) not in self.visited:
            self.visited.append((self.row, self.column))
            self.numvisited += 1

        # The Picobot creates a list of the four squares surrounding it. It
        # records what is in those squares, and which direction they are in.
        relevantSquares = []
        relevantSquares.append((self.array[self.row-1][self.column], "N"))
        relevantSquares.append((self.array[self.row][self.column+1], "E"))
        relevantSquares.append((self.array[self.row][self.column-1], "W"))
        relevantSquares.append((self.array[self.row+1][self.column], "S"))

        # The surroundings are intialized (they'll be in the form 'xxxx').
        surroundings = []

        # For each square surrounding the Picobot, the Picobot decides if it's
        # a wall or not. If it is, it appends the direction to its
        # surroundings.  If it isn't, it appends an 'x'.
        for square in relevantSquares:
            if square[0] == "W":
                surroundings.append(square[1])
            else:
                surroundings.append("x")

        # The surroundings are turned into a string, the way the other
        # functions (and the online simulator) expects them to be.
        surroundings = "".join(surroundings)

        # The Picobot uses its program to decide what state it should switch to
        # next, and which direction it should move in. getMove returns state
        # and direction in the form ('N', 0).
        there = self.program.getMove(self.state, surroundings)

        # This changes the state
        self.state = there[1]
        direction = there[0]

        # This actually moves the Picobot, by changing its position in the
        # array.
        if direction == "N":
            self.row -= 1
        elif direction == "E":
            self.column += 1
        elif direction == "W":
            self.column -= 1
        elif direction == "S":
            self.row += 1
        else:
            self.row += 0

    def run(self, steps):
        """Calls the step method "steps" times"""
        # This simply calls step() as many times as we would like it to be
        # called.
        for steps in range(steps):
            self.step()

    def __repr__(self):
        """Displays the maze, Picobot's position, and visited squares."""
        # The method makes every visited square a . in the array.
        for square in self.visited:
            self.array[square[0]][square[1]] = "."

        # Picobot itself is represented as a "P". The walls have already
        # been represented as "W"'s.
        self.array[self.row][self.column] = "P"
        room = ""

        # The array is turned into a string, with each row broken separated
        # from the next by a newline character.
        for row in self.array:
            for char in row:
                room += char + " "
            room += "\n"

        # The room is returned at the end.
        return room

    def clear(self):
        """Clears a Picobot's visited squares so it can be run again"""
        # This is used so you can draw the same program several times in a row
        # and have a clean slate each time.
        # It resets every visited square to an " ",
        for square in self.visited:
            self.array[square[0]][square[1]] = " "

        # ...and clears both the visited tally and list.
        self.visited = []
        self.numvisited = 0

    def visualize(self):
        """Shows the best Picobot program solving the empty room"""
        # This is my visualization method.
        # It starts by asking what type of visualization to use, and how many
        # steps to run it for.
        visType = input("What visualization type would you like to see?"\
                        "('ASCII', '2D', or '3D') ")
        steps = input("How many steps would you "\
                      "like to run the visualization for? ")

        # ASCII simply uses the representation I wrote for a Picobot object.
        if visType == "ASCII":

            # It starts by clearing it,
            self.clear()

            # then prints itself and steps itself for the number of steps we
            # asked for.
            for step in range(steps):
                print self
                self.step()

        # 2D uses Turtle to draw the Picobot, and is therefore very slow.
        elif visType == "2D":
            # It clears itself, and speeds up the turtle slightly.
            self.clear()
            turtle.speed(0)
            turtle.hideturtle()

            # The walls are initialized as an empty list.
            wallVectors = []

            # The method loops through the array to find all walls, and adds
            # their positions to the list of walls.
            for row in range(len(self.array)):
                for box in range(len(self.array[row])):
                    if self.array[row][box] == "W":
                        pos = Vector(box, row)
                        wallVectors.append(pos)

            # To render properly in turtle, the positions are scaled. The array
            # starts at (0,0), but we don't want turtle to start by rendering
            # there. Every position is moved over by half the number of columns
            # and up by half the number of rows.
            for vector in wallVectors:
                vector.x-=COLUMNS/2.0
                vector.x = vector.x*10
                vector.y-=ROWS/2.0
                vector.y = vector.y*10

                # Each wall is then rendered as a square, colored blue.
                wall = Square(width = 10, center = vector, color="Blue")
                wall.render()

            # The Picobot position is also scaled.
            xPos = (self.column - COLUMNS/2.0)*10
            yPos = (self.row - ROWS/2.0)*10
            botPos = Vector(xPos, yPos)

            # The Picobot is rendered as a green square.
            Picobot = Square(width=10, center=botPos, color="Green")
            Picobot.render()

            # For each step,
            for step in range(steps):

                # the current Picobot position is overridden with a grey
                # square,
                lastSquare = Vector(xPos, yPos)
                lastVisited = Square(width=10, center=lastSquare, color="Gray")
                lastVisited.render()

                # Picobot's program is advanced, a new position is chosen,
                self.step()
                xPos = (self.column - COLUMNS/2.0)*10
                yPos = (self.row - ROWS/2.0)*10
                botPos = Vector(xPos, yPos)

                # ...and Picobot is rendered again.
                Picobot = Square(width=10, center=botPos, color="Green")
                Picobot.render()

        # The 3D rendering uses VPython.
        elif visType == "3D":

            # This is initialized much like the 2D rendering, but floor tiles
            # are needed as well.
            self.clear()
            wallVectors = []
            floorVectors = []

            # So, both floor and wall tiles are stored.  For reasons I didn't
            # quite understand, the rows needed to be changed by making them
            # negative and adding one.  This made VPython properly render
            # the Picobot.
            for row in range(len(self.array)):
                for box in range(len(self.array[row])):
                    if self.array[row][box] == "W":
                        pos = Vector(-row + 1, box)
                        wallVectors.append(pos)
                    else:
                        pos = Vector(-row + 1, box)
                        floorVectors.append(pos)

            # Just like before, the walls are rendered as blue boxes, after
            # being scaled to account for array/VPython differences.  Because
            # we are in 3D now, the board is set up so that it faces the user
            # immediately, for convenience.
            for vector in wallVectors:
                vector.y -= ROWS/2.0
                vector.x += COLUMNS/2.0
                visual.box(pos=(vector.x, vector.y, 0), color=(0, 0, 1))

            # VPython doesn't have a white background, so the floor is rendered
            # as well. The floor is made of white boxes, which are set lower
            # down and made less wide (deep, really) so that they look like
            # tiles.  The rows need to be scaled a bit differently than for
            # Turtle, again for reasons I didn't quite understand (I just
            # played with it until it worked).
            for vector in floorVectors:
                vector.y -= ROWS/2.0
                vector.x += COLUMNS/2.0
                visual.box(pos=(vector.x, vector.y, -.45), width=0.1)

            # Picobot is rendered about the same, except its position also is
            # scaled weirdly to make it work.
            yPos = -(self.row - ROWS/2.0 - 1)
            xPos = self.column - COLUMNS/2.0

            # Picobot is a green box, same size as the walls.
            Picobot = visual.box(pos=(xPos, yPos, 0), color=(0, 1, 0))

            # It is made visible after rendering. It gets made invisible while
            # we render squares that have been moved over, so it appears to
            # move.
            Picobot.visible = True

            # For each step, we make Picobot invisible, render a covered square
            # at Picobot's position (slightly less wide and higher than the
            # floor squares, so in theory they don't overlap), and then redraw
            # Picobot at its new position (making it visible again).
            for step in range(steps):
                Picobot.visible = False
                lastSquare = (xPos, yPos)
                lastVisited = visual.box(pos=(lastSquare[0], lastSquare[1],
                                              -0.3),
                                         width=.04,
                                         color=(0.5, 0.5, 0.5))
                self.step()
                yPos = -(self.row - ROWS/2.0 - 1)
                xPos = self.column - COLUMNS/2.0
                Picobot = visual.box(pos=(xPos, yPos, .15), color=(0, 1, 0))
                Picobot.visible = True

                # Without this, Picbot renders too quickly to see. With this
                # slight delay, it animates nicely.
                time.sleep(.01)


def converter(s):
    """Takes picobot code, as a string, and returns a picobot dictionary"""
    # I made this so I could feed programs returned by GA back into Picobots
    # and render them. It takes a Picobot program, formatted as follows:
    # """
    # 2 xxxS -> W 0
    # 2 xxxx -> S 2
    # 3 NExx -> W 1
    # """
    # (spacing important) and turns it into a dictionary that a Picobot object
    # can use.
    picobotDict = {}

    # It splits the input string at the newline characters,
    L = s.split('\n')

    # and for each item in that list,
    for item in L[1:]:

        # splices the item into a properly formatted key and value.
        key = (int(item[1]), str(item[3:7]))
        value = (str(item[11]), int(item[13]))

        # The key and value are added to the dictionary.
        picobotDict[key] = value

    # The dictionary is returned.
    return picobotDict

# This is the best program I've managed to make so far (fitness: about 0.95,
# independent of starting position, I believe). It's already defined as a
# program, dictionary, and Picobot object (scroll down for the last one). I
# used it for testing my visualize method and for general entertainment.
goodProgram = Program()
goodProgram.rulesDict = {
    (1, 'xxWS'): ('E', 0), (3, 'xxxS'): ('N', 4), (3, 'NExx'): ('S', 3),
    (3, 'xExS'): ('N', 2), (2, 'xxWS'): ('X', 3), (2, 'xExx'): ('W', 4),
    (1, 'xxxS'): ('E', 1), (2, 'Nxxx'): ('X', 3), (4, 'Nxxx'): ('W', 3),
    (0, 'xxxx'): ('S', 3), (1, 'xExS'): ('W', 3), (4, 'NxWx'): ('E', 4),
    (2, 'xxxx'): ('X', 1), (4, 'xExS'): ('X', 1), (3, 'xxWS'): ('E', 4),
    (4, 'xxWx'): ('N', 0), (0, 'xxxS'): ('N', 0), (1, 'xxxx'): ('N', 0),
    (2, 'xExS'): ('W', 0), (3, 'NxWx'): ('S', 2), (2, 'NExx'): ('S', 3),
    (4, 'xxWS'): ('X', 2), (4, 'xExx'): ('X', 1), (1, 'xExx'): ('W', 0),
    (0, 'Nxxx'): ('X', 2), (4, 'xxxx'): ('N', 4), (2, 'NxWx'): ('S', 1),
    (2, 'xxxS'): ('X', 0), (3, 'xxWx'): ('S', 3), (1, 'xxWx'): ('X', 0),
    (4, 'NExx'): ('W', 0), (3, 'xxxx'): ('S', 0), (0, 'xxWS'): ('X', 2),
    (1, 'NxWx'): ('S', 4), (0, 'xExx'): ('S', 2), (1, 'NExx'): ('X', 4),
    (1, 'Nxxx'): ('W', 4), (2, 'xxWx'): ('S', 0), (3, 'Nxxx'): ('S', 0),
    (4, 'xxxS'): ('X', 1), (3, 'xExx'): ('N', 1), (0, 'xExS'): ('N', 4),
    (0, 'NxWx'): ('E', 2), (0, 'xxWx'): ('X', 2), (0, 'NExx'): ('W', 2)
}

bestPicobot = Picobot(10, 10, goodProgram)
