import json
import uuid

from sqlalchemy.orm import Session

from myapp.models.match import Match
from myapp.models.player import Player


class MatchService:
    @staticmethod
    def create_match(db: Session, player1: Player, player2: Player) -> Match:
        new_match = Match(
            uuid=str(uuid.uuid4()),
            score=json.dumps({"sets": [], "current_game": [0, 0]}),
            player1_id=player1.id,
            player2_id=player2.id
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return new_match

    @staticmethod
    def add_point(db: Session, match: Match, player_num: int) -> None:
        """Добавление очка игроку с полной логикой подсчета"""
        score = json.loads(match.score)

        # Обновляем текущий гейм
        score["current_game"][player_num - 1] += 1
        p1_score, p2_score = score["current_game"]

        # Проверка на выигрыш гейма
        if (p1_score >= 4 or p2_score >= 4) and abs(p1_score - p2_score) >= 2:
            score["sets"].append(score["current_game"].copy())
            score["current_game"] = [0, 0]

            # Проверка на выигрыш матча
            if len(score["sets"]) >= 3:
                score["winner"] = player_num

        match.score = json.dumps(score)
        db.commit()
        db.refresh(match)

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
            return json.loads(match.score) if match.score else {"sets": []}
        except (TypeError, json.JSONDecodeError):
            return {"sets": []}

    @staticmethod
    def set_score_data(match: Match, value: dict) -> None:
        """Сериализация счёта в JSON-строку"""
        match.score = json.dumps(value, ensure_ascii=False)

    @staticmethod
    def get_match_by_uuid(db: Session, uuid: str) -> Match:
        return db.query(Match).filter(Match.uuid == uuid).first()
