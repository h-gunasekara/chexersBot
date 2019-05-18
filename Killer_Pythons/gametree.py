"PLEASE WORK"
"jeff"

import sys
import copy
import math
from ast import literal_eval
"""
Data should be in the following format:
['A', ['B', ('D', 3), ('E', 5)], ['C', ['F', ['I',('K',0), ('L', 7)],('J',5)], ['G', ('M',7), ('N',8)], ('H',4)]]

Note that Leaves must be **tuples**

Usage:  python tree_parser.py [filename]
    File should have data in the format shown above.
"""

_TEMPLATE_DEBUG = """hurisitic: {0}

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

ran = range(-3, +3 + 1)
hexes = {(q, r) for q in ran for r in ran if -q - r in ran}
colours = ['red', 'green', 'blue']


class GameNode:
    def __init__(self, name, parent=None):
        self.Name = name      # the board dict
        # the three tuple of distacne from end
        self.value = {'red': 0, 'green': 0, 'blue': 0}
        self.parent = parent  # a node reference
        self.children = []    # a list of nodes

    def addChild(self, childNode):
        self.children.append(childNode)

    def __str__(self, level=0):
        cells = []
        ran = range(-3, +3 + 1)
        for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
            cells.append(_DISPLAY[self.Name[qr]])
        ret = "\t" * level + _TEMPLATE_DEBUG.format(self.value, *cells) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'


class GameTree:
    def __init__(self):
        self.root = None

    def build_tree(self, board):
        """
        :param data_list: Take data in list format
        :return: Parse a tree from it
        """
        self.root = GameNode(board)
        self.parse_subtree(self.root, 0)
        print(str(self.root))

    def parse_subtree(self, parent, currcol):
        # base case
        if currcol >= 2:
            parent.value = self.h(parent.Name, currcol)
            # do hurisitic
            # need to figure out a way to go down every array
            return
        next_moves = self.create(parent.Name, colours[currcol % 3])
        for move in next_moves:
            # print(move)
            tree_node = GameNode(move)
            tree_node.parent = parent
            # print(str(tree_node))
            parent.addChild(tree_node)
            currcol += 1
            self.parse_subtree(tree_node, currcol)

    def create(self, board, col):
        available_actions = []
        all_boards = []
        for qr in hexes:
            if board[qr] == col:
                if qr in _FINISHING_HEXES[col]:
                    action = ("EXIT", qr)
                    all_boards.append(self.change(board, action, col))
                q, r = qr
                for dq, dr in _ADJACENT_STEPS:
                    for i, atype in [(1, "MOVE"), (2, "JUMP")]:
                        tqr = q + dq * i, r + dr * i
                        if tqr in hexes:
                            if board[tqr] == ' ':
                                action = (atype, (qr, tqr))
                                all_boards.append(
                                    self.change(board, action, col))
                                break
        if not available_actions:
            action = ("PASS", None)
            all_boards.append(self.change(board, action, col))
        # print(all_boards)
        return all_boards

    def change(self, board, action, col):
        new_board = copy.copy(board)
        atype, aargs = action
        if atype == "MOVE":
            qr_a, qr_b = aargs
            new_board[qr_a] = ' '
            new_board[qr_b] = col
        elif atype == "JUMP":
            qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
            qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
            new_board[qr_a] = ' '
            new_board[qr_b] = col
            new_board[qr_c] = col
        elif atype == "EXIT":
            qr = aargs
            new_board[qr] = ' '
        else:  # atype == "PASS":
            pass

        return new_board

    def exit_dist(self, qr, col):
        """how many hexes away from a coordinate is the nearest exiting hex?"""
        q, r = qr
        if col == 'red':
            return 3 - q
        if col == 'green':
            return 3 - r
        if col == 'blue':
            return 3 - (-q - r)

    def h(self, board, col):
        """
        Admissible heuristic for single-player Chexers:
        In the best case, a piece can get to the edge of the board in
        exit_dist // 2 jump actions (plus 1 move action when the distance is
        odd), and then can exit with 1 action. Since all pieces must exit, we
        sum these best case individual distances from each piece.
        """

        hscore = {'red': 0, 'green': 0, 'blue': 0}
        for colour in hscore:
            lst = []
            for qr in board:
                if board[qr] == colour:
                    lst.append(qr)

            hscore[colour] = sum(
                math.ceil(
                    self.exit_dist(
                        qr,
                        colour)) for qr in lst)

        return hscore


if __name__ == "__main__":
    main()
