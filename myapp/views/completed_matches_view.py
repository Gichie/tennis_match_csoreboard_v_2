import os

from jinja2 import Environment, FileSystemLoader


class CompletedMatchesView:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        loader = FileSystemLoader(searchpath=template_path, encoding='utf-8')

        self.env = Environment(loader=loader, autoescape=True)

    def render_completed_matches(self, context):
        template = self.env.get_template('completed_matches.html')
        return template.render(**context)
