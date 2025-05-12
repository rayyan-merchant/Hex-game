"""
A data structure used to represent an arbitrary hex game state
"""
from math import inf
from heapq import heappop, heappush

# constants:
# the code used to represent a swap
SWAP_MOVE = (-1, -1)
# the list of directions that are connected to a stone
ADJACENT = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]


# This class is an abstract model for the hex board that can store information
class HexBoard:
    def __init__(self, size=11, swap_rule=False):
        # the width and height of the board
        self.size = size
        # 0 means empty, 1 means a player 1 piece, -1 means a player 2 piece
        self.board = [[0] * size for _ in range(size)]
        # a rule that allows the second player to "swap places" as their first move
        self.swap_rule = swap_rule
        # a history of moves made.
        self.move_list = []
        # the player with the next move. either 1 or -1
        self.turn = 1
        # the player that's won the game
        self._winner = 0
        # the group of stones that connect the sides
        self._winning_group = None

    # for convenience, treat indexing on the hex board as indexing on the board itself
    def __getitem__(self, item):
        return self.board[item]

    # to use the board as a dictionary key, get its board state in a tuple
    def hashable(self):
        return tuple((tuple(row) for row in self.board))

    # treat the winner as a property so that it is only checked when we need to
    @property
    def winner(self):
        if self._winner is None:
            self._update_winner()
        return self._winner

    @property
    def winning_group(self):
        if self._winner is None:
            self._update_winner()
        return self._winning_group

    # checks if a given position is on the board
    def in_bounds(self, row, col):
        return (0 <= row < self.size) and (0 <= col < self.size)

    # if a move is valid, updates the board
    def play(self, row, col):
        moved = False

        # cant move if somebody already won
        if self.winner != 0:
            return moved

        # if there's no move there already, its valid
        if self.in_bounds(row, col) and self.board[row][col] == 0:
            self.board[row][col] = self.turn
            self.move_list.append((row, col))
            self.turn *= -1
            moved = True
            # in this new board state, we don't know if somebody's won
            self._winner = None

        # if swapping is allowed and it's player 2's first move, they can take player 1's first move
        elif self.swap_rule and len(self.move_list) == 1 and (
                        (row, col) == SWAP_MOVE or (row, col) == self.move_list[0]):
            # we mirror it across the board to make it seem like the players switched
            row, col = self.move_list[0]
            self.board[row][col] = 0
            self.board[col][row] = -1
            self.move_list.append(SWAP_MOVE)
            self.turn *= -1
            moved = True

        return moved

    # removes the most recent move
    def undo(self):
        # if the last move won, then we need to clear the result
        self._winner = 0
        self._winning_group = None
        self.turn *= -1
        row, col = self.move_list.pop()
        if (row, col) == SWAP_MOVE:
            row, col = self.move_list[0]
            self.board[col][row] = 0
            self.board[row][col] = 1
        else:
            self.board[row][col] = 0

    # sets the winner of the match
    def resign(self):
        self._winner = -self.turn
        # print('Player',self.turn%3,'resigned')
        # print('Winner is',self.winner%3)

    # checks if a player has made a connection between their walls
    def is_connected(self, player, debug=False):
        # For player 1 (blue), we need to connect left to right (column 0 to column size-1)
        # For player -1 (red), we need to connect top to bottom (row 0 to row size-1)
        
        # First, check if there are any player stones on both sides
        has_start = False
        has_end = False
        
        if player == 1:
            # Check if player 1 has stones in leftmost and rightmost columns
            for i in range(self.size):
                if self.board[i][0] == player:
                    has_start = True
                if self.board[i][self.size-1] == player:
                    has_end = True
        else:
            # Check if player -1 has stones in top and bottom rows
            for i in range(self.size):
                if self.board[0][i] == player:
                    has_start = True
                if self.board[self.size-1][i] == player:
                    has_end = True
        
        # If player doesn't have stones on both sides, no connection is possible
        if not (has_start and has_end):
            return None
        
        # Initialize the search queue with the starting positions
        searchq = []
        if player == 1:
            # Start from all cells in the leftmost column that belong to player 1
            for i in range(self.size):
                if self.board[i][0] == player:
                    # Priority, row, col
                    heappush(searchq, (self.size, i, 0))
        else:
            # Start from all cells in the top row that belong to player -1
            for i in range(self.size):
                if self.board[0][i] == player:
                    # Priority, row, col
                    heappush(searchq, (self.size, 0, i))
        
        if debug: dist_grid = [['-'] * self.size for _ in range(self.size)]
        
        # Track parent cells for path reconstruction
        parent = dict()
        # Track visited cells to avoid cycles
        visited = set()
        # Track the last cell visited
        row, col = -1, -1
        connected = False
        
        # Process the search queue
        while searchq:
            weight, row, col = heappop(searchq)
            
            # Skip if already visited
            if (row, col) in visited:
                continue
                
            # Mark as visited
            visited.add((row, col))
            
            # Check if we've reached the opposite side
            if (player == 1 and col == self.size - 1) or (player == -1 and row == self.size - 1):
                connected = True
                break
                
            # Explore adjacent cells
            for dy, dx in ADJACENT:
                next_row = row + dy
                next_col = col + dx
                
                # Check if the cell is within bounds
                if not (0 <= next_row < self.size and 0 <= next_col < self.size):
                    continue
                    
                # Check if the cell belongs to the player and hasn't been visited
                if self.board[next_row][next_col] == player and (next_row, next_col) not in visited:
                    # Record the parent for path reconstruction
                    parent[(next_row, next_col)] = (row, col)
                    # Add to search queue with priority based on distance to goal
                    priority = self.size - next_col if player == 1 else self.size - next_row
                    heappush(searchq, (priority, next_row, next_col))
        
        # Reconstruct the winning path if connected
        if connected:
            pos = (row, col)
            winning_group = [pos]  # Include the final cell
            while pos in parent:
                pos = parent[pos]
                winning_group.append(pos)
            return winning_group
        else:
            return None

    # checks if either player has won
    def _update_winner(self):
        # First check if player 1 (blue) has won
        group = self.is_connected(1)
        if group:
            self._winner = 1
            self._winning_group = group
            return
        
        # Then check if player -1 (red) has won
        group = self.is_connected(-1)
        if group:
            self._winner = -1
            self._winning_group = group
            return
        
        # If we've reached this point, no one has won yet
        self._winner = 0
        self._winning_group = None

    # draws a nice looking ascii board
    def pretty_print(self, chars=None):
        # Ensure winner and winning path are calculated
        if self._winner is None:
            self._update_winner()
            
        # spacing should be odd for things to be consistent
        spacing = 3
        string = '\n' + ' ' * (2 + (spacing + 1) // 2)
        for i in range(self.size):
            string += ('{:' + str(spacing + 1) + '}').format(str(i + 1) + ':')
        string += '\n' + ' ' * (3 + (spacing + 1) // 2) + ('□' + ' ' * spacing) * self.size
        for i, row in enumerate(self.board):
            string += ('\n' + '{:>' + str(2 + i * (spacing + 1) // 2) + '} ■').format(str(i + 1) + ':')
            for j, num in enumerate(row):
                if self._winning_group and (i,j) in self._winning_group and (i,j-1) in self._winning_group:
                    string += ']' + ' ' * (spacing - 2) + '['
                elif self._winning_group and (i,j) in self._winning_group:
                    string += ' ' * (spacing - 1) + '['
                elif self._winning_group and (i,j-1) in self._winning_group:
                    string += ']' + ' ' * (spacing - 1)
                elif self.move_list and (self.move_list[-1] == (i,j) or
                        (self.move_list[-1] == SWAP_MOVE and self.move_list[-2] == (i,j))):
                    string += ' ' * (spacing - 1) + '('
                elif self.move_list and (self.move_list[-1] == (i,j-1) or
                        (self.move_list[-1] == SWAP_MOVE and self.move_list[-2] == (i,j-1))):
                    string += ')' + ' ' * (spacing - 1)
                else:
                    string += ' ' * spacing


                if num == 0:
                    if chars:
                        string += chars[i][j]
                    else:
                        string += '·'
                elif num < 0:
                    string += '○'
                else:
                    string += '●'
            if self._winning_group and (i,self.size-1) in self._winning_group:
                string += ']' + ' ' * (spacing-1)
            elif self.move_list and self.move_list[-1] == (i, self.size-1):
                string += ')' + ' ' * (spacing-1)
            else:
                string += ' ' * spacing
            string += '■'
        string += '\n' + ' ' * (4 + self.size * (spacing + 1) // 2) + (' ' * spacing + '□') * self.size
        print(string)
