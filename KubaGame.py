# Author: Matthew Norwood
# Date: 2021-05-30
# Description: KubaGame.py - This program contains two classes: KubaGame and Player. KubaGame manages the game board,
# and validates player moves among other things. The Player class handles each of the player objects and keeps track of
# the number of red marbles and player color marbles in possession by each of the individual players.

class KubaGame:
    """
    This class manages the game board for Kuba and tracks the placements and counts of all the marbles across the board.
    """

    def __init__(self, player1, player2):
        """
        Initializes a game of Kuba given two tuples representing player 1 and player 2 and the color they have
        chosen.
        """
        self._player1 = Player(player1)
        self._player2 = Player(player2)
        self._turn = None
        self._winner = None

        self._gameBoard = {
            (0, 0): 'W', (1, 0): 'W', (2, 0): 'X', (3, 0): 'X', (4, 0): 'X', (5, 0): 'B', (6, 0): 'B',
            (0, 1): 'W', (1, 1): 'W', (2, 1): 'X', (3, 1): 'R', (4, 1): 'X', (5, 1): 'B', (6, 1): 'B',
            (0, 2): 'X', (1, 2): 'X', (2, 2): 'R', (3, 2): 'R', (4, 2): 'R', (5, 2): 'X', (6, 2): 'X',
            (0, 3): 'X', (1, 3): 'R', (2, 3): 'R', (3, 3): 'R', (4, 3): 'R', (5, 3): 'R', (6, 3): 'X',
            (0, 4): 'X', (1, 4): 'X', (2, 4): 'R', (3, 4): 'R', (4, 4): 'R', (5, 4): 'X', (6, 4): 'X',
            (0, 5): 'B', (1, 5): 'B', (2, 5): 'X', (3, 5): 'R', (4, 5): 'X', (5, 5): 'W', (6, 5): 'W',
            (0, 6): 'B', (1, 6): 'B', (2, 6): 'X', (3, 6): 'X', (4, 6): 'X', (5, 6): 'W', (6, 6): 'W',
        }

        # my solution to detect if a move undoes the prior move is to keep copies of the prior board and compare a temp
        # board to it in the make move method.
        # learned this the hard way, use dict to pass by value.
        self._priorGameBoard = dict(self._gameBoard)

    def get_current_turn(self):
        """
        Returns the player who's turn it is currently. None if it's the start of the game.
        """
        return self._turn

    def get_winner(self):
        """
        Returns the winner of the current game. None if there is no winner.
        """
        return self._winner

    def get_opposite_player(self, player):
        """
        Given a player object, returns the opposite player.
        :return:
        """
        if player == self._player1:
            return self._player2
        else:
            return self._player1

    def make_move(self, playername, coordinates, direction):
        """
        Given a player name (object), coordinates upon which the marble is located, and direction to move the marble,
        will see if the move is valid, make the move, and then determine whether the move resulted in a win.
        :param playername: the player making the move
        :param coordinates: the coordinates of the marble to be moved.
        :param direction: the direction of the move. Valid directions: L, R, F, B (Left, Right, Forward, Backward)
        :return: True if valid, False otherwise. Also will trigger a win somehow.
        """

        temp_board = dict(self._gameBoard)
        #self.print_board(temp_board)
        if playername == self._player1.get_name():
            player = self._player1
        else:
            player = self._player2

        # check that it's the player's turn.
        if self._turn != player and self._turn is not None:
            return False

        if self.isvalid(coordinates, direction) is False:
            return False

        # execute the move -- put the row upon which the move is being made into an array, and then perform the
        # moves. We will then count the marbles in the result array, see if the number of 'B','W', or 'R' changed
        # and then insert the result array back in place of the old one.
        if direction == 'L':
            # get all of the values from the board where the row matches the coordinates for the move. since this is
            # a left move, create an array from these values starting at y=6.
            x_val = coordinates[0]
            array_to_sort = []
            for i in range(6, -1, -1):
                array_to_sort.append(temp_board[(x_val, i)])

            begin_red_count = self.red_marble_count_array(array_to_sort)
            result_array = self.push_array(array_to_sort, coordinates[1], player.get_color())
            end_red_count = self.red_marble_count_array(result_array)

            # see if this array has less reds
            if begin_red_count - end_red_count > 0:
                player.increase_captured()

            # now copy the result array into the temp board.
            for i in range(6, -1, -1):
                temp_board[(x_val, i)] = result_array[6 - i]

        if direction == 'R':
            # get all of the values from the board where the row matches the coordinates for the move. since this is
            # a right move, create an array from these values starting at y=0.
            x_val = coordinates[0]
            array_to_sort = []
            for i in range(0, 6):
                array_to_sort.append(temp_board[(x_val, i)])

            begin_red_count = self.red_marble_count_array(array_to_sort)
            result_array = self.push_array(array_to_sort, coordinates[1], player.get_color())
            end_red_count = self.red_marble_count_array(result_array)

            # see if this array has less reds
            if begin_red_count - end_red_count > 0:
                player.increase_captured()

            # now copy the result array into the temp board.
            for i in range(0, 6):
                temp_board[(x_val, i)] = result_array[i]

        if direction == 'F':
            # get all of the values from the board where the row matches the coordinates for the move. since this is
            # a forward move, create an array from these values starting at x=6.
            y_val = coordinates[1]
            array_to_sort = []
            for i in range(6, -1, -1):
                array_to_sort.append(temp_board[(i, y_val)])

            begin_red_count = self.red_marble_count_array(array_to_sort)
            result_array = self.push_array(array_to_sort, coordinates[0], player.get_color())
            end_red_count = self.red_marble_count_array(result_array)

            # see if this array has less reds
            if begin_red_count - end_red_count > 0:
                player.increase_captured()

            # now copy the result array into the temp board.
            for i in range(6, -1, -1):
                temp_board[(i, y_val)] = result_array[6 - i]

        if direction == 'B':
            # get all of the values from the board where the row matches the coordinates for the move. since this is
            # a backward move, create an array from these values starting at x = 0.
            y_val = coordinates[1]
            array_to_sort = []
            for i in range(0, 6):
                array_to_sort.append(temp_board[(i, y_val)])

            begin_red_count = self.red_marble_count_array(array_to_sort)
            result_array = self.push_array(array_to_sort, coordinates[0], player.get_color())
            end_red_count = self.red_marble_count_array(result_array)

            # see if this array has less reds
            if begin_red_count - end_red_count > 0:
                player.increase_captured()

            # now copy the result array into the temp board.
            for i in range(0, 6):
                temp_board[(i, y_val)] = result_array[i]

        #self.print_board(temp_board)

        # validate that the move didn't remove one of the current player's marbles.
        previous_count = self.get_marble_count_board(self._priorGameBoard)
        temp_count = self.get_marble_count_board(temp_board)
        current_color = player.get_color()

        if current_color == 'W':
            if previous_count[0] != temp_count[0]:
                return False

        if current_color == 'B':
            if previous_count[1] != previous_count[1]:
                return False

        # validate that the previous move was not undone by the current one.
        if self._priorGameBoard == temp_board:
            return False

        # Check if end conditions of game have been met -- a player wins if they push off 7 red stones or push off all
        # of the opposing player's stones. a player loses if they have no more valid moves.

        # win condition 1
        if temp_count[2] >= 7:
            self._priorGameBoard = self._gameBoard
            self._gameBoard = temp_board
            self._winner = playername
            return True

        # win condition 2
        if current_color == 'W':
            if temp_count[1] == 0:
                self._priorGameBoard = self._gameBoard
                self._gameBoard = temp_board
                self._winner = playername
                return True

        if current_color == 'B':
            if temp_count[0] == 0:
                self._priorGameBoard = self._gameBoard
                self._gameBoard = temp_board
                self._winner = playername
                return True

        # win condition 3 requires a function call to evaluate the temp board for possible moves for the opponent.
        opponent = self.get_opposite_player(player)
        if self.check_for_valid_moves(opponent) is False:
            self._priorGameBoard = self._gameBoard
            self._gameBoard = temp_board
            self._winner = playername
            return True

        # at the end, replace the prior board with the existing game board, and update the game board to the temp board.
        self._priorGameBoard = self._gameBoard
        self._gameBoard = temp_board

        # set the opposite player's turn here.
        self._turn = opponent
        return True

    def get_captured(self, playername):
        """
        Gets the number of red marbles that have been captured and by which player. calls the player class method which
        counts the number of marbles that player object possesses.
        :return: the number of captured balls.
        """
        if playername == self._player1.get_name():
            captured = self._player1.get_player_captured()
        else:
            captured = self._player2.get_player_captured()
        return captured

    def get_marble(self, coordinates):
        """
        Given a set of coordinates, return the color of the marble, if any, that is located at the coordinates.
        :param coordinates:
        :return: the color of the marble location at the coordinates specified.
        """
        marble = self._gameBoard[coordinates]
        return marble

    def get_marble_count(self):
        """
        Returns a 3-tuple with the count of White, Black, and Red marbles on the self board, in the order (W, B, R)
        """
        white = 0
        black = 0
        red = 0
        for value in self._gameBoard:
            if self._gameBoard[value] == 'W':
                white += 1
            elif self._gameBoard[value] == 'B':
                black += 1
            elif self._gameBoard[value] == 'R':
                red += 1
        return (white, black, red)

    def get_marble_count_board(self, board):
        """
        Returns a 3-tuple with the count of White, Black, and Red marbles on the given board, in the order (W, B, R)
        """
        white = 0
        black = 0
        red = 0
        for value in board:
            if board[value] == 'W':
                white += 1
            elif board[value] == 'B':
                black += 1
            elif board[value] == 'R':
                red += 1
        return (white, black, red)

    def isvalid(self, coordinates, direction):
        """
        Checks if a particular move is valid, given coordinates and a direction.
        :return: True if valid, False otherwise.
        """
        # check if the move is valid -- ie there is a free space on the side opposite the direction being pushed OR the
        # ball is on an edge that is opposite from the direction being pushed
        # check edges first -- any coordinate having 0 or 6 in the x position or 0 or 6 in the y position is along an
        # edge
        if self._gameBoard[coordinates] == 'X':
            return False
        if coordinates[0] not in (0, 6) and coordinates[1] not in (0, 6):
            # Means there's an internal move that has been made

            if direction == 'L':
                # check if the cell immediately to the right is open.
                open_coordinates = (coordinates[0]+1, coordinates[1])
                if self._gameBoard[open_coordinates] != 'X':
                    return False

            elif direction == 'R':
                # check if the cell immediately to the left is open.
                open_coordinates = (coordinates[0]-1, coordinates[1])
                if self._gameBoard[open_coordinates] != 'X':
                    return False

            elif direction == 'F':
                # check if the cell immediately to the bottom is open.
                open_coordinates = (coordinates[0], coordinates[1]-1)
                if self._gameBoard[open_coordinates] != 'X':
                    return False

            elif direction == 'B':
                # check if the cell immediately to the top is open.
                open_coordinates = (coordinates[0], coordinates[1]+1)
                if self._gameBoard[open_coordinates] != 'X':
                    return False

    def check_for_valid_moves(self, player):
        """
        Will evaluate the board to see if the supplied player object has any valid moves left.
        :return: True if there are valid moves, False otherwise.
        """
        # loop through all keys and directions checking for valid moves. if a single valid move is found, return true.
        for keys in self._gameBoard:
            if self._gameBoard[keys] == player.get_color():  # checks for valid moves only for the specified player
                for directions in ('L', 'R', 'F', 'B'):
                    if self.isvalid(keys, directions):
                        return True
        return False

    def push_array(self, array, starting_index, color):
        """
        This is a helper function that will push the marbles in an array that is provided at the starting index.
        :param color:
        :param starting_index:
        :param array:
        :return:
        """
        result_array = ['X']
        if starting_index > 0:
            for index in range(0, starting_index):
                result_array.append(array[index])
        for value in range(starting_index, len(array)):
            if len(result_array) == 7:
                break
            if array[value] == 'X' and array[value - 1] == color:
                continue
            result_array.append(array[value])

        return result_array

    def red_marble_count_array(self, array):
        red = 0
        for value in array:
            if value == 'R':
                red += 1
        return red

    def print_board(self, board):
        x = 0
        print("Begin board: ")
        for value in board:
            x += 1
            print(board[value], end='')
            if x % 7 == 0:
                print('\n')
        print("End board.")


