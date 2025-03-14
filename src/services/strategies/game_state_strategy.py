from abc import ABC, abstractmethod

from models.match import Match


class GameStateStrategy(ABC):
    """
    Abstract base class for game state strategies.

    This class defines the interface for all strategies that handle point additions
    and game state updates in different game states (e.g., deuce, advantage).
    """

    @abstractmethod
    def add_point(self, match: Match, score: dict, player_key: str, opponent_key: str, player_num: int) -> None:
        """
        Adds a point to the specified player's score and updates the game state.

        :param match: The Match object representing the current match.
        :param score: A dictionary representing the current score of the match.
        :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
        :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
        :param player_num: The player number (1 or 2).
        """
        pass
