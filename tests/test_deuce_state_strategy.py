import json

import pytest

from src.services.strategies.deuce_state_strategy import DeuceStateStrategy


class TestDeuceStateStrategy:
    @pytest.mark.parametrize(
        "initial_score, "
        "player_key, "
        "expected_state, "
        "expected_points_player1, "
        "expected_points_player2",
        [
            #  test 1 Переход в advantage_1
            ({"player1": {"points": 3}, "player2": {"points": 3}}, "player1", "advantage_1", 4, 3)
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
    ):
        strategy = DeuceStateStrategy()
        score = json.loads(match.score)
        score["player1"]["points"] = initial_score["player1"]["points"]
        score["player2"]["points"] = initial_score["player2"]["points"]

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
