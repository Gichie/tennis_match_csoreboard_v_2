import logging
import os

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from views.template_name import TemplateName

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

    def render_template(self, template_name: TemplateName, context: dict) -> str:
        """
        Renders a template based on the given TemplateName enum.

        :param template_name: The TemplateName enum member representing the template to render.
        :param context: A dictionary containing the data to be passed to the template.
        :return: A string containing the rendered HTML, or an error message if the template is not found.
        """
        try:
            template = self.env.get_template(template_name.value)  # Access the string value of the enum
            return template.render(**context)
        except TemplateNotFound:
            logger.error(f"Template not found: {template_name.value}")
            return "Error rendering template"

    def render_new_match_form(self, player1_name: str = '', player2_name: str = '', errors: dict | None = None) -> str:
        context = {'player1_name': player1_name, 'player2_name': player2_name, 'errors': errors or {}}
        return self.render_template(TemplateName.NEW_MATCH_FORM, context)

    def render_match_score(self, context: dict) -> str:
        return self.render_template(TemplateName.MATCH_SCORE, context)

    def render_final_score(self, context: dict) -> str:
        return self.render_template(TemplateName.FINAL_SCORE, context)

    def render_error_page(self, context: dict) -> str:
        return self.render_template(TemplateName.ERROR_PAGE, context)
