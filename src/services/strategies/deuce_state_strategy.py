from models.match import Match
from services.strategies.game_state_strategy import GameStateStrategy


class DeuceStateStrategy(GameStateStrategy):
    def add_point(self, match: Match, score: dict, player_key: str, opponent_key: str, player_num: int) -> None:
        score[player_key]["points"] += 1
        if score[player_key]["points"] != score[opponent_key]["points"]:
            match.current_game_state = f'advantage_{player_num}'
