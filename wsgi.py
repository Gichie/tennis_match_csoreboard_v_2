import os

from whitenoise import WhiteNoise

from src.controllers.home_controller import HomeController
from src.controllers.match_controller import MatchController
from src.controllers.completed_matches_cotroller import CompletedMatchesController


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


def application(environ, start_response):
    try:
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', 'GET').upper()

        handler = routes.get(method, {}).get(path)
        if handler:
            return handler(environ, start_response)
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"404 Not Found"]
    except Exception as e:
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return [f"Error: {str(e)}".encode("utf-8")]


# Путь к статическим файлам
static_path = os.path.join(os.path.dirname(__file__), 'src/static')
app_with_static = WhiteNoise(application, root=static_path, prefix='/static')
