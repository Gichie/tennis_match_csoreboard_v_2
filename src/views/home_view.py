import os

from jinja2 import Environment, FileSystemLoader


class HomeView:
    """
    A class for rendering the home page using Jinja2 templates.
    """

    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        self.env = Environment(loader=FileSystemLoader(template_path))

    def render_home(self) -> str:
        """
        Renders the home page HTML.

        :return: A string containing the rendered HTML for the home page.
        """
        template = self.env.get_template('home.html')
        return template.render()
