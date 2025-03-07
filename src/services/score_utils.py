SCORE_DIFF = 2
MIN_GAMES = 3
MIN_SETS = 2


def process_tie_break(score: dict, player_key: str, opponent_key: str) -> None:
    score[player_key]['points'] += 1
    if (score[player_key]['points'] >= 7 and
            (score[player_key]['points'] - score[opponent_key]['points']) >= SCORE_DIFF):
        reset_set(score, player_key)


def reset_set(score: dict, winner_key: str) -> None:
    score[winner_key]["sets"] += 1
    score[winner_key]["games"] = 0
    opponent_key = "player2" if winner_key == "player1" else "player1"
    score[opponent_key]["games"] = 0
    score[winner_key]["points"] = 0
    score[opponent_key]["points"] = 0


def reset_game(score: dict, winner_key: str) -> None:
    score[winner_key]["games"] += 1
    score[winner_key]["points"] = 0
    opponent_key = "player2" if winner_key == "player1" else "player1"
    score[opponent_key]["points"] = 0


def is_match_finished(score) -> bool:
    return score["player1"]["sets"] == MIN_SETS or score["player2"]["sets"] == MIN_SETS


def is_set_finished(score: dict, player_key: str, opponent_key: str) -> bool:
    return (
            score[player_key]["games"] >= MIN_GAMES and
            abs(score[player_key]["games"] - score[opponent_key]["games"]) >= SCORE_DIFF
    )


def is_tie_break(score: dict, player_key: str, opponent_key: str) -> bool:
    return score[player_key]["games"] == MIN_GAMES and score[opponent_key]["games"] == MIN_GAMES
