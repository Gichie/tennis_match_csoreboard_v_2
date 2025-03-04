from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class Player(Base):
    __tablename__ = 'players'
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)

    # Связь с таблицей Matches
    matches_as_player1: Mapped['Match'] = relationship(foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2: Mapped['Match'] = relationship(foreign_keys="Match.player2_id", back_populates="player2")
    matches_as_winner: Mapped['Match'] = relationship(foreign_keys="Match.winner_id", back_populates="winner")
