import json
import uuid
from typing import Dict

from sqlalchemy.orm import Session

from myapp.models.match import Match
from myapp.models.player import Player


class MatchService:
    @staticmethod
    def get_initial_score() -> Dict:
        """Возвращает начальную структуру счёта"""
        return {
            "player1": {
                "sets": 0,
                "games": 0,
                "points": 0
            },
            "player2": {
                "sets": 0,
                "games": 0,
                "points": 0
            }
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

        # Обновляем очки
        player_key = f"player{player_num}"
        score[player_key]["points"] += 1

        # Логика перевода очков в геймы
        if score[player_key]["points"] >= 4:
            score[player_key]["games"] += 1
            score[player_key]["points"] = 0

            # Сброс очков у другого игрока
            other_player = "player2" if player_num == 1 else "player1"
            score[other_player]["points"] = 0

        # Логика перевода геймов в сеты
        if score[player_key]["games"] >= 6:
            score[player_key]["sets"] += 1
            score[player_key]["games"] = 0
            score[other_player]["games"] = 0

        match.score = json.dumps(score)
        db.commit()

    @staticmethod
    def is_match_finished(match: Match) -> bool:
        """Проверка завершения матча"""
        score = json.loads(match.score)
        return "winner" in score

    @staticmethod
    def finish_match(match: Match, winner: Player) -> None:
        score = MatchService.get_score_data(match)
        score["winner"] = winner.id
        MatchService.set_score_data(match, score)

    @staticmethod
    def get_score_data(match: Match) -> dict:
        """Десериализация счёта из JSON-строки"""
        try:
            return json.loads(match.score) if match.score else {"sets": 0, "games": 0, "points": 0}
        except (TypeError, json.JSONDecodeError):
            return {"sets": 0, "games": 0, "points": 0}

    @staticmethod
    def set_score_data(match: Match, value: dict) -> None:
        """Сериализация счёта в JSON-строку"""
        match.score = json.dumps(value, ensure_ascii=False)

    @staticmethod
    def get_match_by_uuid(db: Session, uuid: str) -> Match:
        return db.query(Match).filter(Match.uuid == uuid).first()
