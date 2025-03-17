
import logging
from math import ceil
from typing import Callable, Any
from urllib.parse import parse_qs

from controllers.base_controller import BaseController
from database.session import get_db
from exceptions import DatabaseError
from models.match import Match
from services.match_service import MatchService
from views.completed_matches_view import CompletedMatchesView

logger = logging.getLogger(__name__)
PER_PAGE = 10  # Number of matches per page


class CompletedMatchesController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.view: CompletedMatchesView = CompletedMatchesView()

    def list_completed_matches(
            self,
            environ: dict[str, Any],
            start_response: Callable[[str, list[tuple[str, str]]], None]
    ) -> list[bytes]:
        """
        Get a list of completed matches with pagination and filtering.

        :param environ: Dictionary with request environment variables (WSGI)
        :param start_response: Function to set HTTP status and headers
        :return: Response as a list of bytes
        """
        query = parse_qs(environ.get("QUERY_STRING", ''))
        page = int(query.get('page', ['1'])[0])
        player_name = query.get('filter_by_player_name', [None])[0]
        try:
            with get_db() as db:
                matches, total, correct_page = MatchService.get_completed_matches(
                    db,
                    page=page,
                    per_page=PER_PAGE,
                    player_name=player_name
                )
                logger.info(f"Loaded {len(matches)} matches for page {correct_page}")

                context = {
                    "matches": self._prepare_matches_data(matches),
                    "current_page": correct_page,
                    "total_pages": ceil(total / PER_PAGE),
                    "player_name": player_name
                }
                response_body = self.view.render_completed_matches(context)
                headers = [("Content-Type", "text/html; charset=utf-8")]
                start_response("200 OK", headers)
                return [response_body.encode("utf-8")]

        except DatabaseError as e:
            result: list[bytes] = self._handle_error(start_response, e)
            return result
        except Exception as e:
            logger.critical("Unexpected error while loading completed matches", exc_info=True)
            result_exc: list[bytes] = self._handle_error(start_response, e)
            return result_exc

    def _prepare_matches_data(self, matches: list[Match]) -> list[dict[str, str]]:
        """
        Convert raw match data into a format that is easy to display.

        :param matches: List of match objects from the DB
        :return: List of dictionaries with match data
        """
        return [
            {
                "player1": match.player1.name,
                "player2": match.player2.name,
                "winner": match.winner.name
            }
            for match in matches
        ]
