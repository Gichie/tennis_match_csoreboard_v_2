from views.base_view import BaseView
from views.template_name import TemplateName


class HomeView(BaseView):
    """
    A class for rendering the home page using Jinja2 templates.
    """

    def __init__(self):
        super().__init__()

    def render_home(self) -> str:
        return self.render_template(TemplateName.HOME_PAGE)
