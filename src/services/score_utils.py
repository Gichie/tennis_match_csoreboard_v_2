from models.match import Match

SCORE_DIFF = 2
MIN_GAMES = 6
MIN_SETS = 2
MIN_TIE_BREAK_POINTS = 7


def process_tie_break(match: Match, score: dict[str, dict[str, int]], player_key: str, opponent_key: str) -> None:
    """
    Processes a point scored during a tie-break game.

    :param match: The Match object representing the current match.
    :param score: A dictionary representing the current score of the match.
    :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
    :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
    """
    score[player_key]['points'] += 1
    if (score[player_key]['points'] >= MIN_TIE_BREAK_POINTS and
            (score[player_key]['points'] - score[opponent_key]['points']) >= SCORE_DIFF):
        reset_set(match, score, player_key)


def reset_set(match: Match, score: dict[str, dict[str, int]], winner_key: str) -> None:
    """
    Resets the score for a set after a winner is determined.

    :param match: The Match object representing the current match.
    :param score: A dictionary representing the current score of the match.
    :param winner_key: The key representing the winner of the set (e.g., 'player1').
    """
    score[winner_key]["sets"] += 1
    score[winner_key]["games"] = 0
    opponent_key = "player2" if winner_key == "player1" else "player1"
    score[opponent_key]["games"] = 0
    score[winner_key]["points"] = 0
    score[opponent_key]["points"] = 0
    match.current_game_state = 'regular'


def reset_game(score: dict[str, dict[str, int]], winner_key: str) -> None:
    """
    Resets the score for a game after a winner is determined.

    :param score: A dictionary representing the current score of the match.
    :param winner_key: The key representing the winner of the game (e.g., 'player1').
    """
    score[winner_key]["games"] += 1
    score[winner_key]["points"] = 0
    opponent_key = "player2" if winner_key == "player1" else "player1"
    score[opponent_key]["points"] = 0


def is_match_finished(score: dict[str, dict[str, int]]) -> bool:
    """
    Checks if the match is finished.

    :param score: A dictionary representing the current score of the match.
    :return: True if the match is finished, False otherwise.
    """
    return score["player1"]["sets"] == MIN_SETS or score["player2"]["sets"] == MIN_SETS


def is_set_finished(score: dict[str, dict[str, int]], player_key: str, opponent_key: str) -> bool:
    """
    Checks if a set is finished.

    :param score: A dictionary representing the current score of the match.
    :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
    :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
    :return: True if the set is finished, False otherwise.
    """
    return (
            score[player_key]["games"] >= MIN_GAMES and
            abs(score[player_key]["games"] - score[opponent_key]["games"]) >= SCORE_DIFF
    )


def is_tie_break(score: dict[str, dict[str, int]], player_key: str, opponent_key: str) -> bool:
    """
    Checks if a set is at tie-break.

    :param score: A dictionary representing the current score of the match.
    :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
    :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
    :return: True if the set is at tie-break, False otherwise.
    """
    return score[player_key]["games"] == MIN_GAMES and score[opponent_key]["games"] == MIN_GAMES
