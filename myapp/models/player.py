from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True, unique=True)

    # Связь с таблицей Matches
    matches_as_player1 = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2 = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
    matches_as_winner = relationship("Match", foreign_keys="Match.winner_id", back_populates="winner")
