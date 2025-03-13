import pytest

from services.strategies.tie_break_state_strategy import TieBreakStateStrategy
from tests.conftest import setup_score


class TestTieBreakStateStrategy:
    @pytest.mark.parametrize(
        "initial_score, "
        "player_key, "
        "initial_game_state, "
        "expected_state, "
        "expected_points_player1, "
        "expected_points_player2, "
        "expected_games_player1, "
        "expected_games_player2, "
        "expected_sets_player1, "
        "expected_sets_player2 ",
        [
            #  test 1 Начало ti-break (0-0)
            (
                    {"player1": {"points": 0, "games": 6}, "player2": {"points": 0, "games": 6}},
                    "player1",
                    "tie_break",
                    "tie_break",
                    1, 0,
                    6, 6,
                    0, 0
            ),
            #  test 2 Конец tie-break (6-0) -> (7-0)
            (
                    {"player1": {"points": 6, "games": 6}, "player2": {"points": 0, "games": 6}},
                    "player1",
                    "tie_break",
                    "regular",
                    0, 0,
                    0, 0,
                    1, 0
            ),
            #  test 3 tie-break (6-6) -> (7-6) Продолжение tie-break, т.к. разницы в 2 очка нет
            (
                    {"player1": {"points": 6, "games": 6}, "player2": {"points": 6, "games": 6}},
                    "player1",
                    "tie_break",
                    "tie_break",
                    7, 6,
                    6, 6,
                    0, 0
            ),
            # Тест 4: Тай-брейк завершается при разнице в 2 очка (7-5)
            (
                    {"player1": {"points": 6, "games": 6}, "player2": {"points": 5, "games": 6}},
                    "player1",
                    "tie_break",
                    "regular",
                    0, 0,  # points сбрасываются
                    0, 0,  # games сбрасываются
                    1, 0  # player1 выигрывает сет
            )
        ],
        ids=["TieBreakStart(0-0)", "TieBreakEnd(6-0)", "TieBreakContinue(6-6)", "TieBreakEnd_7-5"]
    )
    def test_add_point(
            self,
            match,
            initial_score,
            player_key,
            initial_game_state,
            expected_state,
            expected_points_player1,
            expected_points_player2,
            expected_games_player1,
            expected_games_player2,
            expected_sets_player1,
            expected_sets_player2
    ):
        strategy = TieBreakStateStrategy()

        score = setup_score(match, initial_score)
        match.current_game_state = initial_game_state
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
