from models.match import Match
from services.strategies.game_state_strategy import GameStateStrategy


class DeuceStateStrategy(GameStateStrategy):
    """
    Implements the game logic for the 'deuce' state in a match.

    This strategy handles point additions when the game is in a deuce state.
    It determines whether a player gains an advantage or if the score remains at deuce.
    """

    def add_point(self, match: Match, score: dict, player_key: str, opponent_key: str, player_num: int) -> None:
        """
        Adds a point to the specified player's score and updates the game state.

        :param match: The Match object representing the current match.
        :param score: A dictionary representing the current score of the match.
        :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
        :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
        :param player_num: The player number (1 or 2).
        """
        score[player_key]["points"] += 1
        if score[player_key]["points"] != score[opponent_key]["points"]:
            match.current_game_state = f'advantage_{player_num}'
