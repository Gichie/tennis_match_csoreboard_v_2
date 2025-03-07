import json
import uuid

import pytest

from src.models.match import Match
from src.services.strategies.regular_state_strategy import RegularStateStrategy


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


class TestRegularStateStrategy:
    @pytest.mark.parametrize(
        "initial_dcore, "
        "player_key, "
        "expected_state, "
        "expected_points_player1, "
        "expected_points_player2, "
        "expected_games_player1, "
        "expected_games_player2",
        [
            # Тест 1: Переход в deuce (3-3) после добавления очка player1
            ({"player1": {"points": 2}, "player2": {"points": 3}}, "player1", "deuce", 3, 3, 0, 0),
            # Тест 2: Выигрыш игры (4-1) после добавления очка player1
            ({"player1": {"points": 3}, "player2": {"points": 1}}, "player1", "regular", 0, 0, 1, 0),
            # Тест 4: Обычное добавление очка (2→3)
            ({"player1": {"points": 2}, "player2": {"points": 1}}, "player1", "regular", 3, 1, 0, 0),

        ],
        ids=["Deuce_3-3", "Win_Game_4-1", "Normal_Point_2→3"]
    )
    def test_add_point(
            self,
            match,
            initial_dcore,
            player_key,
            expected_state,
            expected_points_player1,
            expected_points_player2,
            expected_games_player1,
            expected_games_player2
    ):
        strategy = RegularStateStrategy()
        score = json.loads(match.score)
        score["player1"]["points"] = initial_dcore["player1"]["points"]
        score["player2"]["points"] = initial_dcore["player2"]["points"]

        strategy.add_point(
            match,
            score,
            player_key=player_key,
            opponent_key="player2" if player_key == "player1" else "player1",
            player_num=1 if player_key == "player1" else 2
        )

        assert match.current_game_state == expected_state
        assert score["player1"]["points"] == expected_points_player1
        assert score["player2"]["points"] == expected_points_player2
        assert score["player1"]["games"] == expected_games_player1
        assert score["player2"]["games"] == expected_games_player2
