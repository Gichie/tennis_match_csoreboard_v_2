import os

from jinja2 import Environment, FileSystemLoader


class CompletedMatchesView:
    """
    A class responsible for rendering the completed matches view using Jinja2 templates.
    """

    def __init__(self):
        """
        Initializes the CompletedMatchesView by setting up the Jinja2 environment.
        """
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        loader = FileSystemLoader(searchpath=template_path, encoding='utf-8')

        self.env = Environment(loader=loader, autoescape=True)

    def render_completed_matches(self, context: dict) -> str:
        """
        Renders the completed matches HTML page using the provided context.

        :param context: A dictionary containing the data to be passed to the template.
        :return: A string containing the rendered HTML.
        """
        template = self.env.get_template('completed_matches.html')
        return template.render(**context)
