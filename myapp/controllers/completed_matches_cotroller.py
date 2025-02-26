from myapp.database.session import get_db
from myapp.services.match_service import MatchService
from myapp.views.completed_matches_view import CompletedMatchesView


class CompletedMatchesController:
    def __init__(self):
        self.view = CompletedMatchesView()

    def list_completed_matches(self, environ, start_response):
        with get_db() as db:
            completed_matches = MatchService.get_completed_matches(db)
            context = {"matches": completed_matches}
            response_body = self.view.render_completed_matches(context)
            headers = [("Content-Type", "text/html; charset=utf-8")]
            start_response("200 OK", headers)
            return [response_body.encode("utf-8")]
