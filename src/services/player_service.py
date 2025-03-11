import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.player import Player
from src.services.exceptions import DatabaseError, PlayerNotFound

logger = logging.getLogger(__name__)


class PlayerService:
    @staticmethod
    def create_player(name: str) -> Player:
        player = Player(name=name.strip())
        return player

    @staticmethod
    def get_or_create_player_id(db: Session, name: str) -> int:
        try:
            player = db.query(Player).filter(Player.name.ilike(name)).first()
            if not player:
                player = PlayerService.create_player(name)
                db.add(player)
                db.commit()
                db.refresh(player)
            return player.id
        except SQLAlchemyError as e:
            raise DatabaseError('Failed to get or create player id')

    @staticmethod
    def get_name(db: Session, player_id: int) -> str:
        player = db.query(Player).get(player_id)
        if player:
            return player.name
        else:
            raise PlayerNotFound(player_id)
