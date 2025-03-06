from src.models.match import Match
from src.services.strategies.game_state_strategy import (
    GameStateStrategy,
    ResetGameFuncType,
    ResetSetFuncType,
    ProcessTieBreakFuncType
)


class TieBreakStateStrategy(GameStateStrategy):
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
        process_tie_break_func(score, player_key, opponent_key)
        match.current_game_state = 'regular'
