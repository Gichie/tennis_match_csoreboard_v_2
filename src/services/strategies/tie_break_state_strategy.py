from models.match import Match
from services.score_utils import process_tie_break
from services.strategies.game_state_strategy import GameStateStrategy


class TieBreakStateStrategy(GameStateStrategy):
    def add_point(self, match: Match, score: dict, player_key: str, opponent_key: str, player_num: int) -> None:
        process_tie_break(match, score, player_key, opponent_key)
