##########################
######   MINI-MAX   ######
##########################

colours = ['red', 'green', 'blue']

class MiniMax:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.currentNode = None     # GameNode
        self.successors = []        # List of GameNodes
        return

    def minimax(self, node, colour):
        # first, find the max value
        best_val = self.min_value(node, 0) # should be root node of tree

        # second, find the node which HAS that max value
        #  --> means we need to propagate the values back up the
        #      tree as part of our minimax algorithm
        successors = self.getSuccessors(node)
        print("HELLO WORLLDLDLDLDDDDDDD")
        print("MiniMax:  Utility Value of Root Node: = " + str(best_val))
        # find the node with our best move
        best_move = None
        for elem in successors:   # ---> Need to propagate values up tree for this to work
            if elem.value == best_val:
                best_move = elem
                break

        # return that best value that we've found
        return best_move


    def min_value(self, node, depth):
        # print "MiniMax-->MAX: Visited Node :: " + node.Name
        if(self.isTerminal(node)):
            return self.getUtility(node)

        inf = float('inf')
        min_value = {'red': inf, 'green': inf, 'blue': inf}

        successors_states = self.getSuccessors(node)
        depth += 1
        for state in successors_states:
            # We need to look at the relevant
            print("\n" + colours[depth%3])
            curr_col = colours[depth%3]
            min_value[curr_col] = min(min_value[curr_col], self.min_value(state, depth)[curr_col])

        return min_value


    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return node.value
