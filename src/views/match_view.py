import os
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

logger = logging.getLogger(__name__)


class MatchView:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        loader = FileSystemLoader(searchpath=template_path, encoding='utf-8')

        self.env = Environment(loader=loader, autoescape=True)
        self.env.filters['tennis_points'] = lambda x: {0: '0', 1: '15', 2: '30', 3: '40'}.get(x, '40')
        self.env.filters['tie_break_points'] = lambda x: f'{x}'

    def render_new_match_form(self, player1_name='', player2_name='', errors=None):
        try:
            template = self.env.get_template('new_match.html')
            return template.render(player1_name=player1_name, player2_name=player2_name, errors=errors or {})
        except TemplateNotFound:
            logger.error("Template not found: new_match.html")
            return "Error rendering template"

    def render_match_score(self, context):
        try:
            template = self.env.get_template('match_score.html')
            return template.render(**context)  # Явное кодирование
        except TemplateNotFound:
            logger.error("Template not found: match_score.html")
            return "Error rendering template"

    def render_final_score(self, context):
        try:
            template = self.env.get_template('final_score.html')
            return template.render(**context)
        except TemplateNotFound:
            logger.error("Template not found: final_score.html")
            return "Error rendering template"

    def render_error_page(self, context):
        try:
            template = self.env.get_template('error.html')
            return template.render(**context)
        except TemplateNotFound:
            logger.error("Template not found: error.html")
            return "Error rendering template"
