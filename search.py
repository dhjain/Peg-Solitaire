import pegSolitaireUtils
import config
import Queue
import copy

#List of all directions
all_directions = ['N', 'S', 'E', 'W']

#Function for Iterative Deepening Search
def ItrDeepSearch(pegSolitaireObject):
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	# 
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you 
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you 
	# reach goal using Iterative Deepning Search.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to save
	#
	#################################################
    
    #Initially goal state is false
    found_goal_state = False
    
    #Run DFS for depth 0 to 32. The search can only go upto 32 as there are just 33 pegs.  
    for depth in xrange(32):
        #print "Depth", depth
        #Keep a hash of all explored states to prevent exploration of repeated states.
        pegSolitaireUtils.executedStates = set()
        
        #Do DFS with limited depth - "depth"
        found_goal_state = depthLimitedSearch(pegSolitaireObject, depth)
        #break if goal state is reached
        if found_goal_state == True:
            break     
    
    #Append fail status if goal can't be reached
    if found_goal_state == None:
        pegSolitaireObject.trace.append("GOAL NOT FOUND")
    return True


#Function for Depth Limited Search
def depthLimitedSearch(pegSolitaireObject, maxDepth):
    #Check if the current state is goal state or not
    if pegSolitaireUtils.isGoalState(pegSolitaireObject.gameState):
        return True
    
    #If current state is already explored, it will not explore it furthur and return
    if pegSolitaireUtils.isAlreadyExplored(pegSolitaireObject.gameState): 
        return
    
    #if depth reached is zero, goal can't be find with these moves and it backtracks
    if maxDepth == 0:
        return
    
    #Check for all pegs in the peg board in all direction for next game state
    for i in xrange(7):
        for j in xrange(7):
            if pegSolitaireObject.gameState[i][j] == 1: 
                for direction in all_directions:
                    #check valid move
                    if pegSolitaireObject.is_validMove((i,j),direction):
                        #Save game state in another state variable, so that we can backtrack if our next move eventually fails
                        parentObject = pegSolitaireUtils.game("game.txt")
                        parentObject.gameState = pegSolitaireUtils.copyGameState(pegSolitaireObject)
                        #Get next valid move state
                        pegSolitaireObject.getNextState((i,j),direction)
    
                        #Recursively call function with next valid move and depth-1
                        result = depthLimitedSearch(pegSolitaireObject, maxDepth-1)
                        
                        #If the above exploration fails it will return to its initial game state (backtrack)
                        if result == None:
                            pegSolitaireUtils.restoreInitialState(pegSolitaireObject,parentObject.gameState)
                        #If Goal state is reached, it computes the trace and return true
                        if result == True:
                            #Get next move position for computing trace
                            newpos = pegSolitaireObject.getNextPosition((i,j), direction)
                            pegSolitaireObject.trace.insert(0,newpos)
                            pegSolitaireObject.trace.insert(0,(i,j))
                            return True

    return


#Function for A* Search with heuristics 1
def aStarOne(pegSolitaireObject):
    #################################################
        # Must use functions:
        # getNextState(self,oldPos, direction)
        # 
        # we are using this function to count,
        # number of nodes expanded, If you'll not
        # use this grading will automatically turned to 0
        #################################################
        #
        # using other utility functions from pegSolitaireUtility.py
        # is not necessary but they can reduce your work if you 
        # use them.
        # In this function you'll start from initial gameState
        # and will keep searching and expanding tree until you 
	# reach goal using A-Star searching with first Heuristic
	# you used.
        # you must save the trace of the execution in pegSolitaireObject.trace
        # SEE example in the PDF to see what to return
        #
        #################################################
    
    
    intialStartingState = pegSolitaireUtils.copyGameState(pegSolitaireObject)
    #This Queue would keep elements in increasing order of priority. This priority is decided by heuristic value.
    heapQueue = Queue.PriorityQueue()
    #Keep a hash of all explored states to prevent exploration of repeated states.
    pegSolitaireUtils.executedStates = set()
    #ParentStates would include a dictionary to map children nodes to its parent node along with the direction it arrived from.
    #This would help us to compute trace.
    parentStates = {}

    #Insert the first element in the Priority Queue and run a loop until either
    #1. Goal is reached.
    #2. All states are explored.
    heapQueue.put((0,pegSolitaireObject.gameState))
    parentStates[pegSolitaireUtils.stateToString(pegSolitaireObject.gameState)] = (None,None)

    while not heapQueue.empty():
        currentNodeState = (heapQueue.get())[1]
        #If current state is already explored, get the next state from the Queue.
        if pegSolitaireUtils.isAlreadyExplored(currentNodeState): 
            if heapQueue.empty():
                return False;
            currentNodeState = (heapQueue.get())[1]
        
        #If the current state is goal state, compute the trace and return True.
        if pegSolitaireUtils.isGoalState(currentNodeState):
            pegSolitaireUtils.computeTrace(parentStates,pegSolitaireUtils.stateToString(currentNodeState),pegSolitaireObject)
            return True

        #Back up of the parent node.
        initialState = copy.deepcopy(currentNodeState)
        pegSolitaireObject.gameState = currentNodeState
        #Get list of valid moves from the current game state.
        nextValidMoves = pegSolitaireUtils.setValidMoves(pegSolitaireObject)

        for nextMove in nextValidMoves:
            #Get next state of the game based on the position of current node and direction.
            pegSolitaireObject.getNextState((nextMove[0],nextMove[1]),nextMove[2])
            #Set parent for the current state.
            parentStates[pegSolitaireUtils.stateToString(pegSolitaireObject.gameState)] = (pegSolitaireUtils.stateToString(initialState),nextMove)
            #Put the node and the its f(n) value in the queue [f(n) = g(n) + h(n)]
            heapQueue.put((pegSolitaireUtils.funcFforAStarOne(intialStartingState,pegSolitaireObject),pegSolitaireUtils.copyGameState(pegSolitaireObject)))
            #Restore original state for next iteration.
            pegSolitaireUtils.restoreInitialState(pegSolitaireObject,initialState)
          
             
    pegSolitaireObject.trace.append("GOAL NOT FOUND")        

    return False

