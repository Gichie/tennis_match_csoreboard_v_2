import json
import uuid

import pytest

from src.models.match import Match


@pytest.fixture
def match():
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
