
import sys
import copy
import math
"""
DON'T FORGET TO ATTRIBUTE CODE
"""

NUM_PIECES = 4
MAX_DIST = 7
MAX_DEPTH = 4
BOARDDIM = 3
NUM_PLAYERS = 3
_TEMPLATE_DEBUG = """heurisitic: {0}

board:       ,-' `-._,-' `-._,-' `-._,-' `-.
            | {16:} | {23:} | {29:} | {34:} |
            |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
         ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
        | {10:} | {17:} | {24:} | {30:} | {35:} |
        | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
     ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
    | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
 ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
| {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
| -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
 `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
    | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
    | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
     `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
        | {03:} | {08:} | {14:} | {21:} | {28:} |
        | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
         `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
            | {04:} | {09:} | {15:} | {22:} |   | input |
            | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
             `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""


_DISPLAY = {  # something 5 characters wide for each colour:
    'red': " RED ",
    'green': "GREEN",
    'blue': " BLUE",
    ' ': "     "
}

_FINISHING_HEXES = {
    'red': {(3, -3), (3, -2), (3, -1), (3, 0)},
    'green': {(-3, 3), (-2, 3), (-1, 3), (0, 3)},
    'blue': {(-3, 0), (-2, -1), (-1, -2), (0, -3)},
}
_ADJACENT_STEPS = [(-1, +0), (+0, -1), (+1, -1), (+1, +0), (+0, +1), (-1, +1)]

RAN = range(-BOARDDIM, BOARDDIM + 1)
HEXES = [(q, r) for q in RAN for r in RAN if -q - r in RAN]
COLOURS = ['red', 'green', 'blue']
COLOUR_DICT = {'red': 0, 'green': 1, 'blue': 2}

# _TEMPLATE_DEBUG.format(self.value, *cells)

def maxn(game_tree, colour):
    return recur_maxn(game_tree.root, COLOUR_DICT[colour], 0)[1]

def recur_maxn(game_node, colour_index, depth):
    if depth == MAX_DEPTH:
        return game_node.boardstate.eval_scores(), game_node.boardstate.action
    else:
        max_eval = - NUM_PIECES * MAX_DIST - 1
        best_score_dict = {}
        best_action = None
        for child in game_node.children:
            eval_score_dict = recur_maxn(child, colour_index, depth+1)[0]
            eval_score = eval(eval_score_dict, COLOURS[(colour_index + depth) % NUM_PLAYERS])
            if eval_score > max_eval:
#            if ((eval_score > max_eval) or
#                    (eval_score == max_eval and (best_action and best_action[0] != "JUMP" and child.boardstate.action == "JUMP"))):
                max_eval = eval_score
                best_score_dict = eval_score_dict
                best_action = child.boardstate.action
        return best_score_dict, best_action


def eval(eval_score_dict, curr_colour):
    min_opposition = NUM_PIECES * MAX_DIST
    for colour in COLOURS:
        if colour != curr_colour and eval_score_dict[colour] < min_opposition:
            min_opposition = eval_score_dict[colour]
    return min_opposition - eval_score_dict[curr_colour]
#    return - eval_score_dict[curr_colour]

class GameNode:
    def __init__(self, board_state):
        self.boardstate = board_state      # the board state
        # the three tuple of distance from end
        self.value = {'red': 0, 'green': 0, 'blue': 0}
#        self.parent = parent  # a node reference
        self.children = []    # a list of nodes

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self, level=0):
        cells = []
        for qr in HEXES:
            cells.append(_DISPLAY[self.boardstate.board[qr]])
        ret = "\t" * level + _TEMPLATE_DEBUG.format(self.value, *cells) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'


class GameTree:
    def __init__(self, my_colour):
        self.root = None
        self.colourindex = COLOUR_DICT[my_colour]

    def build_tree(self, board):
        """
        :param data_list: Take data in list format
        :return: Parse a tree from it
        """
        self.root = GameNode(BoardState(board))
        self.parse_subtree(self.root, 0)

    def parse_subtree(self, curr_node, depth):
        # base case
        if depth == MAX_DEPTH:
            curr_node.value = curr_node.boardstate.eval_scores()
            return
        else:
            next_board_states = self.create(curr_node.boardstate, COLOURS[(self.colourindex + depth) % NUM_PLAYERS])
            depth += 1
            for next_board_state in next_board_states:
                child = GameNode(next_board_state)
                # print(str(tree_node))
                curr_node.add_child(child)
                self.parse_subtree(child, depth)

    def create(self, board_state, colour):
        all_board_states = []
        for qr in HEXES:
            if board_state.board[qr] == colour:
                if qr in _FINISHING_HEXES[colour]:
                    action = ("EXIT", qr)
                    all_board_states.append(self.change(board_state, action, colour))
                q, r = qr
                for dq, dr in _ADJACENT_STEPS:
                    for i, atype in [(1, "MOVE"), (2, "JUMP")]:
                        tqr = q + dq * i, r + dr * i
                        if tqr in HEXES:
                            if board_state.board[tqr] == ' ':
                                action = (atype, (qr, tqr))
                                all_board_states.append(
                                    self.change(board_state, action, colour))
                                break
        if not all_board_states:
            action = ("PASS", None)
            all_board_states.append(self.change(board_state, action, colour))
        # print(all_boards)
        return all_board_states

    def change(self, board_state, action, colour):
        new_board = copy.copy(board_state.board)
        new_exited = copy.copy(board_state.exited)
        atype, aargs = action
        if atype == "MOVE":
            qr_a, qr_b = aargs
            new_board[qr_a] = ' '
            new_board[qr_b] = colour
        elif atype == "JUMP":
            qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
            qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
            new_board[qr_a] = ' '
            new_board[qr_b] = colour
            new_board[qr_c] = colour
        elif atype == "EXIT":
            qr = aargs
            new_board[qr] = ' '
            new_exited[colour] += 1
        else:  # atype == "PASS":
            pass

        return BoardState(new_board, action, new_exited)


class BoardState:
    def __init__(self, board, action=None, exited={'red': 0, 'green': 0, 'blue': 0}):
        self.board = board
        self.action = action
        self.exited = exited

    def piece_lists(self):
        piecelists = {'red': set(), 'green': set(), 'blue': set()}
        for qr in HEXES:
            if self.board[qr] != ' ':
                piecelists[self.board[qr]].add(qr)
        return piecelists

    def eval_scores(self):
        """
        Since four pieces must exit, we sum the individual distances of
        the best four pieces from exiting, with a distance of zero if a piece
        has already exited. If there are not enough remaining pieces on the
        board, add on 7 (the max distance possible)
        """
        eval_score = {'red': 0, 'green': 0, 'blue': 0}
        for colour in eval_score:
            exit_dists = []
            for qr in self.piece_lists()[colour]:
                exit_dists.append((exit_dist(qr, colour)))
            for i in range(NUM_PIECES - self.exited[colour] - len(exit_dists)):
                exit_dists.append(MAX_DIST)
            eval_score[colour] = sum(sorted(exit_dists)[:(NUM_PIECES - self.exited[colour])])
        return eval_score


def exit_dist(qr, colour):
    """how many HEXES away from a coordinate is the nearest exiting hex?"""
    q, r = qr
    if colour == 'red':
        return BOARDDIM - q
    if colour == 'green':
        return BOARDDIM - r
    if colour == 'blue':
        return BOARDDIM - (-q - r)

if __name__ == "__main__":
    main()
