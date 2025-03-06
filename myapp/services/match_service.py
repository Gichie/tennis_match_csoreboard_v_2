import json
import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from myapp.models.match import Match
from myapp.services.strategies.advantage_state_strategy import AdvantageStateStrategy
from myapp.services.strategies.deuce_state_strategy import DeuceStateStrategy
from myapp.services.strategies.regular_state_strategy import RegularStateStrategy
from myapp.services.strategies.tie_break_state_strategy import TieBreakStateStrategy

MIN_POINTS = 3
MIN_GAMES = 3
MIN_SETS = 2
SCORE_DIFF = 2
STATE_STRATEGY = {
    'regular': RegularStateStrategy(),
    'deuce': DeuceStateStrategy(),
    'tie_break': TieBreakStateStrategy(),
    'advantage': AdvantageStateStrategy()
}


class MatchService:
    @staticmethod
    def create_match(db: Session, player1_id: int, player2_id: int) -> Match:
        new_match = Match(
            uuid=str(uuid.uuid4()),
            player1_id=player1_id,
            player2_id=player2_id
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return new_match

    @staticmethod
    def add_point(db: Session, match: Match, score: dict, player_num: int) -> None:
        player_key = f"player{player_num}"
        opponent_key = "player2" if player_num == 1 else "player1"

        if match.current_game_state.startswith('advantage'):
            strategy = STATE_STRATEGY['advantage']
        else:
            strategy = STATE_STRATEGY.get(match.current_game_state)

        if strategy:
            strategy.add_point(
                match,
                score,
                player_key,
                opponent_key,
                player_num,
                reset_game_func=MatchService._reset_game,
                reset_set_func=MatchService._reset_set,
                process_tie_break_func=MatchService.process_tie_break
            )
        else:
            raise ValueError(f"Неизвестное состояние игры: {match.current_game_state}")

        if MatchService.is_set_finished(score, player_key, opponent_key):
            MatchService._reset_set(score, player_key)
            match.current_game_state = 'regular'
        elif MatchService.is_tie_break(score, player_key, opponent_key):
            match.current_game_state = 'tie_break'

        if MatchService.is_match_finished(score):
            if player_num == 1:
                match.winner_id = match.player1_id
            else:
                match.winner_id = match.player2_id
            match.current_game_state = 'finished'

        match.score = json.dumps(score)
        db.commit()

    @staticmethod
    def process_tie_break(score: dict, player_key: str, opponent_key: str) -> None:
        score[player_key]['points'] += 1
        if (score[player_key]['points'] >= 7 and
                (score[player_key]['points'] - score[opponent_key]['points']) >= SCORE_DIFF):
            MatchService._reset_set(score, player_key)

    @staticmethod
    def _reset_game(score: dict, winner_key: str) -> None:
        score[winner_key]["games"] += 1
        score[winner_key]["points"] = 0
        opponent_key = "player2" if winner_key == "player1" else "player1"
        score[opponent_key]["points"] = 0

    @staticmethod
    def _reset_set(score: dict, winner_key: str) -> None:
        score[winner_key]["sets"] += 1
        score[winner_key]["games"] = 0
        opponent_key = "player2" if winner_key == "player1" else "player1"
        score[opponent_key]["games"] = 0
        score[winner_key]["points"] = 0
        score[opponent_key]["points"] = 0

    @staticmethod
    def is_tie_break(score: dict, player_key: str, opponent_key: str) -> bool:
        return score[player_key]["games"] == MIN_GAMES and score[opponent_key]["games"] == MIN_GAMES

    @staticmethod
    def is_match_finished(score) -> bool:
        return score["player1"]["sets"] == MIN_SETS or score["player2"]["sets"] == MIN_SETS

    @staticmethod
    def is_set_finished(score: dict, player_key: str, opponent_key: str) -> bool:
        return (
                score[player_key]["games"] >= MIN_GAMES and
                abs(score[player_key]["games"] - score[opponent_key]["games"]) >= SCORE_DIFF
        )

    @staticmethod
    def get_match_by_uuid(db: Session, uuid: str) -> Match:
        return db.query(Match).filter(Match.uuid == uuid).first()

    @staticmethod
    def get_completed_matches(
            db: Session,
            page: int = 1,
            per_page: int = 10,
            player_name: str | None = None
    ) -> tuple[list[Match], int]:
        query = (
            db.query(Match)
            .options(
                joinedload(Match.player1),
                joinedload(Match.player2),
                joinedload(Match.winner)
            )
            .filter(Match.winner_id.isnot(None))
        )

        # Фильтр по имени игрока
        if player_name:
            query = query.filter(or_(Match.player1.has(name=player_name), Match.player2.has(name=player_name)))

        # Пагинация
        total = query.count()
        matches = (query.offset((page - 1) * per_page).limit(per_page).all())

        return matches, total
