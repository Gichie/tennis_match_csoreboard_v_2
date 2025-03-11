import json
import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from src.models.match import Match
from src.models.player import Player
from src.services import score_utils
from src.services.exceptions import InvalidGameStateError, NotFoundMatchError, PlayerNumberError
from src.services.strategies.advantage_state_strategy import AdvantageStateStrategy
from src.services.strategies.deuce_state_strategy import DeuceStateStrategy
from src.services.strategies.regular_state_strategy import RegularStateStrategy
from src.services.strategies.tie_break_state_strategy import TieBreakStateStrategy
from src.services.validation import Validation, MIN_PAGE

STATE_STRATEGY = {
    'regular': RegularStateStrategy(),
    'deuce': DeuceStateStrategy(),
    'tie_break': TieBreakStateStrategy(),
    'advantage': AdvantageStateStrategy(),
}

PER_PAGE = 10


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
            raise InvalidGameStateError(f"Unknown game state: {match.current_game_state}")

        if score_utils.is_set_finished(score, player_key, opponent_key):
            score_utils.reset_set(score, player_key)

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
        match = db.query(Match).filter(Match.uuid == uuid).first()
        if match:
            return match
        raise NotFoundMatchError(uuid)

    @staticmethod
    def get_completed_matches(
            db: Session,
            page: int = MIN_PAGE,
            per_page: int = PER_PAGE,
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
            search_pattern = f'%{player_name}%'
            query = query.filter(
                or_(
                    Match.player1.has(Player.name.like(search_pattern)),
                    Match.player2.has(Player.name.like(search_pattern))
                )
            )

        # Пагинация
        total = query.count()
        correct_page = Validation.correct_page(page, total, per_page)
        matches = (query.offset((correct_page - 1) * per_page).limit(per_page).all())

        return matches, total, correct_page

    @staticmethod
    def determine_player_number(params: dict):
        if 'player1_point' in params:
            return 1
        elif 'player2_point' in params:
            return 2
        else:
            raise PlayerNumberError("Player number must be 1 or 2")
