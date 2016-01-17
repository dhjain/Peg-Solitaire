import readGame

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################

#Hash for all explored states
executedStates = set()

#Final Goal State - One Peg at the center of the board
goalState = [[-1,-1,0,0,0,-1,-1],
            [-1,-1,0,0,0,-1,-1],
            [0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0],
            [-1,-1,0,0,0,-1,-1],
            [-1,-1,0,0,0,-1,-1]]
 
#For string representation of game state            
stateString = {}
#List of all directions
all_directions = ['N', 'S', 'E', 'W']


class game:
	def __init__(self, filePath):
		self.gameState = readGame.readGameState(filePath)
		self.nodesExpanded = 0
		self.trace = []

	#Function for checking if new move positon is a corner or not
        def is_corner(self, pos):
            ########################################
            # You have to make changes from here
            # check for if the new positon is a corner or not
            # return true if the position is a corner

            #Verification of corner cases.
            if ((pos[0] < 2 or pos[0] > 4) and (pos[1] < 2 or pos[1] > 4)):
                return True

            return False
        
        #Function for checking if new move is outside peg board or not
        def is_outsideBoard(self, pos):
            #Verification of outside of board cases.
            if (pos[0] < 0 or pos[0] > 6 or pos[1] < 0 or pos[1] > 6):
                return True

            return False
	
        #Function for getting next move position, position is updated by two steps in the specified direction
	def getNextPosition(self, oldPos, direction):
            #########################################
            # YOU HAVE TO MAKE CHANGES HERE
            # See DIRECTION dictionary in config.py and add
            # this to oldPos to get new position of the peg if moved
            # in given direction , you can remove next line

            if direction == 'N':
                return (oldPos[0] - 2,oldPos[1])

            if direction == 'S':
                return (oldPos[0] + 2,oldPos[1])

            if direction == 'E':
                return (oldPos[0],oldPos[1]+2)

            if direction == 'W':
                return (oldPos[0],oldPos[1]-2)

            return oldPos 
	
	#Function for checking if new move is valid move or not
	def is_validMove(self, oldPos, direction):
            #########################################
            # DONT change Things in here
            # In this we have got the next peg position and
            # below lines check for if the new move is a corner

            newPos = self.getNextPosition(oldPos, direction)
            if self.is_corner(newPos):
                return False	
            #########################################
            ########################################
            # YOU HAVE TO MAKE CHANGES BELOW THIS
            # check for cases like:
            # if new move is already occupied
            # or new move is outside peg Board
            # Remove next line according to your convenience

            #Check for outside peg Board
            if self.is_outsideBoard(newPos):
                return False
            
            #Check if new move is same as old move
            if oldPos == newPos:
                return False

            #Check if new move postion is already occupied.
            if self.gameState[newPos[0]][newPos[1]] == 1:
                return False

            #Check if peg is present in middle peg position in the move i.e. peg present at 1 step in the specified direction
            if not self.isJumpPegPresent(oldPos,direction):
                return False

            return True
	
        #Function for getting next game state according to a valid move
	def getNextState(self, oldPos, direction):
            ###############################################
            # DONT Change Things in here
            self.nodesExpanded += 1
            if not self.is_validMove(oldPos, direction):
                print "Error, You are not checking for valid move"
                exit(0)
            ###############################################

            ###############################################
            # YOU HAVE TO MAKE CHANGES BELOW THIS
            # Update the gameState after moving peg
            # eg: remove crossed over pegs by replacing it's
            # position in gameState by 0
            # and updating new peg position as 1

            #Get new move position
            newPos = self.getNextPosition(oldPos,direction)
            #Update peg board state accorsing to the new valid move
            self.updateBoard(oldPos,newPos,direction)

            return self.gameState	


        #Function to check if peg is present in middle peg position in the move i.e. peg present at 1 step in the specified direction
	def isJumpPegPresent(self,oldPos,direction):
            if direction == 'N':
                    return self.gameState[oldPos[0]-1][oldPos[1]]

            if direction == 'S':
                    return self.gameState[oldPos[0]+1][oldPos[1]]

            if direction == 'E':
                    return self.gameState[oldPos[0]][oldPos[1]+1]

            if direction == 'W':
                    return self.gameState[oldPos[0]][oldPos[1]-1]

            return False

        #Function to update the peg board according to next valid move
	def updateBoard(self,oldPos,newPos,direction):
            self.gameState[oldPos[0]][oldPos[1]] = 0
            self.gameState[newPos[0]][newPos[1]] = 1

            if direction == 'N':
                    self.gameState[oldPos[0]-1][oldPos[1]] = 0

            if direction == 'S':
                    self.gameState[oldPos[0]+1][oldPos[1]] = 0

            if direction == 'E':
                    self.gameState[oldPos[0]][oldPos[1]+1] = 0

            if direction == 'W':
                    self.gameState[oldPos[0]][oldPos[1]-1] = 0

            return


