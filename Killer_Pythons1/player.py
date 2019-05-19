
from Killer_Pythons.gametree import *
from Killer_Pythons.minimax import *


_STARTING_HEXES = {
    'red': {(-3, 3), (-3, 2), (-3, 1), (-3, 0)},
    'green': {(0, -3), (1, -3), (2, -3), (3, -3)},
    'blue': {(3, 0), (2, 1), (1, 2), (0, 3)},
}
_FINISHING_HEXES = {
    'red': {(3, -3), (3, -2), (3, -1), (3, 0)},
    'green': {(-3, 3), (-2, 3), (-1, 3), (0, 3)},
    'blue': {(-3, 0), (-2, -1), (-1, -2), (0, -3)},
}
_ADJACENT_STEPS = [(-1, +0), (+0, -1), (+1, -1), (+1, +0), (+0, +1), (-1, +1)]

RAN = range(-3, +3 + 1)
HEXES = {(q, r) for q in RAN for r in RAN if -q - r in RAN}


class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (Red, Green or Blue). The value will be one of the
        strings "red", "green", or "blue" correspondingly.
        """
        self.colour = colour
        self.score = {'red': 0, 'green': 0, 'blue': 0}
        self.board = {qr: ' ' for qr in HEXES}
        for colourx in _STARTING_HEXES:
            for qr in _STARTING_HEXES[colourx]:
                self.board[qr] = colourx

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed
        actions, your player must return a pass instead. The action (or pass)
        must be represented based on the above instructions for representing
        actions.
        """
        return maxn(self.colour, self.score, self.board)

        # TODO: Decide what action to take.
        # available_actions = []
        # for qr in self.hexes:
        #     if self.board[qr] == self.colour:
        #         if qr in _FINISHING_HEXES[self.colour]:
        #             available_actions.append(("EXIT", qr))
        #         q, r = qr
        #         for dq, dr in _ADJACENT_STEPS:
        #             for i, atype in [(1, "MOVE"), (2, "JUMP")]:
        #                 tqr = q+dq*i, r+dr*i
        #                 if tqr in self.hexes:
        #                     if self.board[tqr] == ' ':
        #                         available_actions.append((atype, (qr, tqr)))
        #                         break
        # if not available_actions:
        #     available_actions.append(("PASS", None))
        #
        # print(self.board)
        # Your mum is your dad
        # print(available_actions)
        #
        # for (type, coord) in available_actions:
        #     if type == "EXIT":
        #         return (type, coord)
        # for (type, coord) in available_actions:
        #     if type == "JUMP":
        #         return (type, coord)
        # for (type, coord) in available_actions:
        #     if type == "MOVE":
        #         return (type, coord)
        # for (type, coord) in available_actions:
        #     if type == "PASS":
        #         return (type, coord)
        #
        #
        # We have the list of next avalabile moves handy and we want to make a
        # Tree so that we can

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red",
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action
        (or pass) for the player colour (your method does not need to validate
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.

        atype, aargs = action
        if atype == "MOVE":
            qr_a, qr_b = aargs
            self.board[qr_a] = ' '
            self.board[qr_b] = colour

        elif atype == "JUMP":
            qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
            qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
            self.board[qr_a] = ' '
            self.board[qr_b] = colour
            self.board[qr_c] = colour

        elif atype == "EXIT":
            qr = aargs
            self.board[qr] = ' '
            self.score[colour] += 1
        else:  # atype == "PASS":
            pass
