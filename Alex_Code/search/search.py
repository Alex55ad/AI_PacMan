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
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""
    solution = []
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    startingPos = problem.getStartState()
    if(problem.isGoalState(startingPos)):
        print "Solution: ", solution
        return solution
    stack = util.Stack()
    visited = []
    stack.push((startingPos, []))
    while not stack.isEmpty():
        currentx, actions = stack.pop()
        solution = actions
        if isinstance(currentx[0], int):
            current = currentx
        if (not (current in visited)):
            visited.append(current)
            if(problem.isGoalState(currentx)):
                print "Solution: ", solution
                return solution
            successors = problem.getSuccessors(currentx)
            for nextState, action, _ in successors:
                stack.push((nextState, actions + [action]))
    print "Solution: ", solution
    return solution       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    solution = []
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    startingPos = problem.getStartState()
    if problem.isGoalState(startingPos):
        print "Solution: ", solution
        return solution
    queue = util.Queue() 
    visited = set()
    queue.push((startingPos, []))
    while not queue.isEmpty():
        currentx, actions = queue.pop()
        solution = actions
        if isinstance(currentx[0], int):
            current = currentx
        else: current = currentx[0]
        if current not in visited:
            visited.add(current)
            if problem.isGoalState(currentx):
                print "Solution: ", solution
                return solution
            successors = problem.getSuccessors(currentx)
            print "Succsessors: ", successors
            for nextState, action, _ in successors:
                queue.push((nextState, actions + [action])) 
    print "Solution: ", solution
    return solution
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    startingPos = problem.getStartState()
    solution = []
    if problem.isGoalState(startingPos):
        print "Solution: ", solution
        return solution
    queue = util.PriorityQueue()
    visited = set()
    queue.push((startingPos, [], 0), 0) 
    while not queue.isEmpty():
        current,actions, cost = queue.pop
        if current not in visited:
            visited.add(current)
        if problem.isGoalState(current):
            print "solution: ", solution
            return solution
        successors = problem.getSuccessors(current)
        for nextState, action, step_cost in successors:
            step_cost = cost + step_cost
            queue.push((nextState, actions + [action], step_cost), step_cost)
    print "Solution: ", solution
    return solution
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    start_node = (start_state, [], 0, heuristic(start_state, problem))

    priority_queue = util.PriorityQueue()
    visited = set()
    solution = []
    priority_queue.push(start_node, start_node[2] + start_node[3])

    while not priority_queue.isEmpty():
        current_state, actions, cost, _ = priority_queue.pop()
        solution = actions
        if isinstance(current_state, int):
            current = current_state
            visited_corners = set()  # Initialize visited_corners as an empty set
        else:
            current, visited_corners = current_state

        if problem.isGoalState(current_state):
            return solution

        if current not in visited:
            visited.add(current)

            successors = problem.getSuccessors(current_state)
            for next_state, action, step_cost in successors:
                if isinstance(current_state, int):
                    next_state = (next_state, visited_corners)  # Convert to the (x, y, visited_corners) format
                new_actions = actions + [action]
                new_cost = cost + step_cost
                priority = new_cost + heuristic(next_state, problem)
                priority_queue.push((next_state, new_actions, new_cost, priority), priority)

    return solution
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch