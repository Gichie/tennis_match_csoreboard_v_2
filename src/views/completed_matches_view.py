from views.base_view import BaseView
from views.template_name import TemplateName


class CompletedMatchesView(BaseView):
    """
    A class responsible for rendering the completed matches view using Jinja2 templates.
    """

    def __init__(self) -> None:
        """
        Initializes the CompletedMatchesView by setting up the Jinja2 environment.
        """
        super().__init__()

    def render_completed_matches(self, context: dict[str, int | str | list[dict[str, str]]]) -> str:
        return self.render_template(TemplateName.COMPLETED_MATCHES, context)
