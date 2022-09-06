import numpy as np
import abc
import util
from game import Agent, Action
import math

MAX_AGENT = 0
MIN_AGENT = 1
INFINITY = float('inf')
MIN_INFINITY = float('-inf')


def _get_best_value(list_tups, player):
    """ returns the tuple with the best score depending on the player type
        @param list_tups a list of tuples [(score, action), (score, action), ...]
        @param player current player
        @return the tuple with the best value according to the given player """
    if player == MAX_AGENT:
        best = list_tups[0]
        for tup in list_tups:
            if tup[0] > best[0]:
                best = tup
        return best
    else:
        best = list_tups[0]
        for tup in list_tups:
            if tup[0] < best[0]:
                best = tup
        return best


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in
                  legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if
                        scores[index] == best_score]
        chosen_index = np.random.choice(
            best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(
            action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score

        h, w = np.shape(board)
        top_left_score = (board[0, 0] + (board[0, 1] + board[1, 0]) / 2 +
                          (board[1, 1] / 4)) ** 2
        bottom_left_score = (board[h - 1, 0] + (
                    board[h - 2, 0] + board[h - 1, 1]) / 2
                             + (board[h - 2, 1] / 4)) ** 2
        top_right_score = (board[0, w - 1] + (
                    board[0, w - 2] + board[1, w - 1]) / 2
                           + (board[1, w - 2] / 4)) ** 2
        bottom_right_score = (board[h - 1, w - 1] +
                              (board[h - 1, w - 2] + board[h - 2, w - 1]) / 2 +
                              (board[h - 2, w - 2] / 4)) ** 2
        empty_cells = np.count_nonzero(board == 0)
        return max(top_left_score, bottom_left_score, top_right_score,
                   bottom_right_score) + max_tile + empty_cells * 64


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        minimax_move, value = self.max_value(game_state, self.depth * 2)
        return minimax_move

    def max_value(self, game_state, depth):
        if depth == 0 or game_state.done:
            return Action.STOP, self.evaluation_function(game_state)
        max_value = np.NINF
        minimax_move = Action.STOP
        for move in game_state.get_legal_actions(MAX_AGENT):
            next_state = game_state.generate_successor(MAX_AGENT, move)
            new_move, value = self.min_value(next_state, depth - 1)
            if value > max_value:
                minimax_move = move
                max_value = value
        return minimax_move, max_value

    def min_value(self, game_state, depth):
        if depth == 0 or game_state.done:
            return Action.STOP, self.evaluation_function(game_state)
        min_value = np.PINF
        minimax_move = Action.STOP
        for move in game_state.get_legal_actions(MIN_AGENT):
            next_state = game_state.generate_successor(MIN_AGENT, move)
            new_move, value = self.max_value(next_state, depth - 1)
            if value < min_value:
                minimax_move = move
                min_value = value
        return minimax_move, min_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action, value = self.max_value(game_state, 2 * self.depth,
                                       np.NINF, np.PINF)
        return action

    def max_value(self, game_state, depth, alpha, beta):
        if depth == 0 or game_state.done:
            return Action.STOP, self.evaluation_function(game_state)
        max_value = np.NINF
        minimax_move = Action.STOP
        for move in game_state.get_legal_actions(MAX_AGENT):
            next_state = game_state.generate_successor(MAX_AGENT, move)
            new_move, value = self.min_value(next_state, depth - 1, alpha,
                                             beta)
            if value > max_value:
                minimax_move = move
                max_value = value
            if value >= beta:
                return minimax_move, max_value
            if value > alpha:
                alpha = value
        return minimax_move, max_value

    def min_value(self, game_state, depth, alpha, beta):
        if depth == 0 or game_state.done:
            return Action.STOP, self.evaluation_function(game_state)
        min_value = np.PINF
        minimax_move = Action.STOP
        for move in game_state.get_legal_actions(MIN_AGENT):
            next_state = game_state.generate_successor(MIN_AGENT, move)
            new_move, value = self.max_value(next_state, depth - 1, alpha,
                                             beta)
            if value < min_value:
                minimax_move = move
                min_value = value
            if value <= alpha:
                return minimax_move, min_value
            if value < beta:
                beta = value
        return minimax_move, min_value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        minimax_move, value = self.max_value(game_state, 2 * self.depth)
        return minimax_move

    def max_value(self, game_state, depth):
        if depth == 0 or game_state.done:
            returned_val = self.evaluation_function(game_state)
            return Action.STOP, returned_val
        max_value = np.NINF
        minimax_move = Action.STOP
        for move in game_state.get_legal_actions(0):
            next_state = game_state.generate_successor(0, move)
            new_move, value = self.expect_value(next_state, depth - 1)
            if value > max_value:
                minimax_move = move
                max_value = value
        return minimax_move, max_value

    def expect_value(self, game_state, depth):
        if depth == 0 or game_state.done:
            return Action.STOP, self.evaluation_function(game_state)
        exp_val = 0
        minimax_move = Action.STOP
        for move in game_state.get_legal_actions(1):
            next_state = game_state.generate_successor(1, move)
            new_move, value = self.max_value(next_state, depth - 1)
            exp_val += value
        exp_val = exp_val / len(game_state.get_legal_actions(1))
        # diff_from_exp = np.NINF
        # for move in game_state.get_legal_actions(1):
        #     next_state = game_state.generate_successor(1, move)
        #     new_move, value = self.max_value(next_state, depth - 1)
        #     new_diff = np.abs(exp_val - value)
        #     if new_diff < diff_from_exp:
        #         minimax_move = new_move
        #         diff_from_exp = new_diff
        return minimax_move, exp_val


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    Our better evaluation function consists of 4 values:
    1. the value of the first row
    2. the value of the monotonicity of the board
    3. the amount of empty tiles
    4. the max tile on the board
    the numbers in the returned value were chosen such that each of the 4 values
    states above will have an affect on the value of the heuristic.
    """
    board = current_game_state.board
    max_tile = current_game_state.max_tile
    empty_cells = np.count_nonzero(board == 0)
    h, w = np.shape(board)
    first_row_val_right = board[0][w - 1] * 8 + board[0][w - 2] * 4 + board[0][w - 3] * 2 + board[0][w - 4]
    first_row_val_left = board[0][0] * 8 + board[0][1] * 4 + board[0][2] * 2 + board[0][3]
    if first_row_val_right > first_row_val_left:
        first_row_val = first_row_val_right
        diff = np.sum(np.diff(board))
    else:
        first_row_val = first_row_val_left
        diff = np.sum(np.negative(np.diff(board)))
    return first_row_val * 16 + diff * -16 + max_tile * 8 + empty_cells * 256
    # return -np.sum(np.diff(current_game_state.board))

    



# Abbreviation
better = better_evaluation_function
