import json

import pytest

from src.services.strategies.deuce_state_strategy import DeuceStateStrategy
from tests.conftest import setup_score


class TestDeuceStateStrategy:
    @pytest.mark.parametrize(
        "initial_score, "
        "player_key, "
        "expected_state, "
        "expected_points_player1, "
        "expected_points_player2, "
        "expected_games_player1, "
        "expected_games_player2, "
        "expected_sets_player1, "
        "expected_sets_player2 ",
        [
            #  test 1 Переход в advantage_1
            ({"player1": {"points": 3}, "player2": {"points": 3}}, "player1", "advantage_1", 4, 3, 0, 0, 0, 0)
        ],
        ids=["advantage_4_3"]
    )
    def test_add_point(
            self,
            match,
            initial_score,
            player_key,
            expected_state,
            expected_points_player1,
            expected_points_player2,
            expected_games_player1,
            expected_games_player2,
            expected_sets_player1,
            expected_sets_player2
    ):
        strategy = DeuceStateStrategy()

        score = setup_score(match, initial_score)

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
        assert score["player1"]["sets"] == expected_sets_player1
        assert score["player2"]["sets"] == expected_sets_player2