#Function for A* Search with heuristics 2
def aStarTwo(pegSolitaireObject):
	#################################################
        # Must use functions:
        # getNextState(self,oldPos, direction)
        # 
        # we are using this function to count,
        # number of nodes expanded, If you'll not
        # use this grading will automatically turned to 0
        #################################################
        #
        # using other utility functions from pegSolitaireUtility.py
        # is not necessary but they can reduce your work if you 
        # use them.
        # In this function you'll start from initial gameState
        # and will keep searching and expanding tree until you 
        # reach goal using A-Star searching with second Heuristic
        # you used.
        # you must save the trace of the execution in pegSolitaireObject.trace
        # SEE example in the PDF to see what to return
        #
        #################################################
        
    intialStartingState = pegSolitaireUtils.copyGameState(pegSolitaireObject)    
    #This Queue would keep elements in increasing order of priority. This priority is decided by heuristic value.
    heapQueue = Queue.PriorityQueue()
    #Keep a hash of all explored states to prevent exploration of repeated states.
    pegSolitaireUtils.executedStates = set()
    #ParentStates would include a dictionary to map children nodes to its parent node along with the direction it arrived from.
    #This would help us to compute trace.
    parentStates = {}

    #Insert the first element in the Priority Queue and run a loop until either
    #1. Goal is reached.
    #2. All states are explored.
    heapQueue.put((0,pegSolitaireObject.gameState))
    parentStates[pegSolitaireUtils.stateToString(pegSolitaireObject.gameState)] = (None,None)

    while not heapQueue.empty():
        currentNodeState = (heapQueue.get())[1]
        #If current state is already explored, get the next state from the Queue.
        if pegSolitaireUtils.isAlreadyExplored(currentNodeState):
            if heapQueue.empty():
                return False;
            currentNodeState = (heapQueue.get())[1]
        
        #If the current state is goal state, compute the trace and return True.
        if pegSolitaireUtils.isGoalState(currentNodeState):
            pegSolitaireUtils.computeTrace(parentStates,pegSolitaireUtils.stateToString(currentNodeState),pegSolitaireObject)
            return True

        #Back up of the parent node.
        initialState = copy.deepcopy(currentNodeState)
        pegSolitaireObject.gameState = currentNodeState
        #Get list of valid moves from the current game state.
        nextValidMoves = pegSolitaireUtils.setValidMoves(pegSolitaireObject)

        for nextMove in nextValidMoves:
            #Get next state of the game based on the position of current node and direction.
            pegSolitaireObject.getNextState((nextMove[0],nextMove[1]),nextMove[2])
            #Set parent for the current state.
            parentStates[pegSolitaireUtils.stateToString(pegSolitaireObject.gameState)] = (pegSolitaireUtils.stateToString(initialState),nextMove)
            #Put the node and the its f(n) value in the queue [f(n) = g(n) + h(n)]
            heapQueue.put((pegSolitaireUtils.heuristic2(pegSolitaireObject),pegSolitaireUtils.copyGameState(pegSolitaireObject)))
            #Restore original state for next iteration.
            pegSolitaireUtils.restoreInitialState(pegSolitaireObject,initialState)
            
    pegSolitaireObject.trace.append("GOAL NOT FOUND")        

    return False