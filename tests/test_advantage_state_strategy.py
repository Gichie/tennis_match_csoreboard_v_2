import pytest

from models.match import Match
from services.strategies.advantage_state_strategy import AdvantageStateStrategy
from tests.conftest import setup_score


class TestAdvantageStateStrategy:
    """
    Tests for the `AdvantageStateStrategy` class, focusing on the `add_point` method.
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
        "expected_sets_player2",
        [
            #  Test 1 Player 1 wins with advantage(4-3), transition to regular
            (
                    {"player1": {"points": 4}, "player2": {"points": 3}},
                    "player1",
                    "advantage_1",
                    "regular",
                    0, 0,
                    1, 0,
                    0, 0
            ),
            #  Test 2 Player 2 wins with advantage(4-3), transition to deuce
            ({"player1": {"points": 4}, "player2": {"points": 3}}, "player2", "advantage_1", "deuce", 4, 4, 0, 0, 0, 0),
            #  Test 3 Player 2 wins with advantage(3-4), transition to regular
            ({"player1": {"points": 3}, "player2": {"points": 4}}, "player2", "advantage_2", "regular", 0, 0, 0, 1, 0,
             0),
            # Test 4: Player 1 wins when player2 has advantage (return to deuce)
            ({"player1": {"points": 3}, "player2": {"points": 4}}, "player1", "advantage_2", "deuce", 4, 4, 0, 0, 0, 0),
            # Test 5: Increment of games with existing wins
            (
                    {"player1": {"points": 4, "games": 2}, "player2": {"points": 3}},
                    "player1",
                    "advantage_1",
                    "regular",
                    0, 0,
                    3, 0,
                    0, 0
            ),
            # Test 6: Tie-break transition with advantage_1 and game score 6-6
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
            match: Match,
            initial_score: dict,
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
        Tests the `add_point` method of the `AdvantageStateStrategy` class.

        :param match: A `Match` object (fixture).
        :param initial_score: A dictionary representing the initial score of the match.
        :param player_key: The key representing the player who scored a point ('player1' or 'player2').
        :param initial_game_state: The initial game state of the match (e.g., 'advantage_1', 'advantage_2').
        :param expected_state: The expected game state after adding the point.
        :param expected_points_player1: The expected number of points for player 1 after adding the point.
        :param expected_points_player2: The expected number of points for player 2 after adding the point.
        :param expected_games_player1: The expected number of games for player 1 after adding the point.
        :param expected_games_player2: The expected number of games for player 2 after adding the point.
        :param expected_sets_player1: The expected number of sets for player 1 after adding the point.
        :param expected_sets_player2: The expected number of sets for player 2 after adding the point.
        """
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
