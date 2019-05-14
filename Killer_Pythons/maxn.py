
class MaxN:

    def __init__(self, board, hexes, colour, score):
        self.layers = 6
        self.hexes = hexes
        self.colour = colour
        self.board = board
        self.score = score
        self.items = []
        col = ['red', 'green', 'blue']
        for i in range(layers):
            currcol = col[i%3]
            self.items.append(self.board, [])



    def recursiveadd():


    def add_layer(self, colour):
        for qr in self.hexes:
            if self.board[qr] == self.colour:
                if qr in _FINISHING_HEXES[self.colour]:
                    self.items.append()[self.board]
                    self.score[colour] += 1
                    self.p_map[self.board[qr]] = score
                    self.h_map[self.board[qr]] = ("EXIT", qr)
                q, r = qr
                for dq, dr in _ADJACENT_STEPS:
                    for i, atype in [(1, "MOVE"), (2, "JUMP")]:
                        tqr = q+dq*i, r+dr*i
                        if tqr in self.hexes:
                            if self.board[tqr] == ' ':
                                self.p_map[self.board[qr]] = score
                                self.h_map[self.board[qr]] = (atype, (qr, tqr))
                                break
        if not self.items:
            self.p_map[self.board[qr]] = score
            self.h_map[self.board[qr]] = ("PASS", None)