class Player:
    """
    A class representing a player object.
    """

    def __init__(self, player):
        """
        initialize a Player object.
        :param player: a tuple with the player name and color.
        """
        self._player = player[0]
        self._color = player[1]
        self._captured = 0
        self._playerMarbleCount = 8

    def get_name(self):
        """
        get the name of the player for the current object.
        """
        return self._player

    def get_color(self):
        """
        get the color of marbles used by the player.
        """
        return self._color

    def get_player_captured(self):
        """
        returns number of red marbles captured.
        """
        return self._captured

    def get_marble_count(self):
        """
        returns number of player's marbles that are still on the game board.
        """
        return self._playerMarbleCount

    def increase_captured(self):
        """
        if a red marble is pushed off the board, increase the captured count.
        """
        self._captured += 1
        return

# "DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS (all pseudocode is listed below)"
# 1. Initialize the board - set up a dictionary where the keys are the coordinates of the board and the values are the
#    color of the marble or 'X' if there is no marble at that coordinate.
# 2. Determine how to track which player's move it is. - keep a list of the names of the player objects that have been
#    initialized for the board. Once the first player has made the move, set the current turn data member to be equal to
#    the element in the list not equal to the player making the move.
# 3. Determine how to validate move: 1. Check that it's the turn of the player making the move. 2. The game starts with
#    the opposite move data member being None. At the end of the move, the opposite move will be determined and
#    it will be stored in the opposite move data member. On every turn, the move being made will be compared to the
#    opposite move data member and if it matches, this will be an invalid move. 3. Finally, verify that there is an open
#    space opposite of the direction being moved to the starting coordinate.
# 4. Determine how to return the marble count. Iterate over the dictionary that represents the game board and store
#    counts for each color marble. Then return these counts as a tuple.
# 5. Determine how to move the marbles on the board - For each move, move to the opposite end of the board and slide the
#    marbles towards (or over) the edge one at a time (iterate to the coordinate starting point).
#    Each move will open up the adjacent space.

