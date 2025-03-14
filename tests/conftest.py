import json
import uuid

import pytest

from models.match import Match


@pytest.fixture
def match() -> Match:
    """
    Fixture that creates and returns a sample `Match` object.
    """
    return Match(
        uuid=str(uuid.uuid4()),
        player1_id=1,
        player2_id=2,
        score=json.dumps({
            "player1": {"sets": 0, "games": 0, "points": 0},
            "player2": {"sets": 0, "games": 0, "points": 0}
        }),
        current_game_state='regular'
    )


def setup_score(match: Match, initial_score: dict):
    """
    Sets up the score for a match based on the given initial score.

    :param match: The `Match` object to set up the score for.
    :param initial_score: A dictionary representing the initial score for the players.
                          Example: {"player1": {"points": 1, "games": 2}, "player2": {"sets": 1}}
    :return: A dictionary representing the updated score.
    """
    score = json.loads(match.score)
    for player in ["player1", "player2"]:
        if player in initial_score:
            for key in ["points", "games", "sets"]:
                if key in initial_score[player]:
                    score[player][key] = initial_score[player][key]
    return score
