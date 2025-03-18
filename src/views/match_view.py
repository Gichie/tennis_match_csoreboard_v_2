import logging
from enum import Enum

from views.base_view import BaseView
from views.template_name import TemplateName

logger = logging.getLogger(__name__)


class TennisPoint(Enum):
    LOVE = 0
    FIFTEEN = 15
    THIRTY = 30
    FORTY = 40


class MatchView(BaseView):
    """
    A class responsible for rendering various match-related views using Jinja2 templates,
    including new match forms, match scores, final scores, and error pages.
    """

    def __init__(self) -> None:
        super().__init__()
        self.env.filters['tennis_points'] = lambda x: {
            0: f'{TennisPoint.LOVE.value}',
            1: f'{TennisPoint.FIFTEEN.value}',
            2: f'{TennisPoint.THIRTY.value}',
            3: f'{TennisPoint.FORTY.value}'
        }.get(x, f'{TennisPoint.FORTY.value}')
        self.env.filters['tie_break_points'] = lambda x: f'{x}'

    def render_new_match_form(
            self,
            player1_name: str = '',
            player2_name: str = '',
            errors: dict[str, str] | None = None
    ) -> str:
        context = {'player1_name': player1_name, 'player2_name': player2_name, 'errors': errors or {}}
        return self.render_template(TemplateName.NEW_MATCH_FORM, context)

    def render_match_score(self, context: dict[str, str]) -> str:
        return self.render_template(TemplateName.MATCH_SCORE, context)

    def render_final_score(self, context: dict[str, str]) -> str:
        return self.render_template(TemplateName.FINAL_SCORE, context)
