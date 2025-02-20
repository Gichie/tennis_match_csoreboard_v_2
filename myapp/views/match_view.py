from jinja2 import Environment, FileSystemLoader
import os


class MatchView:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        loader = FileSystemLoader(
            searchpath=template_path,
            encoding='utf-8'  # Кодировка задаётся здесь
        )

        self.env = Environment(
            loader=loader,
            autoescape=True  # Включаем автоэкранирование
        )

    def render_new_match_form(self):
        template = self.env.get_template('new_match.html')
        return template.render()

    def render_match_score(self, context):
        template = self.env.get_template('match_score.html')
        return template.render(**context)  # Явное кодирование
