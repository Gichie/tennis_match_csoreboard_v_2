from config.config import MIN_TIE_BREAK_POINTS, SCORE_DIFF, MIN_SETS, MIN_GAMES
from models.match import Match

ScoreDict = dict[str, dict[str, int]]


def process_tie_break(match: Match, score: ScoreDict, player_key: str, opponent_key: str) -> None:
    """
    Processes a point scored during a tie-break game.

    Increases the player's score. If the player scores at least
    MIN_TIE_BREAK_POINTS points and leads the opponent by at least SCORE_DIFF,
    the set is reset.

    :param match: The Match object representing the current match.
    :param score: A dictionary representing the current score of the match.
    :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
    :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
    """
    score[player_key]['points'] += 1
    if (score[player_key]['points'] >= MIN_TIE_BREAK_POINTS and
            (score[player_key]['points'] - score[opponent_key]['points']) >= SCORE_DIFF):
        reset_set(match, score, player_key)


def get_opponent_key(player_key: str) -> str:
    """
    Returns the opponent key given the player key.

    :param player_key: Player key (e.g. 'player1').
    :return: Opponent key (e.g. 'player2').
    """
    return "player2" if player_key == "player1" else "player1"


def reset_set(match: Match, score: ScoreDict, winner_key: str) -> None:
    """
    Resets the score for a set after a winner is determined.

    :param match: The Match object representing the current match.
    :param score: A dictionary representing the current score of the match.
    :param winner_key: The key representing the winner of the set (e.g., 'player1').
    """
    score[winner_key]["sets"] += 1
    score[winner_key]["games"] = 0
    opponent_key = get_opponent_key(winner_key)
    score[opponent_key]["games"] = 0
    score[winner_key]["points"] = 0
    score[opponent_key]["points"] = 0
    match.current_game_state = 'regular'


def reset_game(score: ScoreDict, winner_key: str) -> None:
    """
    Resets the score for a game after a winner is determined.

    :param score: A dictionary representing the current score of the match.
    :param winner_key: The key representing the winner of the game (e.g., 'player1').
    """
    score[winner_key]["games"] += 1
    score[winner_key]["points"] = 0
    opponent_key = get_opponent_key(winner_key)
    score[opponent_key]["points"] = 0


def is_match_finished(score: ScoreDict) -> bool:
    """
    Checks if the match is finished.

    :param score: A dictionary representing the current score of the match.
    :return: True if the match is finished, False otherwise.
    """
    res: bool = score["player1"]["sets"] == MIN_SETS or score["player2"]["sets"] == MIN_SETS
    return res


def is_set_finished(score: ScoreDict, player_key: str, opponent_key: str) -> bool:
    """
    Checks if a set is finished.

    :param score: A dictionary representing the current score of the match.
    :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
    :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
    :return: True if the set is finished, False otherwise.
    """
    res: bool = (
            score[player_key]["games"] >= MIN_GAMES and
            abs(score[player_key]["games"] - score[opponent_key]["games"]) >= SCORE_DIFF
    )
    return res


def is_tie_break(score: ScoreDict, player_key: str, opponent_key: str) -> bool:
    """
    Checks if a set is at tie-break.

    :param score: A dictionary representing the current score of the match.
    :param player_key: The key representing the player in the score dictionary (e.g., 'player1').
    :param opponent_key: The key representing the opponent in the score dictionary (e.g., 'player2').
    :return: True if the set is at tie-break, False otherwise.
    """
    res: bool = score[player_key]["games"] == MIN_GAMES and score[opponent_key]["games"] == MIN_GAMES
    return res
