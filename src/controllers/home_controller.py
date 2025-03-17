"""
Module containing the Home Controller for rendering the main page.
"""
from typing import Callable, Any

from views.home_view import HomeView


class HomeController:
    """
    Controller for managing the home page.
    """

    def __init__(self) -> None:
        self.view = HomeView()

    def index(
            self,
            environ: dict[str, Any],
            start_response: Callable[[str, list[tuple[str, str]]], None]
    ) -> list[bytes]:
        """
        Handle incoming HTTP requests for the home page.

        :param environ: WSGI environment dictionary containing request data
        :param start_response: WSGI response starter function
        :return: Encoded HTML content of the home page
        """
        response_body = self.view.render_home()
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]
