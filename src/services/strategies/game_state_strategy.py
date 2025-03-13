from abc import ABC, abstractmethod

from models.match import Match


class GameStateStrategy(ABC):
    @abstractmethod
    def add_point(self, match: Match, score: dict, player_key: str, opponent_key: str, player_num: int) -> None:
        pass
