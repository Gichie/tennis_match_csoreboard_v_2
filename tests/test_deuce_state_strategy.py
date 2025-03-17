import pytest

from models.match import Match
from services.strategies.deuce_state_strategy import DeuceStateStrategy
from tests.conftest import setup_score


class TestDeuceStateStrategy:
    """
    Tests for the `DeuceStateStrategy` class, specifically focusing on the `add_point` method.
    """

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
            # test 1 Transition to advantage_1
            ({"player1": {"points": 3}, "player2": {"points": 3}}, "player1", "advantage_1", 4, 3, 0, 0, 0, 0)
        ],
        ids=["advantage_4_3"]
    )
    def test_add_point(
            self,
            match: Match,
            initial_score: dict[str, dict[str, int]],
            player_key: str,
            expected_state: str,
            expected_points_player1: int,
            expected_points_player2: int,
            expected_games_player1: int,
            expected_games_player2: int,
            expected_sets_player1: int,
            expected_sets_player2: int
    ) -> None:
        """
        Tests the `add_point` method of the `DeuceStateStrategy` class.

        :param match: A `Match` object (fixture).
        :param initial_score: A dictionary representing the initial score of the match.
        :param player_key: The key representing the player who scored a point ('player1' or 'player2').
        :param expected_state: The expected game state after adding the point (e.g., 'advantage_1').
        :param expected_points_player1: The expected number of points for player 1 after adding the point.
        :param expected_points_player2: The expected number of points for player 2 after adding the point.
        :param expected_games_player1: The expected number of games for player 1 after adding the point.
        :param expected_games_player2: The expected number of games for player 2 after adding the point.
        :param expected_sets_player1: The expected number of sets for player 1 after adding the point.
        :param expected_sets_player2: The expected number of sets for player 2 after adding the point.
        """
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
