import math

from board import Board
from search import SearchProblem, ucs
import util
import numpy as np


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in
                state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        top_left = state.state[0][0]
        top_right = state.state[0][self.board.board_w - 1]
        down_left = state.state[self.board.board_h - 1][0]
        down_right = state.state[self.board.board_h - 1][
            self.board.board_w - 1]
        return top_left != -1 and top_right != -1 and down_left != -1 and down_right != -1

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must
        be composed of legal moves
        """
        # util.raiseNotDefined()
        total_cost = 0
        for move in actions:
            total_cost += move.piece.get_num_tiles()
        return total_cost


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    "*** YOUR CODE HERE ***"
    top_left = (0, 0)
    top_right = (0, state.board_w - 1)
    bottom_right = (state.board_h - 1, state.board_w - 1)
    bottom_left = (state.board_h - 1, 0)
    corners = {0: top_left, 1: top_right, 2: bottom_right, 3: bottom_left}
    available_corners = dict()
    for corner_key, corner_val in corners.items():
        if state.get_position(corner_val[1], corner_val[0]) == -1:
            available_corners[corner_key] = corner_val
    worst_heuristic_value = state.board_h * state.board_w
    for corner_index in available_corners.keys():
        if not check_option_to_cover_corners(state, corner_index):
            return worst_heuristic_value
    available_tiles = get_available_tiles(state)
    if not available_tiles:
        return worst_heuristic_value
    minimum_tiles = set()
    min_distances_sum = 0
    for corner in available_corners.values():
        min_tile, min_distance = min_tile_and_distance_to_corner(
            corner, available_tiles)
        min_distances_sum += min_distance
        minimum_tiles.add(min_tile)
    heuristic_value = min_distances_sum + len(minimum_tiles)
    return heuristic_value


def check_option_to_cover_corners(state, corner_to_check):
    """
        Check if any of the tiles adjacent to the corners are occupied and
        returns False if they are
        Each number represents a different corner
        0 - top left corner
        1 - top right corner
        2 - bottom right corner
        3 - bottom left corner
    """
    if corner_to_check == 0:
        if state.get_position(1, 0) != -1 or state.get_position(0, 1) != -1:
            return False
    elif corner_to_check == 1:
        if state.get_position(state.board_w - 2, 0) != -1 or \
                state.get_position(state.board_w - 1, 1) != -1:
            return False
    elif corner_to_check == 2:
        if state.get_position(state.board_w - 1, state.board_h - 2) != -1 or \
                state.get_position(state.board_w - 2, state.board_h - 1) != -1:
            return False
    else:
        if state.get_position(0, state.board_h - 2) != -1 or \
                state.get_position(1, state.board_h - 1) != -1:
            return False
    return True


def get_available_tiles(state):
    """
    The following function returns the available tiles which pieces can be
    placed at
    """
    available_tiles = list()
    for row in range(state.board_h):
        for col in range(state.board_w):
            if state.check_tile_legal(0, col, row) and \
                    state.check_tile_attached(0, col, row):
                available_tiles.append((row, col))
    return available_tiles


def calculate_chebyshev_distance(coordinate1, coordinate2):
    """
    The following function calculates the Chebyshev distance between 2 given
    coordinates
    """
    return max(np.abs(coordinate1[0] - coordinate2[0]),
               np.abs(coordinate1[1] - coordinate2[1]))


def min_tile_and_distance_to_corner(corner, tiles_list):
    """
    The following function finds the tile with the minimal distance from the
    given corner and returns the tile as well as the distance calculated
    """
    min_distance, min_tile = None, None
    for tile in tiles_list:
        tile_distance = calculate_chebyshev_distance(corner, tile)
        if min_tile is None or min_distance > tile_distance:
            min_tile = tile
            min_distance = tile_distance
    return min_tile, min_distance


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        for target in self.targets:
            if state.state[target[0]][target[1]] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves
        """
        total_cost = 0
        for move in actions:
            total_cost += move.piece.get_num_tiles()
        return total_cost


def blokus_cover_heuristic(state, problem):
    """
    The main heuristic used is the amount of available targets left to cover.
    """
    available_targets = list()
    for target in problem.targets:
        if state.get_position(target[1], target[0]) == -1:
            available_targets.append(target)
    worst_heuristic_value = state.board_h * state.board_w
    for available_target in available_targets:
        if not check_target_reachable(state, available_target):
            return worst_heuristic_value
    return len(available_targets)


def check_target_reachable(state, target):
    """
    The following function checks whether the target is reachable in the given
    state. Returns True in case it is and False otherwise.
    """
    target_row = target[0]
    target_col = target[1]
    if target_row - 1 >= 0 and state.state[target_row - 1][target_col] != -1:
        return False
    if target_row + 1 < state.board_h and \
            state.state[target_row + 1][target_col] != -1:
        return False
    if target_col - 1 >= 0 and state.state[target_row][target_col - 1] != -1:
        return False
    if target_col + 1 < state.board_w and \
            state.state[target_row][target_col + 1] != -1:
        return False
    return True


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point

    def change_state(self, board):
        self.board = board

    def changes_targets(self, targets):
        self.targets = targets.copy()

    def change_starting_point(self, starting_point):
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        for target in self.targets:
            if state.state[target[0]][target[1]] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        total_cost = 0
        for move in actions:
            total_cost += move.piece.get_num_tiles()
        return total_cost

    def solve(self):
        """
        This method should return a sequence of actions that covers all target
        locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time.
        Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closest uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        current_state = self.board.__copy__()
        backtrace = []
        points_dict = dict()
        for target in self.targets:
            points_dict[target] = util.manhattanDistance(target,
                                                         self.starting_point)
        sorted_dict = sorted(points_dict.items(), key=lambda x: x[1])
        starting_point = self.starting_point
        target_problem = ClosestLocationSearch(current_state.board_w,
                                               current_state.board_h,
                                               current_state.piece_list,
                                               starting_point,[(0,0)])
        for target in sorted_dict:
            target_problem.change_state(current_state)
            target_problem.changes_targets([target[0]])
            path = ucs(target_problem)
            backtrace += path
            target_problem.change_starting_point(target[0])
            for action in path:
                current_state = current_state.do_move(0, action)
            self.expanded = target_problem.expanded
        return backtrace


class MiniContestSearch:
    """
    Implement your contest entry here
    """
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
