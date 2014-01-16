#Andrew Michaud
#12/3/11
#CS 5 Green
#Picobot Project Milestone

import random

ROWS = 20
COLUMNS = 20
STATES = 5
TRIALS = 20
STEPS = 800
allowedPatterns = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx',
                   'xxWx']

class Program:
    def __init__(self):
        """Initializes a program by creating an empty rules dictionary"""
        self.rulesDict = {}

    def randomize(self):
        """Randomizes a program, filling its dictionary with a set of rules
        that are random but cover every possible Picobot state"""
        #These are all possible directions for movement.
        directions = ['N', 'E', 'W', 'S', 'X']
        #The method loops over all patterns and rules to create a rule for
        #every possible situation picobot can find itself in.
        for pattern in allowedPatterns:
            for state in range(STATES):
                #This for loop is different. It loops over the pattern the
                #function is currently looking at, and removes the directions
                #that are in that pattern from the list of possible directions.
                #This prevents the method from creating a rule that is not
                #possible to fulfill.
                for char in pattern:
                    if char in directions:
                        directions.remove(char)
                #When that is finished, the method creates a key based on the
                #state and pattern it is looking at, and creates a value based
                #on a random direction and state. Both are added to the
                #dictionary.
                current = (state, pattern)
                newDirection = random.choice(directions)
                newState = random.choice(range(STATES))
                self.rulesDict[current] = (newDirection, newState)
                #The directions are reset for the next time through the loop.
                directions = ['N', 'E', 'W', 'S', 'X']

    def getMove(self, state, pattern):
        """Given a Picobot's current state, finds its next move"""
        #This function simply uses the rules dictionary to find the next move
        #for the given situation.
        newState = self.rulesDict[(state, pattern)]
        return newState

    def mutate(self):
        """Chooses a rule at random and changes the move and new state"""
        #A random key is chosen.
        victim = random.choice(self.rulesDict.keys())
        directions = ['N', 'E', 'W', 'S', 'X']
        #The old value for that key is stored.
        oldNext = self.rulesDict[victim]
        newNext = oldNext
        #This while loop prevents the same rule from being chosen again.
        while newNext == oldNext:
            #The same process as in the randomize method is used here to
            #choose a new value for this key.
            for char in victim[1]:
                    if char!='x' and char in directions:
                        directions.remove(char)
            randDirection = random.choice(directions)
            randState = random.choice(range(STATES))
            newNext = (randDirection, randState)
        #The key is assigned the new value the method has chosen.
        self.rulesDict[victim] = newNext

    def crossover(self, other):
        """Creates an offspring program based on two parent programs (self
        and other)"""
        #A random state is chosen for the crossover point, and an offspring
        #program is initialized.
        crossState = random.choice(range(STATES))
        offspring = Program()
        #This loops over every key in the self program, and adds every rule
        #for a state below (or at) our crossover point to the offspring's
        #dictionary.  
        for current in self.rulesDict.keys():
            if current[0] <= crossState:
                offspring.rulesDict[current] = self.rulesDict[current]
        #This does the same, but for states above the crossover point and for
        #the "other" program.
        for current in other.rulesDict.keys():
            if current[0] > crossState:
                offspring.rulesDict[current] = other.rulesDict[current]
        #The offspring is returned to whoever called the function.
        return offspring

    def __repr__(self):
        """Prints out the code representing a program"""
        #This is the string that will hold the program.
        code = ""
        #The method sorts the keys to make the output look nicer.
        keyList=self.rulesDict.keys()
        keyList.sort()
        #This loops over every key.
        for item in keyList:
            #The tuples for both the keys and the values are broken into
            #strings, and arranged in the way picobot expects its rules
            #to be. This makes it easier to read for the user and enables
            #the code to be pasted directly into the picobot simulator for
            #testing/fun.
            first = str(item[0])+" "+str(item[1])
            second = str(self.rulesDict[item][0])+" "+str(self.rulesDict[item][1])
            code+=first + " -> " + second+"\n"
        #The code is returned at the end.
        return code

