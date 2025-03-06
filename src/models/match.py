import json

from sqlalchemy import String, ForeignKey, event, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base
from .player import Player


class Match(Base):
    __tablename__ = 'matches'
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    player1_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    player2_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=True)
    score: Mapped[JSON] = mapped_column(JSON, nullable=False)
    current_game_state: Mapped[str] = mapped_column(String(26), default='regular')

    player1: Mapped[Player] = relationship(foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2: Mapped[Player] = relationship(foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner: Mapped[Player] = relationship(foreign_keys=[winner_id], back_populates="matches_as_winner")


# Обработчик события
@event.listens_for(Match, 'before_insert')
def set_default_score(mapper, connection, target):
    if not target.score:
        target.score = json.dumps({"player1": {"sets": 0, "games": 0, "points": 0},
                                   "player2": {"sets": 0, "games": 0, "points": 0}}, ensure_ascii=False)


@event.listens_for(Match, 'before_insert')
def validate_uuid(mapper, connection, target):
    if not target.uuid:
        raise ValueError("UUID must be set before insert!")
