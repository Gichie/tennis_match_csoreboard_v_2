from abc import ABC, abstractmethod

from myapp.models.match import Match
from typing import Callable


ResetGameFuncType = Callable[[dict, str], None]
ResetSetFuncType = Callable[[dict, str], None]
ProcessTieBreakFuncType = Callable[[dict, str, str], None]


class GameStateStrategy(ABC):
    @abstractmethod
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
        pass
