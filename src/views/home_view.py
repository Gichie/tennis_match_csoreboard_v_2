import os

from jinja2 import Environment, FileSystemLoader

from views.template_name import TemplateName


class HomeView:
    """
    A class for rendering the home page using Jinja2 templates.
    """

    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        self.env = Environment(loader=FileSystemLoader(template_path))

    def render_home(self) -> str:
        template = self.env.get_template(TemplateName.HOME_PAGE.value)
        return template.render()
