from models.match import Match
from services.score_utils import process_tie_break
from services.strategies.game_state_strategy import GameStateStrategy


class TieBreakStateStrategy(GameStateStrategy):
    """
    Implements the game logic for the 'tie_break' state in a match.

    This strategy handles point additions during a tie-break game.
    It delegates the point processing to the `process_tie_break` function.
    """

    def add_point(
            self,
            match: Match,
            score: dict[str, dict[str, int]],
            player_key: str,
            opponent_key: str,
            player_num: int
    ) -> None:
        """
        Adds a point to the specified player's score and updates the game state during a tie-break.

        :param match: The Match object representing the current match.
        :param score: A dictionary representing the current score of the match.
        :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
        :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
        :param player_num: The player number (1 or 2).
        """
        process_tie_break(match, score, player_key, opponent_key)
