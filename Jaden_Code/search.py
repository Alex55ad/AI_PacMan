"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  """
  
  print("Start:", problem.getStartState())
  print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
  print("Start's successors:", problem.getSuccessors(problem.getStartState()))  
  
  queue = util.Stack()
  visitedNodes = []
  start = problem.getStartState()
  firstNode = (start,[])

  queue.push(firstNode)

  while not queue.isEmpty():
    state,actions = queue.pop()
    if state not in visitedNodes:
      visitedNodes.append(state)
      if problem.isGoalState(state):
        return actions
      else:
        successors = problem.getSuccessors(state)
        for state,action,cost in successors:
          newAction = actions + [action]
          newNode = (state,newAction)
          queue.push(newNode)
  return []

import copy
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    open_ds = util.Queue()

    start = [problem.getStartState(), ""]
    open_ds.push([start])

    visited_state = [start[0]]

    while not open_ds.isEmpty():
        node = open_ds.pop()
        end = node[-1]

        if problem.isGoalState(end[0]):
            return [state[1] for state in node[1:]]

        successors = problem.getSuccessors(end[0])
        for succ in successors:
            if succ[0] not in visited_state:
                visited_state.append(succ[0])
                new_node = copy.deepcopy(node)
                new_node.append(succ)
                open_ds.push(new_node)

    return []
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
   
    open_ds = util.PriorityQueue()

    start_state = problem.getStartState()
    start = (start_state, "", (0, heuristic(start_state, problem)))
    open_ds.push([start], start[2])

    visited_state = {start_state[0]: sum(start[2])}

    while not open_ds.isEmpty():
        node = open_ds.pop()

        if not open_ds.isEmpty():
            next_node = open_ds.pop()
            temp = [node, next_node]

            while not open_ds.isEmpty() and sum(node[-1][2]) == sum(next_node[-1][2]):
                next_node = open_ds.pop()
                temp.append(next_node)
            
            tie_nodes = temp if sum(node[-1][2]) == sum(next_node[-1][2]) else temp[:-1]

            for n in tie_nodes:
                if node[-1][2][0] < n[-1][2][0]:
                    node = n

            for n in temp:
                if node != n:
                    open_ds.push(n, sum(n[-1][2]))

        end = node[-1]
        if end[0] not in visited_state or sum(end[2]) <= visited_state[end[0]]:
            if problem.isGoalState(end[0]):
                return [state[1] for state in node[1:]]

            successors = problem.getSuccessors(end[0])
            for succ in successors:
                gn_succ = end[2][0] + succ[2]
                hn_succ = heuristic(succ[0], problem)
                fn_succ = gn_succ + hn_succ
                if succ[0] not in visited_state or fn_succ < visited_state[succ[0]]:
                    visited_state[succ[0]] = fn_succ
                    new_node = copy.deepcopy(node)
                    new_succ = (succ[0], succ[1], (gn_succ, hn_succ))
                    new_node.append(new_succ)
                    open_ds.push(new_node, fn_succ)
    return []
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch