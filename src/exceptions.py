# Service Layer Exceptions
class NotFoundMatchError(Exception):
    """Raised when a match is not found"""


class InvalidGameStateError(Exception):
    """Raised when the game state is invalid."""


class PlayerNumberError(Exception):
    """Raised when the request does not specify which player to add a point to."""


class PlayerNotFound(Exception):
    """Raised when the player is not found in the database."""

    def __init__(self, player_id: int):
        super().__init__(f"Player with ID {player_id} not found")


class InvalidScoreError(Exception):
    """Raised when score data is corrupted"""


class DatabaseError(Exception):
    """Raised when database operation failed"""
