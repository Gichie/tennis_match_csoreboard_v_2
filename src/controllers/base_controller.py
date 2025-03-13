from src.views.match_view import MatchView


class BaseController:
    def __init__(self):
        self.view = MatchView()

    def _handle_error(self, start_response, exception, match_uuid=None, status='500 Internal Server Error'):
        error_message = str(exception)
        error_title = type(exception).__name__

        response_body = self.view.render_error_page({
            "error_title": error_title,
            "error_message": error_message,
            "match_uuid": match_uuid
        })

        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]
