import pytest

from models.match import Match
from services.strategies.tie_break_state_strategy import TieBreakStateStrategy
from tests.conftest import setup_score


class TestTieBreakStateStrategy:
    """
    Tests for the `TieBreakStateStrategy` class, focusing on the `add_point` method.
    """

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
            # test 1 Start ti-break (0-0)
            (
                    {"player1": {"points": 0, "games": 6}, "player2": {"points": 0, "games": 6}},
                    "player1",
                    "tie_break",
                    "tie_break",
                    1, 0,
                    6, 6,
                    0, 0
            ),
            # test 2 End tie-break (6-0) -> (7-0)
            (
                    {"player1": {"points": 6, "games": 6}, "player2": {"points": 0, "games": 6}},
                    "player1",
                    "tie_break",
                    "regular",
                    0, 0,
                    0, 0,
                    1, 0
            ),
            # test 3 tie-break (6-6) -> (7-6) Continuation of tie-break, since there is no difference of 2 points
            (
                    {"player1": {"points": 6, "games": 6}, "player2": {"points": 6, "games": 6}},
                    "player1",
                    "tie_break",
                    "tie_break",
                    7, 6,
                    6, 6,
                    0, 0
            ),
            # Test 4: Tie-break ends with a difference of 2 points (7-5)
            (
                    {"player1": {"points": 6, "games": 6}, "player2": {"points": 5, "games": 6}},
                    "player1",
                    "tie_break",
                    "regular",
                    0, 0,
                    0, 0,
                    1, 0
            )
        ],
        ids=["TieBreakStart(0-0)", "TieBreakEnd(6-0)", "TieBreakContinue(6-6)", "TieBreakEnd_7-5"]
    )
    def test_add_point(
            self,
            match: Match,
            initial_score: dict[str, dict[str, int]],
            player_key: str,
            initial_game_state: str,
            expected_state: str,
            expected_points_player1: int,
            expected_points_player2: int,
            expected_games_player1: int,
            expected_games_player2: int,
            expected_sets_player1: int,
            expected_sets_player2: int
    ) -> None:
        """
        Tests the `add_point` method of the `TieBreakStateStrategy` class.

        :param match: A `Match` object (fixture).
        :param initial_score: A dictionary representing the initial score of the match.
        :param player_key: The key representing the player who scored a point ('player1' or 'player2').
        :param initial_game_state: The initial game state of the match, which should be 'tie_break'.
        :param expected_state: The expected game state after adding the point (e.g., 'tie_break', 'regular').
        :param expected_points_player1: The expected number of points for player 1 after adding the point.
        :param expected_points_player2: The expected number of points for player 2 after adding the point.
        :param expected_games_player1: The expected number of games for player 1 after adding the point.
        :param expected_games_player2: The expected number of games for player 2 after adding the point.
        :param expected_sets_player1: The expected number of sets for player 1 after adding the point.
        :param expected_sets_player2: The expected number of sets for player 2 after adding the point.
        """
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
