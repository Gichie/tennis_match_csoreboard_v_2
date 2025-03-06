from src.models.match import Match
from src.services.strategies.game_state_strategy import (
    GameStateStrategy,
    ResetGameFuncType,
    ResetSetFuncType,
    ProcessTieBreakFuncType
)

MIN_POINTS = 3
SCORE_DIFF = 2


class RegularStateStrategy(GameStateStrategy):
    def add_point(
            self,
            match: Match,
            score: dict,
            player_key: str,
            opponent_key: str,
            player_num: int,
            reset_game_func: ResetGameFuncType,
            reset_set_func: ResetSetFuncType,
            process_tie_break_func: ProcessTieBreakFuncType
    ) -> None:

        score[player_key]["points"] += 1
        if (
                score[player_key]["points"] > MIN_POINTS and
                score[player_key]["points"] - score[opponent_key]["points"] >= SCORE_DIFF
        ):
            reset_game_func(score, player_key)
        elif (
                score[player_key]["points"] == MIN_POINTS and
                score[opponent_key]["points"] == MIN_POINTS
        ):
            match.current_game_state = 'deuce'
