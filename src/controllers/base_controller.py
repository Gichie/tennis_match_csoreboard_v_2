from typing import Callable

from views.match_view import MatchView


class BaseController:
    """
    BaseController class for handling common operations and error handling in the application.
    """

    def __init__(self) -> None:
        self.view: MatchView = MatchView()

    def _handle_error(
            self,
            start_response: Callable[[str, list[tuple[str, str]]], None],
            exception: Exception,
            match_uuid: str | None = None,
            status: str = '500 Internal Server Error'
    ) -> list[bytes]:
        """
        Handle errors and return a rendered error page.

        :param start_response: Callable to start the response with status and headers.
        :param exception: The exception that occurred.
        :param match_uuid: Optional UUID of the match related to the error.
        :param status: HTTP status code for the error response.

        :return: A list containing the encoded response body.
        """
        error_message = str(exception)
        error_title = type(exception).__name__

        response_body: str = self.view.render_error_page({
            "error_title": error_title,
            "error_message": error_message,
            "match_uuid": match_uuid
        })

        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]
