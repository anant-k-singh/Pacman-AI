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

def genericSearch(problem, ds, heuristic=None):
    visited = []        # List of already visisted nodes
    action_list = []    # List of actions taken to get to the current node
    initial = problem.getStartState()   # Starting state of the problem

    if isinstance(ds, util.Stack) or isinstance(ds, util.Queue):
        ds.push((initial, action_list))
    elif isinstance(ds, util.PriorityQueue):
        ds.push((initial, action_list), heuristic(initial, problem))

    # While there are still elements on the ds, expand the value of each 
    # node for the node to explore, actions to get there, and the cost. If the
    # node isn't visited already, check to see if node is the goal. If no, then
    # add all of the node's successors onto the ds (with relevant 
    # information about path and cost associated with that node)
    while ds: 
        if isinstance(ds, util.Stack) or isinstance(ds, util.Queue):
            node, actions = ds.pop() 
        elif isinstance(ds, util.PriorityQueue):
            node, actions = ds.pop()
        
        if not node in visited:
            visited.append(node)
            if problem.isGoalState(node):
                return actions
            successors = problem.getSuccessors(node)
            for successor in successors:
                coordinate, direction, cost = successor
                newActions = actions + [direction]
                if isinstance(ds, util.Stack) or isinstance(ds, util.Queue):
                    ds.push((coordinate, newActions))
                elif isinstance(ds, util.PriorityQueue):
                    newCost = problem.getCostOfActions(newActions) + \
                               heuristic(coordinate, problem)
                    ds.push((coordinate, newActions), newCost)                  

    return []
    
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # Use the genericSearch method, with the ds maintained using a Stack
    # so that the search proceeds in the order of exploring from the node last
    # discovered
    return genericSearch(problem, util.Stack())

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    # Use the genericSearch method, with the ds maintained with a Queue so 
    # that all nodes on the same level are explored before the next level is 
    # explored. This will find the optimal solution, because each level is 
    # explored before the next, so the first time the goal is reached will be
    # the shortest path to the goal.
    return genericSearch(problem, util.Queue())

def uniformCostSearch(problem):
    "Search the node of least total cost first. "

    # Running UCS is the same as running A* Search with a null heuristic, 
    # so simplify the calls by just using aStarSearch.
    return aStarSearch(problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    # Use the genericSearch method, with the ds maintained with a 
    # PriorityQueue. The cost is calculated using the provided heuristic. 
    # If no heuristic is given (such as UCS), then default to the given
    # nullHeuristic
    return genericSearch(problem, util.PriorityQueue(), heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
