import pytest

from services.strategies.advantage_state_strategy import AdvantageStateStrategy
from tests.conftest import setup_score


class TestAdvantageStateStrategy:
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
        "expected_sets_player2",
        [
            #  Test 1 Выигрыш player 1 при advantage(4-3), переход в regular
            (
                    {"player1": {"points": 4}, "player2": {"points": 3}},
                    "player1",
                    "advantage_1",
                    "regular",
                    0, 0,
                    1, 0,
                    0, 0
            ),
            #  Test 2 Выигрыш player 2 при advantage(4-3), переход в deuce
            ({"player1": {"points": 4}, "player2": {"points": 3}}, "player2", "advantage_1", "deuce", 4, 4, 0, 0, 0, 0),
            #  Test 3 Выигрыш player 2 при advantage(3-4), переход в regular
            ({"player1": {"points": 3}, "player2": {"points": 4}}, "player2", "advantage_2", "regular", 0, 0, 0, 1, 0, 0),
            # Тест 4: Игрок 1 выигрывает, когда advantage у player2 (возврат в deuce)
            ({"player1": {"points": 3}, "player2": {"points": 4}}, "player1", "advantage_2", "deuce", 4, 4, 0, 0, 0, 0),
            # Тест 5: Инкремент геймов при существующих победах
            (
                    {"player1": {"points": 4, "games": 2}, "player2": {"points": 3}},
                    "player1",
                    "advantage_1",
                    "regular",
                    0, 0,
                    3, 0,
                    0, 0
            ),
            # Тест 6: Переход в tie-break при advantage_1 и счете в геймах 6-6
            (
                    {"player1": {"points": 4, "games": 5}, "player2": {"points": 3, "games": 6}},
                    "player1",
                    "advantage_1",
                    "tie_break",
                    0, 0,
                    6, 6,
                    0, 0
            )
        ],
        ids=[
            "WinGamePlayer1(4-3)",
            "WinGamePlayer2(4-3)",
            "WinGamePlayer2(3-4)",
            "BackToDeuceFromAdv2",
            "IncrementExistingGames",
            "TieBreak"
        ]
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
        strategy = AdvantageStateStrategy()
        match.current_game_state = initial_game_state
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

