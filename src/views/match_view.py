import logging

from views.base_view import BaseView
from views.template_name import TemplateName

logger = logging.getLogger(__name__)


class MatchView(BaseView):
    """
    A class responsible for rendering various match-related views using Jinja2 templates,
    including new match forms, match scores, final scores, and error pages.
    """

    def __init__(self) -> None:
        super().__init__()
        self.env.filters['tennis_points'] = lambda x: {0: '0', 1: '15', 2: '30', 3: '40'}.get(x, '40')
        self.env.filters['tie_break_points'] = lambda x: f'{x}'

    def render_new_match_form(
            self,
            player1_name: str = '',
            player2_name: str = '',
            errors: dict[str, str] | None = None
    ) -> str:
        context = {'player1_name': player1_name, 'player2_name': player2_name, 'errors': errors or {}}
        result: str = self.render_template(TemplateName.NEW_MATCH_FORM, context)
        return result

    def render_match_score(self, context: dict[str, str]) -> str:
        result: str = self.render_template(TemplateName.MATCH_SCORE, context)
        return result

    def render_final_score(self, context: dict[str, str]) -> str:
        result: str = self.render_template(TemplateName.FINAL_SCORE, context)
        return result
