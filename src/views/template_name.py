from enum import Enum


class TemplateName(Enum):
    NEW_MATCH_FORM = 'new_match.html'
    MATCH_SCORE = 'match_score.html'
    FINAL_SCORE = 'final_score.html'
    ERROR_PAGE = 'error.html'
    COMPLETED_MATCHES = 'completed_matches.html'
    HOME_PAGE = 'home.html'