#Testing the Program class.
    
#I created two new programs p1 and p2.  They were started with empty
#dictionaries, and returned nothing if called. I then randomized them to get
#two random programs. I also got to test the __repr__ method in finding what
#the results were so I could paste them here.
    
##p1:
    
##0 NExx -> X 0
##0 NxWx -> E 1
##0 Nxxx -> W 1
##0 xExS -> W 1
##0 xExx -> N 1
##0 xxWS -> X 1
##0 xxWx -> N 0
##0 xxxS -> W 0 This rule is mutated below.
##0 xxxx -> E 0
##1 NExx -> W 1
##1 NxWx -> X 1
##1 Nxxx -> W 1
##1 xExS -> X 1
##1 xExx -> X 0
##1 xxWS -> E 1
##1 xxWx -> X 1
##1 xxxS -> E 0
##1 xxxx -> E 0
    
##p2:
    
##0 NExx -> X 0
##0 NxWx -> X 0
##0 Nxxx -> S 0
##0 xExS -> N 0
##0 xExx -> X 0
##0 xxWS -> E 1
##0 xxWx -> E 1
##0 xxxS -> E 1
##0 xxxx -> X 1
##1 NExx -> W 1
##1 NxWx -> S 1 This rule was mutated below.
##1 Nxxx -> X 0
##1 xExS -> N 1
##1 xExx -> X 0
##1 xxWS -> X 0
##1 xxWx -> E 1
##1 xxxS -> E 0
##1 xxxx -> X 1
    
#I mutated them next to test my mutate() function.
    
##p1:
    
##0 NExx -> X 0
##0 NxWx -> E 1 
##0 Nxxx -> W 1
##0 xExS -> W 1
##0 xExx -> N 1
##0 xxWS -> X 1
##0 xxWx -> N 0
##0 xxxS -> N 1  This rule was mutated.
##0 xxxx -> E 0
##1 NExx -> W 1
##1 NxWx -> X 1
##1 Nxxx -> W 1
##1 xExS -> X 1
##1 xExx -> X 0
##1 xxWS -> E 1
##1 xxWx -> X 1
##1 xxxS -> E 0
##1 xxxx -> E 0

##p2:
    
##0 NExx -> X 0
##0 NxWx -> X 0
##0 Nxxx -> S 0
##0 xExS -> N 0
##0 xExx -> X 0
##0 xxWS -> E 1
##0 xxWx -> E 1
##0 xxxS -> E 1
##0 xxxx -> X 1
##1 NExx -> W 1
##1 NxWx -> S 0 This rule was mutated.
##1 Nxxx -> X 0
##1 xExS -> N 1
##1 xExx -> X 0
##1 xxWS -> X 0
##1 xxWx -> E 1
##1 xxxS -> E 0
##1 xxxx -> X 1
#Everything seems to be working there.
    
#Finally, I tested the crossover function, as "p1.crossover(p2)"
#The offspring:
##0 NExx -> X 0 It appears the function chose 0 as the crossover state.
##0 NxWx -> E 1 This would take every rule with a state less than or equal to
##0 Nxxx -> W 1 0 from p1 (which appears to have happened), and every rule with
##0 xExS -> W 1 a state greater than 0 from p2 (which also appears to have 
##0 xExx -> N 1 happened.  Everything seems in order here as well.
##0 xxWS -> X 1
##0 xxWx -> N 0
##0 xxxS -> N 1
##0 xxxx -> E 0
##1 NExx -> W 1
##1 NxWx -> S 0
##1 Nxxx -> X 0
##1 xExS -> N 1
##1 xExx -> X 0
##1 xxWS -> X 0
##1 xxWx -> E 1
##1 xxxS -> E 0
##1 xxxx -> X 1   
                        