# Process Flow (pseudocode):
# 1. Initialize the game board
# 2. Either player makes a move.
#    a. Verify that the move is valid
#       _ Is the current player's move = None or does it match the player making the move?
#       - Is the side from which the marbles will be pushed empty, either with an open space or the border of the board?
#       - Check if the move is the opposite of prior move by comparing it to the data member stored from the prior move.
#    b. Execute the move.
#       - Move all the marbles in the direction specified starting at the coordinates specified.
#       - Determine if the move resulted in a marble being captured.
#           - If a marble was captured, either a red one or by the opposing player, update the counts for the player
#             objects as necessary.
#    c. Check if the move resulted in a win of some kind.
#       - Did the player making the move collect a 7th red marble?
#       - Did the player making the move collect the last player marble belonging to the opposing player?
#       - Did the move prevent either player from making a subsequent move?
#       c1. If a move resulted in a win, update the winning player data member.
#    d. If a win did not occur, catalogue the move that was completed, calculate the opposite move, store it in a data
#       member, update the turn to the opposite player name.
# 3. Wait for more input.

#
# game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
# val1 = game.get_marble_count() #returns (8,8,13)
# print(val1)
# val1ish = game.get_marble((0, 0))
# print(val1ish)
# val2 = game.get_captured('PlayerA') #returns 0
# print(val2)
# val3 = game.get_current_turn() #returns 'PlayerB' because PlayerA has just played.
# val4 = game.get_winner() #returns None
# result = game.make_move('PlayerA', (6, 5), 'F')
# print(result)
# #game.print_board(game._gameBoard)
# result2 = game.make_move('PlayerA', (6, 5), 'L') #Cannot make this move
# print(result2)
# result3 = game.get_marble((5, 5)) #returns 'W'
# print(result3)