import logging
import os

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

logger = logging.getLogger(__name__)


class MatchView:
    """
    A class responsible for rendering various match-related views using Jinja2 templates,
    including new match forms, match scores, final scores, and error pages.
    """

    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        loader = FileSystemLoader(searchpath=template_path, encoding='utf-8')

        self.env = Environment(loader=loader, autoescape=True)
        self.env.filters['tennis_points'] = lambda x: {0: '0', 1: '15', 2: '30', 3: '40'}.get(x, '40')
        self.env.filters['tie_break_points'] = lambda x: f'{x}'

    def render_new_match_form(self, player1_name: str = '', player2_name: str = '', errors: dict | None = None) -> str:
        """
        Renders the form for creating a new match.

        :param player1_name: The name of the first player.  Defaults to ''.
        :param player2_name: The name of the second player. Defaults to ''.
        :param errors: A dictionary containing error messages. Defaults to None (empty dictionary).
        :return: A string containing the rendered HTML of the new match form, or an error message if the template is not found.
        """
        try:
            template = self.env.get_template('new_match.html')
            return template.render(player1_name=player1_name, player2_name=player2_name, errors=errors or {})
        except TemplateNotFound:
            logger.error("Template not found: new_match.html")
            return "Error rendering template"

    def render_match_score(self, context: dict) -> str:
        """
        Renders the current score of a match.

        :param context: A dictionary containing the data to be passed to the template, such as player names and scores.
        :return: A string containing the rendered HTML of the match score, or an error message if the template is not found.
        """
        try:
            template = self.env.get_template('match_score.html')
            return template.render(**context)
        except TemplateNotFound:
            logger.error("Template not found: match_score.html")
            return "Error rendering template"

    def render_final_score(self, context: dict) -> str:
        """
        Renders the final score of a match.

        :param context: A dictionary containing the data to be passed to the template, such as the winning player and the final score.
        :return: A string containing the rendered HTML of the final score, or an error message if the template is not found.
        """
        try:
            template = self.env.get_template('final_score.html')
            return template.render(**context)
        except TemplateNotFound:
            logger.error("Template not found: final_score.html")
            return "Error rendering template"

    def render_error_page(self, context: dict) -> str:
        """
        Renders an error page.

        :param context: A dictionary containing the data to be passed to the template, such as the error message.
        :return: A string containing the rendered HTML of the error page, or an error message if the template is not found.
        """
        try:
            template = self.env.get_template('error.html')
            return template.render(**context)
        except TemplateNotFound:
            logger.error("Template not found: error.html")
            return "Error rendering template"
