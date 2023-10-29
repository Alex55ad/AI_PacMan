# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import copy
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

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
    """Search the node of least total cost first."""
    open_ds = util.PriorityQueue()

    start = [problem.getStartState(),""]
    open_ds.push([start], 0)
    visited_state = []

    while not open_ds.isEmpty():
        node = open_ds.pop()
        end = node[-1]

        if problem.isGoalState(end[0]):
            return [state[1] for state in node[1:]]

        if end[0] not in visited_state:
            visited_state.append(end[0])
            successors = problem.getSuccessors(end[0])
            for succ in successors:
                new_node = node + [succ]
                total_cost = problem.getCostOfActions([state[1] for state in new_node[1:]])
                open_ds.push(new_node, total_cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    current = problem.getStartState()
    priority_queue = util.PriorityQueue()
    visited = []
    solution = []

    if problem.isGoalState(current):
        print "Solution: ", solution
        return solution
    
    while not problem.isGoalState(current):
        if current not in visited:
            visited.append(current)
            successors = problem.getSuccessors(current)

            for nextState, action, step_cost in successors:
                temp = solution + [action]
                que_pos = problem.getCostOfActions(temp) + heuristic(nextState,problem)
                priority_queue.push((temp,nextState),que_pos)
        aux = priority_queue.pop()
        solution = aux[0]
        current = aux[1]

    return solution
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
