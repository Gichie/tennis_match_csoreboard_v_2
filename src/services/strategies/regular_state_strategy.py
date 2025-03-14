from models.match import Match
from services.score_utils import reset_game, SCORE_DIFF, is_tie_break
from services.strategies.game_state_strategy import GameStateStrategy

MIN_POINTS = 3


class RegularStateStrategy(GameStateStrategy):
    """
    Implements the game logic for the 'regular' state in a match.

    This strategy handles point additions when the game is in a regular state.
    It determines whether a player wins the game, or if the game transitions to deuce.
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
        if (
                score[player_key]["points"] > MIN_POINTS and
                score[player_key]["points"] - score[opponent_key]["points"] >= SCORE_DIFF
        ):
            reset_game(score, player_key)
            if is_tie_break(score, player_key, opponent_key):
                match.current_game_state = 'tie_break'

        elif (
                score[player_key]["points"] == MIN_POINTS and
                score[opponent_key]["points"] == MIN_POINTS
        ):
            match.current_game_state = 'deuce'
