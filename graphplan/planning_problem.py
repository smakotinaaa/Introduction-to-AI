from util import Pair
import copy
from proposition_layer import PropositionLayer
from plan_graph_level import PlanGraphLevel
from pgparser import PgParser
from action import Action

try:
    from search import SearchProblem
    from search import a_star_search

except:
    try:
        from CPF.search import SearchProblem
        from CPF.search import a_star_search
    except:
        from CPF.search_win_34 import SearchProblem
        from CPF.search_win_34 import a_star_search


class PlanningProblem:
    def __init__(self, domain_file, problem_file):
        """
        Constructor
        """
        p = PgParser(domain_file, problem_file)
        self.actions, self.propositions = p.parse_actions_and_propositions()
        # list of all the actions and list of all the propositions

        initial_state, goal = p.parse_problem()
        # the initial state and the goal state are lists of propositions

        self.initialState = frozenset(initial_state)
        self.goal = frozenset(goal)

        self.create_noops()
        # creates noOps that are used to propagate existing propositions from one layer to the next

        PlanGraphLevel.set_actions(self.actions)
        PlanGraphLevel.set_props(self.propositions)
        self.expanded = 0

    def get_start_state(self):
        return self.initialState

    def is_goal_state(self, state):
        """
        Hint: you might want to take a look at goal_state_not_in_prop_payer function
        """
        return not self.goal_state_not_in_prop_layer(list(state))

    def get_successors(self, state):
        """
        For a given state, this should return a list of triples,
        (successor, action, step_cost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'step_cost' is the incremental
        cost of expanding to that successor, 1 in our case.
        You might want to this function:
        For a list / set of propositions l and action a,
        a.all_preconds_in_list() returns true if the preconditions of a are in l

        Note that a state *must* be hashable!! Therefore, you might want to
        represent a state as a frozenset
        """
        self.expanded += 1
        successor_list = []
        for action in self.actions:
            if action.all_preconds_in_list(state) and not action.is_noop():
                new_state = set(state)
                new_state.update(action.get_add())
                new_state = new_state - set(action.get_delete())
                successor_list.append((frozenset(new_state), action, 1))
        return successor_list

    @staticmethod
    def get_cost_of_actions( actions):
        return len(actions)

    def goal_state_not_in_prop_layer(self, propositions):
        """
        Helper function that receives a  list of propositions (propositions) and returns False
        if not all the goal propositions are in that list
        """
        for goal in self.goal:
            if goal not in propositions:
                return True
        return False

    def create_noops(self):
        """
        Creates the noOps that are used to propagate propositions from one layer to the next
        """
        for prop in self.propositions:
            name = prop.name
            precon = []
            add = []
            precon.append(prop)
            add.append(prop)
            delete = []
            act = Action(name, precon, add, delete, True)
            self.actions.append(act)


def max_level(state, planning_problem):
    """
    The heuristic value is the number of layers required to expand all goal propositions.
    If the goal is not reachable from the state your heuristic should return float('inf')
    A good place to start would be:
    prop_layer_init = PropositionLayer()          #create a new proposition layer
    for prop in state:
        prop_layer_init.add_proposition(prop)        #update the proposition layer with the propositions of the state
    pg_init = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
    pg_init.set_proposition_layer(prop_layer_init)   #update the new plan graph level with the the proposition layer
    """
    prop_layer_init = PropositionLayer()
    for prop in state:
        prop_layer_init.add_proposition(prop)
    pg_init = PlanGraphLevel()
    pg_init.set_proposition_layer(prop_layer_init)
    graphs = list()
    graphs.append(pg_init)
    current_level = 0
    current_layer_props = pg_init.get_proposition_layer().get_propositions()
    while not planning_problem.is_goal_state(current_layer_props):
        pg_curr = PlanGraphLevel()
        pg_curr.expand_without_mutex(graphs[current_level])
        graphs.append(pg_curr)
        current_level += 1
        if is_fixed(graphs, current_level):
            return float('inf')
        current_layer_props = pg_curr.get_proposition_layer().get_propositions()
    return current_level


def level_sum(state, planning_problem):
    """
    The heuristic value is the sum of sub-goals level they first appeared.
    If the goal is not reachable from the state your heuristic should return float('inf')
    """
    prop_layer_init = PropositionLayer()
    for prop in state:
        prop_layer_init.add_proposition(prop)
    pg_init = PlanGraphLevel()
    pg_init.set_proposition_layer(prop_layer_init)
    graphs = list()
    graphs.append(pg_init)
    current_level = 0
    sum_of_levels = 0
    current_layer_props = pg_init.get_proposition_layer().get_propositions()
    sub_goals = set(planning_problem.goal) - current_layer_props
    while not planning_problem.is_goal_state(current_layer_props):
        pg_curr = PlanGraphLevel()
        pg_curr.expand_without_mutex(graphs[current_level])
        graphs.append(pg_curr)
        current_level += 1
        if is_fixed(graphs, current_level):
            return float('inf')
        current_layer_props = pg_curr.get_proposition_layer().get_propositions()
        for prop in current_layer_props:
            if prop in sub_goals:
                sum_of_levels += current_level
                sub_goals.remove(prop)
    return sum_of_levels


def is_fixed(graph, level):
    """
    Checks if we have reached a fixed point,
    i.e. each level we'll expand would be the same, thus no point in continuing
    """
    if level == 0:
        return False
    return len(graph[level].get_proposition_layer().get_propositions()) == len(
        graph[level - 1].get_proposition_layer().get_propositions())


def null_heuristic(*args, **kwargs):
    return 0


if __name__ == '__main__':
    import sys
    import time

    if len(sys.argv) != 1 and len(sys.argv) != 4:
        print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
        exit()
    domain = 'dwrDomain.txt'
    problem = 'dwrProblem.txt'
    heuristic = null_heuristic
    if len(sys.argv) == 4:
        domain = str(sys.argv[1])
        problem = str(sys.argv[2])
        if str(sys.argv[3]) == 'max':
            heuristic = max_level
        elif str(sys.argv[3]) == 'sum':
            heuristic = level_sum
        elif str(sys.argv[3]) == 'zero':
            heuristic = null_heuristic
        else:
            print("Usage: planning_problem.py domain_name problem_name heuristic_name[max, sum, zero]")
            exit()

    prob = PlanningProblem(domain, problem)
    start = time.time()
    plan = a_star_search(prob, heuristic)
    elapsed = time.time() - start
    if plan is not None:
        print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
    else:
        print("Could not find a plan in %.2f seconds" % elapsed)
    print("Search nodes expanded: %d" % prob.expanded)