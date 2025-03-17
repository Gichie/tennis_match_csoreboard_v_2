import logging
import os
from typing import Any, Callable

from whitenoise import WhiteNoise

from controllers.completed_matches_controller import CompletedMatchesController
from controllers.home_controller import HomeController
from controllers.match_controller import MatchController

logger = logging.getLogger(__name__)

home_controller = HomeController()
match_controller = MatchController()
completed_matches_controller = CompletedMatchesController()

routes = {
    "GET": {
        "/": home_controller.index,
        "/index": home_controller.index,
        "/new-match": match_controller.new_match_form,
        "/match-score": match_controller.match_score,
        '/matches': completed_matches_controller.list_completed_matches
    },
    "POST": {
        "/new-match": match_controller.create_match,
        "/match-score": match_controller.match_score
    }
}


def application(environ: dict[str, Any], start_response: Callable[[str, list[tuple[str, str]]], None]) -> Any:
    """
    WSGI application that handles routing and request processing.

    :param environ: A dictionary containing the WSGI environment variables.
    :param start_response: A callable used to begin the HTTP response.
    :return: A list of bytes representing the response body.
    """
    try:
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', 'GET').upper()
        logger.info(f"Received request: {method} {path}")

        handler = routes.get(method, {}).get(path)
        if handler:
            return handler(environ, start_response)
        else:
            logger.warning(f"404 Not Found: {method} {path}")
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"404 Not Found"]
    except Exception as e:
        logger.error("500 Internal Server Error", exc_info=True)
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return [f"Error: {str(e)}".encode("utf-8")]


# Path to static files
static_path = os.path.join(os.path.dirname(__file__), 'static')
app_with_static = WhiteNoise(application, root=static_path, prefix='/static')
