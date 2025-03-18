import json
import logging
import uuid
from typing import Any

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from config.config import PER_PAGE
from exceptions import InvalidGameStateError, NotFoundMatchError, PlayerNumberError, DatabaseError
from models.match import Match
from models.player import Player
from services import score_utils
from services.score_utils import ScoreDict
from services.strategies.advantage_state_strategy import AdvantageStateStrategy
from services.strategies.deuce_state_strategy import DeuceStateStrategy
from services.strategies.regular_state_strategy import RegularStateStrategy
from services.strategies.tie_break_state_strategy import TieBreakStateStrategy
from services.validation import Validation, MIN_PAGE

logger = logging.getLogger(__name__)
STATE_STRATEGY = {
    'regular': RegularStateStrategy(),
    'deuce': DeuceStateStrategy(),
    'tie_break': TieBreakStateStrategy(),
    'advantage': AdvantageStateStrategy(),
}


class MatchService:
    """
    Provides services for managing matches.

    This class encapsulates the logic for creating, updating, and retrieving match data.
    """

    @staticmethod
    def create_match(db: Session, player1_id: int, player2_id: int) -> Match:
        """
        Creates a new match in the database.

        :param db: The SQLAlchemy session.
        :param player1_id: The ID of the first player.
        :param player2_id: The ID of the second player.
        :return: The newly created Match object.
        :raises DatabaseError: If a database error occurs during match creation.
        """
        try:
            new_match = Match(
                uuid=str(uuid.uuid4()),
                player1_id=player1_id,
                player2_id=player2_id
            )
            db.add(new_match)
            db.commit()
            db.refresh(new_match)
            logger.info(f"Match created successfully with UUID: {new_match.uuid}")
            return new_match
        except SQLAlchemyError as e:
            logger.error("Database error during match creation", exc_info=True)
            raise DatabaseError("Failed to create match") from e

    @staticmethod
    def add_point(db: Session, match: Match, score: ScoreDict, player_num: int) -> None:
        """
        Adds a point to the specified player's score and updates the game state.

        :param db: The SQLAlchemy session.
        :param match: The Match object representing the current match.
        :param score: A dictionary representing the current score of the match.
        :param player_num: The player number (1 or 2).
        :raises InvalidGameStateError: If the game state is unknown.
        """
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
            score_utils.reset_set(match, score, player_key)

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
        """
        Retrieves a match by its UUID.

        :param db: The SQLAlchemy session.
        :param uuid: The UUID of the match to retrieve.
        :return: The Match object with the specified UUID.
        :raises NotFoundMatchError: If a match with the given UUID is not found.
        """
        match = db.query(Match).filter(Match.uuid == uuid).first()
        if match:
            return match
        raise NotFoundMatchError(f"Match with uuid: {uuid} not found")

    @staticmethod
    def get_completed_matches(
            db: Session,
            page: int = MIN_PAGE,
            per_page: int = PER_PAGE,
            player_name: str | None = None
    ) -> tuple[list[Match], int, int]:
        """
        Retrieves a list of completed matches, with optional pagination and filtering by player name.

        :param db: The SQLAlchemy session.
        :param page: The page number to retrieve (defaults to MIN_PAGE).
        :param per_page: The number of matches to retrieve per page (defaults to PER_PAGE).
        :param player_name: The name of the player to filter by (optional).
        :return: A tuple containing the list of completed matches and the total number of completed matches.
        :raises DatabaseError: If a database error occurs during retrieval.
        """
        query = (
            db.query(Match)
            .options(
                joinedload(Match.player1),
                joinedload(Match.player2),
                joinedload(Match.winner)
            )
            .filter(Match.winner_id.isnot(None))
        )

        # Filter by player name
        if player_name:
            search_pattern = f'%{player_name}%'
            query = query.filter(
                or_(
                    Match.player1.has(Player.name.like(search_pattern)),
                    Match.player2.has(Player.name.like(search_pattern))
                )
            )

        # Pagination
        total = query.count()
        correct_page = Validation.correct_page(page, total, per_page)
        try:
            matches = (query.offset((correct_page - 1) * per_page).limit(per_page).all())
            return matches, total, correct_page
        except SQLAlchemyError as e:
            logger.error("Database error during getting list of completed matches", exc_info=True)
            raise DatabaseError("Failed to get completed matches") from e

    @staticmethod
    def determine_player_number(params: dict[Any, list[Any]]) -> int:
        """
        Returns the player number (1 or 2) based on parameters.

        Determines the player number (1 or 2) based on the presence of
        'player1_point' or 'player2_point' in the parameters.

        :param params: A dictionary of parameters.
        :return: The player number (1 or 2).
        :raises PlayerNumberError: If neither 'player1_point
        """

        if 'player1_point' in params:
            return 1
        elif 'player2_point' in params:
            return 2
        else:
            raise PlayerNumberError("Player number must be 1 or 2")
