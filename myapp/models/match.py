import json

from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship

from .base import Base


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    player1_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player2_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    winner_id = Column(Integer, ForeignKey('players.id'), nullable=True)
    score = Column(String(1000), nullable=False)

    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner = relationship("Player", foreign_keys=[winner_id], back_populates="matches_as_winner")


# Обработчик события
@event.listens_for(Match, 'before_insert')
def set_default_score(mapper, connection, target):
    if not target.score:
        target.score = json.dumps({"sets": []}, ensure_ascii=False)


@event.listens_for(Match, 'before_insert')
def validate_uuid(mapper, connection, target):
    if not target.uuid:
        raise ValueError("UUID must be set before insert!")
