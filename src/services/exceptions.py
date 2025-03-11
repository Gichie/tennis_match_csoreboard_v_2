class NotFoundMatchError(Exception):
    """Raised when a match is not found"""
    def __init__(self, match_uuid, message="Match not found"):
        self.match_uuid = match_uuid
        self.message = f"{message}: {match_uuid}"
        super().__init__(self.message)


class InvalidGameStateError(Exception):
    """Raised when the game state is invalid."""


class PlayerNumberError(Exception):
    """Raised when the request does not specify which player to add a point to."""


class InvalidScoreError(Exception):
    """Raised when score data is corrupted"""
