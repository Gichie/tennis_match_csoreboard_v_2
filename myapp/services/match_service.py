import json
import uuid
from typing import Dict

from sqlalchemy.orm import Session

from myapp.models.match import Match

MIN_GAMES = 3


class MatchService:
    @staticmethod
    def get_initial_score() -> Dict:
        """Возвращает начальную структуру счёта"""
        return {
            "player1": {"sets": 0, "games": 0, "points": 0},
            "player2": {"sets": 0, "games": 0, "points": 0}
        }

    @staticmethod
    def create_match(db: Session, player1_id: int, player2_id: int) -> Match:
        new_match = Match(
            uuid=str(uuid.uuid4()),
            score=json.dumps(MatchService.get_initial_score()),
            player1_id=player1_id,
            player2_id=player2_id
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return new_match

    @staticmethod
    def add_point(db: Session, match: Match, player_num: int) -> None:
        score = json.loads(match.score)
        player_key = f"player{player_num}"
        opponent_key = "player2" if player_num == 1 else "player1"

        if match.current_game_state == "regular":
            score[player_key]["points"] += 1
            if score[player_key]["points"] > 3 and score[player_key]["points"] - score[opponent_key]["points"] > 1:
                MatchService._reset_game(score, player_key)
            elif score[player_key]["points"] == 3 and score[opponent_key]["points"] == 3:
                match.current_game_state = 'deuce'

        elif match.current_game_state == 'deuce':
            score[player_key]["points"] += 1
            if score[player_key]["points"] != score[opponent_key]["points"]:
                match.current_game_state = f'advantage_{player_num}'

        elif match.current_game_state.startswith('advantage'):
            current_advantage_player = int(match.current_game_state.split('_')[1])
            if player_num == current_advantage_player:
                MatchService._reset_game(score, player_key)
                match.current_game_state = 'regular'
            else:
                score[player_key]["points"] += 1
                match.current_game_state = 'deuce'

        elif match.current_game_state == 'tie_break':
            MatchService.process_tie_break(score, player_key, opponent_key)
            match.current_game_state = 'regular'

        # Проверка завершения сета (6 игр с разницей >= 2 или 7-5)
        if score[player_key]["games"] >= MIN_GAMES and abs(
                score[player_key]["games"] - score[opponent_key]["games"]) >= 2:
            MatchService._reset_set(score, player_key)
            match.current_game_state = 'regular'
        elif score[player_key]["games"] == MIN_GAMES and score[opponent_key]["games"] == MIN_GAMES:
            match.current_game_state = 'tie_break'

        match.score = json.dumps(score)

        # Проверка завершения матча (2 сета)
        if MatchService.is_match_finished(match):
            if player_num == 1:
                match.winner_id = match.player1_id
            else:
                match.winner_id = match.player2_id

        db.commit()

    @staticmethod
    def process_tie_break(score, player_key, opponent_key):
        score[player_key]['points'] += 1
        if score[player_key]['points'] >= 7 and (score[player_key]['points'] - score[opponent_key]['points']) >= 2:
            MatchService._reset_set(score, player_key)

    @staticmethod
    def _reset_game(score: dict, winner_key: str):
        score[winner_key]["games"] += 1
        score[winner_key]["points"] = 0
        opponent_key = "player2" if winner_key == "player1" else "player1"
        score[opponent_key]["points"] = 0

    @staticmethod
    def _reset_set(score: dict, winner_key: str):
        score[winner_key]["sets"] += 1
        score[winner_key]["games"] = 0
        opponent_key = "player2" if winner_key == "player1" else "player1"
        score[opponent_key]["games"] = 0
        score[winner_key]["points"] = 0
        score[opponent_key]["points"] = 0

    @staticmethod
    def is_match_finished(match: Match) -> bool:
        score = json.loads(match.score)
        return score["player1"]["sets"] == 2 or score["player2"]["sets"] == 2

    @staticmethod
    def get_match_by_uuid(db: Session, uuid: str) -> Match:
        return db.query(Match).filter(Match.uuid == uuid).first()
