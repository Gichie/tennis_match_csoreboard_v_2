import json
import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from src.models.match import Match
from src.services import score_utils
from src.services.strategies.advantage_state_strategy import AdvantageStateStrategy
from src.services.strategies.deuce_state_strategy import DeuceStateStrategy
from src.services.strategies.regular_state_strategy import RegularStateStrategy
from src.services.strategies.tie_break_state_strategy import TieBreakStateStrategy


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
                player_num
            )
        else:
            raise ValueError(f"Неизвестное состояние игры: {match.current_game_state}")

        if score_utils.is_set_finished(score, player_key, opponent_key):
            score_utils.reset_set(score, player_key)
            match.current_game_state = 'regular'
        elif score_utils.is_tie_break(score, player_key, opponent_key):
            match.current_game_state = 'tie_break'

        if score_utils.is_match_finished(score):
            if player_num == 1:
                match.winner_id = match.player1_id
            else:
                match.winner_id = match.player2_id
            match.current_game_state = 'finished'

        match.score = json.dumps(score)
        db.commit()

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
