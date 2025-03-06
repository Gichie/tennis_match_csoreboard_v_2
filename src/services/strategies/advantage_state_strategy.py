from src.models.match import Match
from src.services.strategies.game_state_strategy import (
    GameStateStrategy,
    ResetGameFuncType,
    ResetSetFuncType,
    ProcessTieBreakFuncType
)


class AdvantageStateStrategy(GameStateStrategy):
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
        current_advantage_player = int(match.current_game_state.split('_')[1])
        if player_num == current_advantage_player:
            reset_game_func(score, player_key)
            match.current_game_state = 'regular'
        else:
            score[player_key]["points"] += 1
            match.current_game_state = 'deuce'
