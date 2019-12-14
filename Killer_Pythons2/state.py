"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: State representation

Authors: Hamish Gunasekara, Zoe Schwerkolt

The below code (particularly for the class State) was inspired by Matt
Farrugia-Roberts' code in his state.py created for the missionaries and
cannibals problem.
"""

import copy
from functools import total_ordering

BOARDDIM = 3 # Half-width of the hexagonal board

class Coords:
    """
    Represents board coordinates
    """

    # Initialises the Coords class
    def __init__(self, q, r):
        self.q = q
        self.r = r

    # Creates string representation of the Coords class
    def __str__(self):
        return "({}, {})".format(self.q, self.r)

    # Creates representation of the Coords class
    def __repr__(self):
        return str(self)

    # Creates Hash of Coords class
    def __hash__(self):
        coord_tuple = (self.q, self.r)
        return hash(coord_tuple)

    # Checks if Coords self is less than Coords other
    def __lt__(self, other):
        return (self.q, self.r) < (other.q, other.r)

    # Checks equality between the Coords classes
    def __eq__(self, other):
        return (self.q, self.r) == (other.q, other.r)

    # Checks whether given Coords are within the bounds of the board
    def within_board(self):
        return (-BOARDDIM <= self.q <= BOARDDIM and
                -BOARDDIM <= self.r <= BOARDDIM and
                -BOARDDIM <= self.q + self.r <= BOARDDIM)

    # Finds all neighbours of given Coords
    def neighbours(self):
        neighbour_list = []
        for i in range(self.q - 1, self.q + 2):
            for j in range(self.r - 1, self.r + 2):
                neighbour = Coords(i, j)
                if (not (neighbour == Coords(self.q - 1, self.r - 1)
                         or neighbour == self
                         or neighbour == Coords(self.q + 1, self.r + 1))
                        and neighbour.within_board()):
                    neighbour_list.append(neighbour)
        return neighbour_list


class State:
    """
    Represents a Chexers board state
    """

    # Initialises State class
    def __init__(self, pieces, blocks, colour, exited, cost, action, prev):
        self.pieces = pieces
        self.blocks = blocks
        self.colour = colour
        self.exited = exited
        self.cost = cost
        self.action = action
        self.prev = prev

    # Creates string representation of State class
    def __str__(self):
        return "S({}, {})".format(self.pieces, self.blocks)

    # Creates representation of State class
    def __repr__(self):
        return str(self)

    # Copies State class without copying pointer
    def copy(self):
        return State(copy.copy(self.pieces), copy.copy(self.blocks),
                     copy.copy(self.colour), copy.copy(self.exited),
                     copy.copy(self.cost), copy.copy(self.action),
                     copy.copy(self.prev))

    # Converts State class into a unique tuple (for equality and hashability)
    def tup(self):
        pieces_tuple = tuple(sorted(self.pieces))
        blocks_tuple = tuple(sorted(self.blocks))
        return (pieces_tuple, blocks_tuple, self.exited)

    # Checks equality between State classes
    def __eq__(self, other):
        return self.tup() == other.tup()

    # Checks if State self is less than State other
    def __lt__(self, other):
        return self.tup() < other.tup()

    # Creates Hash of State class
    def __hash__(self):
        return hash(self.tup())

    # Checks whether the goal state has been reached
    def is_goal(self):
        return not self.pieces

    # Finds all the possible successor states - i.e. all possible moves for
    # each piece on the board
    def successors(self):
        allowed_states = []
        for piece in self.pieces:
            # Iterates through each neighbour of a piece
            for neighbour in piece.neighbours():
                next_state = self.copy()
                next_state.pieces.remove(piece)
                next_state.cost += 1
                # Checks to see if neighbour can be moved into
                if not (neighbour in self.pieces or neighbour in self.blocks):
                    next_state.pieces.append(neighbour)
                    next_state.action = ("MOVE from " + str(piece) + " to " +
                                         str(neighbour) + ".")
                    next_state.prev = self
                    allowed_states.append(next_state)
                # If not, the neighbour can be jumped over
                else:
                    jump_target = jump(neighbour, piece)
                    if (jump_target.within_board()
                            and not (jump_target in self.pieces
                                     or jump_target in self.blocks)):
                        next_state.pieces.append(jump_target)
                        next_state.action = ("JUMP from " + str(piece) + " to "
                                             + str(jump_target) + ".")
                        next_state.prev = self
                        allowed_states.append(next_state)

            # Checks to see if piece is able to exit
            if at_exit(piece, self.colour):
                next_state = self.copy()
                next_state.pieces.remove(piece)
                next_state.exited += 1
                next_state.cost += 1
                next_state.action = "EXIT from " + str(piece) + "."
                next_state.prev = self
                allowed_states.append(next_state)

        return allowed_states

    # Initialises the heuristic dictionary and list of nodes to start the
    # breadth-first search which evaluates the heuristic function for each
    # coord
    def start_heuristic_bfs(self):
        heuristic_dict = {}
        nodes = []

        # Assigns the initial value of nodes to be the coords at the exit of
        # a given colour
        for x in range(-BOARDDIM, 1):
            if self.colour == 'red':
                q = BOARDDIM
                piece = Coords(q, x)
            elif self.colour == 'green':
                r = BOARDDIM
                piece = Coords(x, r)
            elif self.colour == 'blue':
                y = -BOARDDIM - x
                piece = Coords(x, y)

            # Only requires one move to exit the board from these initial
            # coords
            if not (piece in self.blocks):
                heuristic_dict[piece] = 1
                nodes.append((piece, 1))

        return nodes, heuristic_dict

    # Creates the heuristic dictionary for the board of the heuristic value for
    # each coordinate based on a breadth-first search of the board with the
    # blocks in place
    def init_heuristic(self):
        nodes, heuristic_dict = self.start_heuristic_bfs()

        # Breadth-first search of the entire board, from the exit point
        # backwards, determining the minimum number of moves it would take to
        # get a piece to exit from a given coord
        while nodes:
            (piece, cost) = nodes.pop(0)
            for neighbour in piece.neighbours():

                # Adds a cost of 1 to adjacent pieces that haven't already been
                # explored
                if (not (neighbour in self.blocks) and
                        not (neighbour in heuristic_dict)):
                    heuristic_dict[neighbour] = cost + 1
                    nodes.append((neighbour, cost + 1))

                # Adds a cost of 1 to pieces that could be jumped to that
                # haven't already been explored
                jump_target = jump(neighbour, piece)
                if (not (jump_target in self.blocks) and
                        not (jump_target in heuristic_dict)):
                    heuristic_dict[jump_target] = cost + 1
                    nodes.append((jump_target, cost + 1))

        return heuristic_dict

def at_exit(piece, colour):
    """
    Function to return whether a piece of a given colour has an available exit
    action, i.e. is on the correct edge of the board.

    Arguments:

    * `piece` -- coords representing the position of the given piece.

    * `colour` -- a string 'red', 'green' or 'blue' representing the colour of
    the piece.
    """
    return ((colour == 'red' and piece.q == BOARDDIM) or
            (colour == 'green' and piece.r == BOARDDIM) or
            (colour == 'blue' and piece.q + piece.r == -BOARDDIM))

def jump(neighbour, with_piece):
    """
    Function to return the coords where a given piece will land if it jumps
    over a given neighbour

    Arguments:

    * `neighbour` -- coords representing the position of the piece to be jumped
    over

    * `with_piece` -- coords representing the piece `neighbour` will be jumped
    over with
    """
    return Coords(2 * neighbour.q - with_piece.q,
                  2 * neighbour.r - with_piece.r)
