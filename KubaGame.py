# Author: Matthew Norwood
# Date: 2021-05-30
# Description: KubaGame.py


class KubaGame:
    """

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

    def make_move(self, playername, coordinates, direction):
        """
        Given a player name, coordinates upon which the marble is located, and direction to move the marble, will
        see if the move is valid, make the move, and then determine whether the move resulted in a win.
        :param playername: the player making the move
        :param coordinates: the coordinates of the marble to be moved.
        :param direction: the direction of the move. Valid directions: L, R, F, B (Left, Right, Forward, Backward)
        :return: True
        """

    def get_captured(self, player):
        """
        Gets the number of red marbles that have been captured and by which player.
        :return:
        """
        captured = player.get_player_captured()
        return captured

    def get_marble(self, coordinates):
        """
        Given a set of coordinates, return the color of the marble, if any, that is located at the coordinates.
        :param coordinates:
        :return:
        """
        marble = self._gameBoard[coordinates]
        if marble != 'X':
            return None
        else:
            return marble


class Player:
    """
    A class representing a player object.
    """

    def __init__(self, player):
        """
        initialize a Player object.
        :param player:
        """
        self._player = player[0]
        self._color = player[1]
        self._captured = 0
        self._playerMarbleCount = 8

    def get_color(self):
        """

        :return:
        """
        return self._color

    def get_player_captured(self):
        """

        :return:
        """
        return self._captured

    def get_player_marble_count(self):
        """

        :return:
        """
        return self._playerMarbleCount

    def increase_captured(self):
        """

        :return:
        """

        self._captured += 1
        return
