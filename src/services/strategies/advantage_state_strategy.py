import logging

from exceptions import InvalidGameStateError
from models.match import Match
from services.score_utils import reset_game, is_tie_break
from services.strategies.game_state_strategy import GameStateStrategy

logger = logging.getLogger(__name__)


class AdvantageStateStrategy(GameStateStrategy):
    """
    Implements the game logic for the 'advantage' state in a match.

    This strategy handles point additions when the game is in an advantage state
    (e.g., 'advantage_1' or 'advantage_2'). It determines whether the advantage
    player wins the game, or if the game returns to deuce.
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
        Adds a point to the specified player's score and updates the game state.

        :param match: The Match object representing the current match.
        :param score: A dictionary representing the current score of the match.
        :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
        :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
        :param player_num: The player number (1 or 2).
        """
        if not match.current_game_state.startswith('advantage_'):
            logger.error("Invalid game state for AdvantageStateStrategy: {match.current_game_state}}")
            raise InvalidGameStateError(f"Expected advantage state but got: {match.current_game_state}")

        try:
            current_advantage_player = int(match.current_game_state.split('_')[1])
        except (IndexError, ValueError) as e:
            logger.error(
                f"Error parsing advantage player from game state: {match.current_game_state}",
                exc_info=True
            )
            raise InvalidGameStateError(f"Invalid advantage game state format: {match.current_game_state}") from e

        logger.debug(
            f"Advantage state: current advantage player is {current_advantage_player}, scoring player is {player_num}"
        )

        if player_num == current_advantage_player:
            reset_game(score, player_key)
            if is_tie_break(score, player_key, opponent_key):
                match.current_game_state = 'tie_break'
            else:
                match.current_game_state = 'regular'
        else:
            score[player_key]["points"] += 1
            match.current_game_state = 'deuce'
            logger.debug(f"Point for player {player_num} in deuce. Game state reset to deuce.")
