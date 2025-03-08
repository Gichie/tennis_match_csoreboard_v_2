from src.models.match import Match
from src.services.score_utils import reset_game, is_tie_break
from src.services.strategies.game_state_strategy import GameStateStrategy


class AdvantageStateStrategy(GameStateStrategy):
    def add_point(self, match: Match, score: dict, player_key: str, opponent_key: str, player_num: int) -> None:
        current_advantage_player = int(match.current_game_state.split('_')[1])
        if player_num == current_advantage_player:
            reset_game(score, player_key)
            if is_tie_break(score, player_key, opponent_key):
                match.current_game_state = 'tie_break'
            else:
                match.current_game_state = 'regular'
        else:
            score[player_key]["points"] += 1
            match.current_game_state = 'deuce'
