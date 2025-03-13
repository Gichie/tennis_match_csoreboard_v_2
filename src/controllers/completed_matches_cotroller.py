import logging
import math
from urllib.parse import parse_qs

from src.controllers.base_controller import BaseController
from src.database.session import get_db
from src.services.exceptions import DatabaseError
from src.services.match_service import MatchService
from src.views.completed_matches_view import CompletedMatchesView

logger = logging.getLogger(__name__)
PER_PAGE = 10  # Количество матчей на странице


class CompletedMatchesController(BaseController):
    def __init__(self):
        self.view = CompletedMatchesView()

    def list_completed_matches(self, environ, start_response):
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
                    "total_pages": math.ceil(total / PER_PAGE),
                    "player_name": player_name
                }

                response_body = self.view.render_completed_matches(context)
                headers = [("Content-Type", "text/html; charset=utf-8")]
                start_response("200 OK", headers)
                return [response_body.encode("utf-8")]

        except DatabaseError as e:
            return self._handle_error(start_response, e)
        except Exception as e:
            logger.critical("Unexpected error while loading completed matches", exc_info=True)
            return self._handle_error(start_response, e)

    def _prepare_matches_data(self, matches):
        return [
            {
                "player1": match.player1.name,
                "player2": match.player2.name,
                "winner": match.winner.name
            }
            for match in matches
        ]
