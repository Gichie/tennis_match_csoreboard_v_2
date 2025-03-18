"""
Controller module for managing matches: creating, displaying and updating results.
"""
import json
import logging
from typing import Callable, Any
from urllib.parse import parse_qs

from sqlalchemy.orm import Session

from controllers.base_controller import BaseController
from database.session import get_db
from exceptions import (
    NotFoundMatchError,
    InvalidGameStateError,
    PlayerNumberError,
    InvalidScoreError,
    DatabaseError,
    PlayerNotFound
)
from models.match import Match
from services import score_utils
from services.match_service import MatchService
from services.player_service import PlayerService
from services.validation import Validation
from utils.request_utils import parse_form_data

logger = logging.getLogger(__name__)


class MatchController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def new_match_form(
            self,
            environ: dict[str, Any],
            start_response: Callable[[str, list[tuple[str, str]]], None]
    ) -> list[bytes]:
        """
        Display the form for creating a match

        :param environ: Dictionary with WSGI request data
        :param start_response: Function to set HTTP status and headers
        :return: Response as a list of bytes
        """
        response_body = self.view.render_new_match_form()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    def create_match(
            self,
            environ: dict[str, Any],
            start_response: Callable[[str, list[tuple[str, str]]], None]
    ) -> list[bytes]:
        """
        Creates a new match based on the form data.

        :param environ: Dictionary with WSGI request data
        :param start_response: Function to set HTTP status and headers
        :return: Response as a list of bytes
        """
        try:
            params = parse_form_data(environ)

            player1_name = params.get('player1', '').strip()
            player2_name = params.get('player2', '').strip()
            validation_errors = Validation.player_names(player1_name, player2_name)

            if validation_errors:
                response_body = self.view.render_new_match_form(
                    player1_name=player1_name,
                    player2_name=player2_name,
                    errors=validation_errors
                )
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [response_body.encode('utf-8')]

            with get_db() as db:
                player1_id = PlayerService.get_or_create_player_id(db, player1_name)
                player2_id = PlayerService.get_or_create_player_id(db, player2_name)
                new_match = MatchService.create_match(db, player1_id, player2_id)

                db.add(new_match)
                db.commit()
                db.refresh(new_match)

                headers = [
                    ('Location', f'/match-score?uuid={new_match.uuid}'),
                    ('Content-Type', 'text/plain')
                ]
                start_response('302 Found', headers)
                return [b'Redirecting...']

        except DatabaseError as e:
            return self._handle_error(start_response, e)
        except Exception as e:
            logger.critical("Unexpected error during match creation", exc_info=True)
            return self._handle_error(start_response, e)

    def match_score(
            self,
            environ: dict[str, Any],
            start_response: Callable[[str, list[tuple[str, str]]], None]
    ) -> list[bytes]:
        """
        Displays the current score of the match or handles updates.

        :param environ: Dictionary with WSGI request data
        :param start_response: Function to set HTTP status and headers
        :return: Response as a list of bytes
        """
        query = parse_qs(environ.get('QUERY_STRING', ''))
        match_uuid = query.get('uuid', [''])[0]

        try:
            with get_db() as db:
                match = MatchService.get_match_by_uuid(db, match_uuid)

                try:
                    score = json.loads(match.score)
                except json.JSONDecodeError:
                    raise InvalidScoreError("Score data is corrupted")
                if environ['REQUEST_METHOD'] == 'POST':
                    return self._handle_score_update(environ, start_response, match, score, db)

                return self._render_score_page(start_response, match, score, db)

        except NotFoundMatchError as e:
            logger.warning('Match not found')
            return self._handle_error(start_response, e, status='404 Not Found')
        except InvalidScoreError as e:
            return self._handle_error(start_response, e, status='400 Bad Request')
        except Exception as e:
            logger.critical("Unexpected error during match scoring", exc_info=True)
            return self._handle_error(start_response, e)

    def _handle_score_update(
            self,
            environ: dict[str, Any],
            start_response: Callable[[str, list[tuple[str, str]]], None],
            match: Match,
            score: dict[str, dict[str, int]],
            db: Session
    ) -> list[bytes]:
        """
        Handles updating the match score.

        :param environ: Dictionary with WSGI request data
        :param start_response: Function to set HTTP status and headers
        :param match: Match object from the database
        :param score: Current score as a dictionary
        :param db: Database session
        :return: Response as a list of bytes
        """
        try:
            params = parse_form_data(environ)

            player_num = MatchService.determine_player_number(params)
            MatchService.add_point(db, match, score, player_num)

            if score_utils.is_match_finished(score):
                return self._render_final_score(start_response, match, db)

            return self._render_score_page(start_response, match, score, db)

        except (InvalidGameStateError, PlayerNumberError) as e:
            logger.warning(f"Invalid operation for match {match.uuid}")
            return self._handle_error(start_response, e, match.uuid, status='400 Bad Request')
        except Exception as e:
            logger.critical('Unexpected error while updating match score', exc_info=True)
            return self._handle_error(start_response, e, match.uuid)

    def _render_score_page(
            self,
            start_response: Callable[[str, list[tuple[str, str]]], None],
            match: Match,
            score: dict[str, dict[str, int]],
            db: Session
    ) -> list[bytes]:
        """
        Generates a page with the current match score.

        :param start_response: Function for setting HTTP status and headers
        :param match: Match object from the DB
        :param score: Current score as a dictionary
        :return: Response as a list of bytes
        """
        try:
            context = {
                "uuid": match.uuid,
                "player1": PlayerService.get_name(db, match.player1_id),
                "player2": PlayerService.get_name(db, match.player2_id),
                "player1_points": score["player1"]["points"],
                "player1_games": score["player1"]["games"],
                "player1_sets": score["player1"]["sets"],
                "player2_points": score["player2"]["points"],
                "player2_games": score["player2"]["games"],
                "player2_sets": score["player2"]["sets"],
                "finished": False,
                "current_game_state": match.current_game_state
            }

            response_body = self.view.render_match_score(context)
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response('200 OK', headers)
            return [response_body.encode('utf-8')]  # Обязательное кодирование
        except PlayerNotFound as e:
            return self._handle_error(start_response, e, status='404 Not Found')
        except Exception as e:
            logger.critical('Unexpected error while rendering match score', exc_info=True)
            return self._handle_error(start_response, e)

    def _render_final_score(
            self,
            start_response: Callable[[str, list[tuple[str, str]]], None],
            match: Match,
            db: Session
    ) -> list[bytes]:
        """
        Generates a page with the final result of the match.

        :param start_response: Function for setting the HTTP status and headers
        :param match: Match object from the DB
        :return: Response as a list of bytes
        """
        try:
            context = {
                "player1": PlayerService.get_name(db, match.player1_id),
                "player2": PlayerService.get_name(db, match.player2_id),
                "winner": PlayerService.get_name(db, match.winner_id),
                "player1_sets": json.loads(match.score)["player1"]["sets"],
                "player2_sets": json.loads(match.score)["player2"]["sets"],
            }
            response_body = self.view.render_final_score(context)
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response('200 OK', headers)
            return [response_body.encode('utf-8')]

        except PlayerNotFound as e:
            return self._handle_error(start_response, e, status='404 Not Found')
        except Exception as e:
            logger.critical('Unexpected error while rendering final match score', exc_info=True)
            return self._handle_error(start_response, e)
