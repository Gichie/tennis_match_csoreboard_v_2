import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from myapp.models.player import Player

logger = logging.getLogger(__name__)


class PlayerService:
    @staticmethod
    def create_player(name: str) -> Player:
        player = Player(name=name.strip())
        return player

    @staticmethod
    def get_player_id(db: Session, name: str) -> int:
        try:
            # Проверяем валидность имени
            if not name or not isinstance(name, str):
                raise ValueError("Invalid player name")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise

        player = db.query(Player).filter(Player.name.ilike(name)).first()
        if not player:
            player = PlayerService.create_player(name)
            db.add(player)
            db.commit()
            db.refresh(player)
        return player.id

    @staticmethod
    def get_name(db: Session, player_id: int) -> str:
        player = db.query(Player).get(player_id)
        return player.name if player else 'Unknown'