#Function to check if goal state is reached or not.
def isGoalState(currentState):
    for i in range(7):
        for j in range(7):
            if(currentState[i][j] != goalState[i][j]):
                return False

    return True


#This would act like a Hash to see if the state is already explored before.
def isAlreadyExplored(currentState):
    currentStateString = ""
    #Convert state to a String to Hash
    currentStateString = stateToString(currentState)

    if currentStateString in executedStates:
        return True

    executedStates.add(currentStateString)
    return False

#A function to return the list of Valid moves from original state.
def setValidMoves(pegSolitaireObject):
    setOfValidMoves = set()

    for row in xrange(7):
        for column in xrange(7):
            if pegSolitaireObject.gameState[row][column] == 1:
                for direction in all_directions:
                    if pegSolitaireObject.is_validMove((row,column),direction):
                        setOfValidMoves.add((row,column,direction))

    return setOfValidMoves

#Function to return the string representation of a gameState
def stateToString(gameState):
    gameStateString = ""

    for i in xrange(7):
	for j in xrange(7):
            gameStateString = gameStateString + str(gameState[i][j])

    stateString[gameStateString] = gameState
    return gameStateString

#Return a deep copy of game state array
def copyGameState(pegSolitaireObject):
    copy_game_state = [[0 for i in range(7)] for i in range(7)]
    for i in xrange(7):
        for j in xrange(7):
            copy_game_state[i][j] = pegSolitaireObject.gameState[i][j]

    return copy_game_state

#Restore the state to original game state to prepare it for alternate move
def restoreInitialState(pegSolitaireObject,initialState):
    for i in xrange(7):
        for j in xrange(7):
            pegSolitaireObject.gameState[i][j] = initialState[i][j]

    return

#To compute the trace of A* using parent dictionary
def computeTrace(parentStates, node,pegSolitaireObject):
    trace = []
    while not parentStates[node][0] == None:
        trace.append(parentStates[node][1])
        node = parentStates[node][0]

    for item in trace:
        pegSolitaireObject.trace.append(pegSolitaireObject.getNextPosition((item[0],item[1]),item[2]))
        pegSolitaireObject.trace.append((item[0],item[1]))

    pegSolitaireObject.trace.reverse()
    return


#This calculates function f(n) = g(n) + h(n) for a particular game state for A* One search.
def funcFforAStarOne(intialStartingState, currentState):
    return funcG(intialStartingState, currentState) + heuristic1(currentState)


#This calculates function f(n) = g(n) + h(n) for a particular game state for A* Two search.
def funcFforAStarTwo(intialStartingState, currentState):
    return funcG(intialStartingState, currentState) + heuristic2(currentState)
    

#This calculates function g(n) for a particular game state.
#Calulated using Sum of distances of every position in current game state from corresponding position in initial game state 
def funcG(intialStartingState, currentState):
    distance = 0
    for i in xrange(7):
        for j in xrange(7):
            distance = distance + abs(intialStartingState[i][j] - currentState.gameState[i][j])

    return distance    

#This calculates heuristic 1 for a particular game state.
#Sum of distances of every peg's position from center position (3,3)[Manhattan Distance]
def heuristic1(currentState):
    distance = 0
    for i in xrange(7):
        for j in xrange(7):
            if currentState.gameState[i][j] == 1:
                distance = distance + abs(i-3) + abs(j-3)

    return distance

#This calculates heuristic 1 for a particular game state.
#Sum of distances of every peg's position from middle of the peg board. 
def heuristic2(currentState):
    distance = 0
    for i in xrange(7):
        for j in xrange(7):
            if currentState.gameState[i][j] == 1:
                distance = distance + abs(i-3)

    return distance