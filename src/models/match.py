import json

from sqlalchemy import String, ForeignKey, event, JSON, Connection
from sqlalchemy.orm import relationship, Mapped, mapped_column, Mapper

from models.base import Base
from models.player import Player


class Match(Base):
    """
    Represents a match between two players.

    This class defines the structure of the 'matches' table in the database.
    It stores information about the match, including the players involved,
    the winner, the score, and the current game state.
    """
    __tablename__ = 'matches'
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    player1_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    player2_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=True)
    score: Mapped[str] = mapped_column(JSON, nullable=False)
    current_game_state: Mapped[str] = mapped_column(String(26), default='regular')

    player1: Mapped[Player] = relationship(foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2: Mapped[Player] = relationship(foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner: Mapped[Player] = relationship(foreign_keys=[winner_id], back_populates="matches_as_winner")


# Event handler
@event.listens_for(Match, 'before_insert')
def set_default_score(mapper: Mapper[Match], connection: Connection, target: Match) -> None:
    """
    Sets a default score for a match if no score is provided during insertion.

    :param mapper: The mapper object.
    :param connection: The database connection.
    :param target: The instance of the Match class being inserted.
    """
    if not target.score:
        target.score = json.dumps({"player1": {"sets": 0, "games": 0, "points": 0},
                                   "player2": {"sets": 0, "games": 0, "points": 0}}, ensure_ascii=False)


@event.listens_for(Match, 'before_insert')
def validate_uuid(mapper: Mapper[Match], connection: Connection, target: Match) -> None:
    """
    Validates that a UUID is set before inserting a new match.

    :param mapper: The mapper object.
    :param connection: The database connection.
    :param target: The instance of the Match class being inserted.
    :raises ValueError: If the UUID is not set.
    """
    if not target.uuid:
        raise ValueError("UUID must be set before insert!")
