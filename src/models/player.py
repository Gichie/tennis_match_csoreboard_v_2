from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class Player(Base):
    """
    Represents a player in the game.

    This class defines the structure of the 'players' table in the database.
    It stores information about each player, including their name.
    """
    __tablename__ = 'players'
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)

    # Relationships with the Matches table
    matches_as_player1: Mapped['Match'] = relationship(foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2: Mapped['Match'] = relationship(foreign_keys="Match.player2_id", back_populates="player2")
    matches_as_winner: Mapped['Match'] = relationship(foreign_keys="Match.winner_id", back_populates="winner")
